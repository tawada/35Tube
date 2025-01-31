from fastapi import FastAPI

from . import middlewares

app = FastAPI()
middlewares.add_middlewares(app)
