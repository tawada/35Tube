from fastapi import FastAPI
from fastapi_pagination import add_pagination

from . import middlewares

app = FastAPI()
add_pagination(app)
middlewares.add_middlewares(app)
