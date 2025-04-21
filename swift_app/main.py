from fastapi import FastAPI

from .database import init_db
from .routers.bank_router import bank_router

app = FastAPI()
app.include_router(bank_router)


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}
