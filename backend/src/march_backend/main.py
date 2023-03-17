"""
Main March backend.
"""
import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from . import auth
from .exceptions import PermissionDeniedError
from .mail import base, gmail

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


log = logging.getLogger(__name__)


@app.exception_handler(PermissionDeniedError)
async def permission_denied_handler(_: Request, exc: PermissionDeniedError):
    """Handle PermissionDeniedError and raise as HTTPException 403."""
    log.exception(exc)
    return JSONResponse(status_code=403, content={"message": "Permission denied."})


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
