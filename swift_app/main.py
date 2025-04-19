from fastapi import FastAPI

from .databse import init_db

app = FastAPI()


@app.lifespan("startup")
def on_startup():
    init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}
