from fastapi import status

from auth_app.models import UserModel, BlacklistedTokenModel
from auth_app.schema import RegisterUserSchema, ShowUserSchema, LoginUserSchema, TokenSchema, LogoutSchema
from auth_app.utils import create_access_token, create_refresh_token
from passlib.context import CryptContext
from database import database

from config.global_settings import global_settings
from config.boilerplate.response_template import GenericResponseModel

class UserModelHelpers:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)
    
    @classmethod
    def get_user_by_email(cls, email: str):
        user = database.get_collection(UserModel.Meta.collection_name).find_one({"email": email.strip().lower()})
        if user:
            return UserModel.model_validate(user)
        return None

    @classmethod
    def create_user(cls, user_data: RegisterUserSchema):
        data = user_data.model_dump()
        data["password"] = cls.pwd_context.hash(user_data.password)
        if cls.get_user_by_email(user_data.email):
            raise ValueError("User with this email already exists")
        
        user_obj = UserModel(**data)
        user_obj.save()
        return ShowUserSchema(**user_obj.model_dump())
    
    @classmethod
    def authenticate_user_via_password(cls, data: LoginUserSchema) -> TokenSchema:
        user = cls.get_user_by_email(data.email)
        if not user:
            raise ValueError("User with this email does not exist")
        if not cls.verify_password(data.password, user.password):
            raise ValueError("Incorrect password")
        
        tokens = {
            "access_token": create_access_token(user),
            "refresh_token": create_refresh_token(user)
        }

        return TokenSchema(**tokens)
    
    @classmethod
    def logout_user(cls, logout_data: LogoutSchema) -> GenericResponseModel:
        access_token = logout_data.access_token
        refresh_token = logout_data.refresh_token

        blacklisted_access_token = BlacklistedTokenModel(token=access_token)
        blacklisted_access_token.save()

        blacklisted_refresh_token = BlacklistedTokenModel(token=refresh_token)
        blacklisted_refresh_token.save()

        res = GenericResponseModel(
            message="Successfully logged out",
            status_code=status.HTTP_200_OK
        )

        return res
        