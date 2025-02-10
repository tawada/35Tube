from fastapi import FastAPI
from fastapi_pagination import add_pagination

from . import middlewares, routers

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
add_pagination(app)
middlewares.add_middlewares(app)
app.include_router(routers.router)
