from fastapi import FastAPI
from app.api import rental
from app.api import store

app = FastAPI()

app.include_router(rental.router, prefix="/rental", tags=["Rentals"])
app.include_router(store.router, prefix="/store", tags=["Stores"])