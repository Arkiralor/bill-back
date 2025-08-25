from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

from helpers.auth import UserModelHelpers
from schema.auth import RegisterUserSchema, ShowUserSchema, LoginUserSchema

@router.post("/register", response_model=ShowUserSchema)
def register_user(user_data: RegisterUserSchema):
    return UserModelHelpers.create_user(user_data)

@router.post("/login", response_model=ShowUserSchema)
def login_user(user_data: LoginUserSchema):
    return UserModelHelpers.authenticate_user_via_password(user_data.email, user_data.password)
    