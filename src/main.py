from contextlib import asynccontextmanager
from multiprocessing import cpu_count
import uvicorn

from fastapi import FastAPI, Request, Response
from bill_app.routers import router as bill_router
from auth_app.routers import router as auth_router
from config.global_settings import global_settings, ShowSettingsSchema, GlobalSettings

from utils.repo_init import init_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_indexes()
    yield
    # Shutdown logic
    # (close DB connections etc.)
    print("App shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(bill_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/settings/", response_model=GlobalSettings)
async def get_settings():
    return ShowSettingsSchema(**global_settings.model_dump(mode="json"))

if __name__ == "__main__":
    print(f"Starting server at {global_settings.BASE_URL}")
    print(f"Debug mode is {'on' if global_settings.DEBUG else 'off'}")
    print(f"Environment: {global_settings.ENV_TYPE}")
    uvicorn.run(
            "main:app", 
            host="0.0.0.0", 
            port=global_settings.BASE_PORT,       # 👈 set your port here
            reload= True if global_settings.DEBUG else False,
            workers=1 if global_settings.DEBUG else int(cpu_count() // 2), 
        )