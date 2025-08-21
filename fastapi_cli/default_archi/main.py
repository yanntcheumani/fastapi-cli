
from fastapi import FastAPI
from core.config import settings
from api.routers import routers

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(routers)

@app.get("/")
def read_root():
    return {"Hello": "World"}