from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

from auth_app.helpers import UserModelHelpers
from auth_app.models import UserModel
from auth_app.schema import RegisterUserSchema, ShowUserSchema, LoginUserSchema, TokenSchema
from auth_app.utils import get_current_user

@router.post("/register", response_model=ShowUserSchema)
def register_user(user_data: RegisterUserSchema):
    return UserModelHelpers.create_user(user_data)

@router.post("/login", response_model=TokenSchema)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = LoginUserSchema(email=form_data.username, password=form_data.password)
    return UserModelHelpers.authenticate_user_via_password(user_data)

@router.post("/login/v2", response_model=TokenSchema)
def login_user(form_data: LoginUserSchema):
    user_data = LoginUserSchema(email=form_data.email, password=form_data.password)
    return UserModelHelpers.authenticate_user_via_password(user_data)

@router.get("/me", response_model=ShowUserSchema)
async def get_current_user(current_user: UserModel = Depends(get_current_user)):
    return ShowUserSchema(**current_user.model_dump(mode="json"))
    