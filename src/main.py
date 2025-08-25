from fastapi import FastAPI, Request, Response
from routers.bill import router as bill_router
from routers.auth import router as auth_router
from config.global_settings import global_settings

app = FastAPI()

app.include_router(auth_router)
app.include_router(bill_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/settings/")
async def get_settings():
    return {
        "app_name": global_settings.APP_NAME,
        "debug": global_settings.DEBUG,
        "base_url": global_settings.BASE_URL,
        "env_type": global_settings.ENV_TYPE,
        "allowed_hosts": global_settings.ALLOWED_HOSTS,
        "time_zone": global_settings.TIME_ZONE,
        "use_tz": global_settings.USE_TZ,
        "mongo_url": str(global_settings.MONGO_URL),
        "jwt_algorithm": global_settings.JWT_ALGORITHM,
        "access_token_expire_minutes": global_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh_token_expire_minutes": global_settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        "otp_attempt_limit": global_settings.OTP_ATTEMPT_LIMIT,
        "otp_attempt_timeout": global_settings.OTP_ATTEMPT_TIMEOUT
    }
