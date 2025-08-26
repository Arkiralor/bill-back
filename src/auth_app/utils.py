from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from bcrypt import hashpw, gensalt, checkpw
from auth_app.models import UserModel, BlacklistedTokenModel
from config.global_settings import global_settings
from jwt import encode, decode, PyJWTError, ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, status
from fastapi import Depends
from typing import Annotated

from database import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(user: UserModel):
    expires_on = datetime.now(tz=timezone.utc) + timedelta(minutes=global_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user.id,
        "scope": "access",
        "exp": expires_on
    }

    try:
        token = encode(
            payload,
            global_settings.SECRET_KEY,
            algorithm=global_settings.JWT_ALGORITHM
        )
        return token

    except PyJWTError as e:
        print(f"Error creating access token: {e}")
        return None


def verify_access_token(token: str):
    if database.get_collection(BlacklistedTokenModel.Meta.collection_name).find_one({"token": token}):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode(
            token,
            global_settings.SECRET_KEY,
            algorithms=[global_settings.JWT_ALGORITHM]
        )

        if payload.get("scope") != "access":
            raise ValueError("Invalid token scope")

        return payload
    except ExpiredSignatureError as ex:
        obj = BlacklistedTokenModel(token=token)
        obj.save()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex
    except PyJWTError as e:
        print(f"Error verifying access token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except ValueError as ve:
        print(f"Token validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from ve


def create_refresh_token(user: UserModel):
    expires_on = datetime.now(tz=timezone.utc) + timedelta(minutes=global_settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user.id,
        "scope": "refresh",
        "exp": expires_on
    }
    try:
        token = encode(
            payload,
            global_settings.SECRET_KEY,
            algorithm=global_settings.JWT_ALGORITHM
        )
        return token

    except PyJWTError as e:
        print(f"Error creating refresh token: {e}")
        return None


def verify_refresh_token(token: str):
    if database.get_collection(BlacklistedTokenModel.Meta.collection_name).find_one({"token": token}):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode(
            token,
            global_settings.SECRET_KEY,
            algorithms=[global_settings.JWT_ALGORITHM]
        )

        if payload.get("scope") != "refresh":
            raise ValueError("Invalid token scope")
        return payload
    except ExpiredSignatureError as ex:
        obj = BlacklistedTokenModel(token=token)
        obj.save()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex
    except PyJWTError as e:
        print(f"Error verifying refresh token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except ValueError as ve:
        print(f"Token validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from ve

def refresh_tokens(refresh_token: str):
    payload = verify_refresh_token(refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = database.get_collection(
        UserModel.Meta.collection_name).find_one({"id": user_id})
    user_obj = UserModel.model_validate(user)
    if not user_obj or not user_obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    old_refresh_token_obj = BlacklistedTokenModel(token=refresh_token)
    old_refresh_token_obj.save()

    new_access_token = create_access_token(user_obj)
    new_refresh_token = create_refresh_token(user_obj)

    if not new_access_token or not new_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create tokens",
        )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
    }

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)
    except InvalidTokenError:
        raise credentials_exception
    user = database.get_collection(
        UserModel.Meta.collection_name).find_one({"_id": payload.get("sub")})
    if user is None:
        raise credentials_exception
    user_obj = UserModel.model_validate(user)
    user_obj.last_login = datetime.now(tz=timezone.utc)
    user_obj.save()
    return user_obj