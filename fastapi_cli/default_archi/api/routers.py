from api.v1.router import router_v1
from fastapi import APIRouter

routers = APIRouter(prefix="/api")

routers.include_router(router_v1, prefix="/v1", tags=["v1"])
