"""
Main March backend.
"""
import uvicorn
from fastapi import FastAPI

from . import auth
from .mail import base, gmail

app = FastAPI()


@app.get("/")
async def root() -> dict:
    """Root Hello World page"""

    return {"message": "Hello World"}


app.include_router(auth.router, prefix="/auth")
app.include_router(base.router, prefix="/mail/base")
app.include_router(gmail.router, prefix="/mail/gmail")


def start():
    """Start the app."""
    uvicorn.run("march_backend.main:app", host="0.0.0.0", port=8000, reload=True)
