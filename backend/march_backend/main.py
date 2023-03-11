"""
Main March backend.
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root() -> dict:
    """Root Hello World page"""

    return {"message": "Hello World"}


def start():
    """Start the app."""
    uvicorn.run("march_backend.main:app", host='0.0.0.0', port=8000,
                reload=True, workers=2)
