"""Authentication api"""
import json
from typing import List, Tuple, Union

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from requests_oauthlib import OAuth2Session

router = APIRouter()


class OAuth2TokenModel(BaseModel):
    """Model for OAuth2Token."""

    access_token: str
    expires_in: int
    refresh_token: str
    scope: List[str]
    token_type: str
    id_token: str
    expires_at: float


@router.get("/auth/", tags=["authentication"])
async def root():
    """Main page."""
    return {"message": "Authenticating."}


async def get_google_session(
    state: Union[str, None] = None
) -> Tuple[OAuth2Session, dict]:
    """Get a Google OAuth2 session."""
    secret = {}
    with open("client_secret.json", "rt", encoding="utf-8") as secret_file:
        secret = json.loads(secret_file.read())
        print(f"secret: {secret}")
        secret = secret["web"]
    return (
        OAuth2Session(
            client_id=secret["client_id"],
            state=state,
            scope=[
                "https://mail.google.com/",
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            redirect_uri=secret["redirect_uris"][0],
        ),
        secret,
    )


@router.get("/auth/oauth/token", tags=["authentication"])
async def oauth_token(state: str, code: str) -> OAuth2TokenModel:
    """Get the OAuth2 authentication token."""
    google, secret = await get_google_session(state=state)
    args = [secret["token_uri"]]
    kwargs = {"client_secret": secret["client_secret"], "code": code}
    print(f"fetchging token for {args} {kwargs}")
    token = google.fetch_token(*args, **kwargs)
    return token


@router.get(
    "/auth/oauth/start", tags=["authentication"], response_class=RedirectResponse
)
async def oauth_start():
    """Authenticate using OAuth for google."""
    google, secret = await get_google_session()
    authorization_url = google.authorization_url(
        secret["auth_uri"], access_type="offline", prompt="select_account"
    )[0]
    return authorization_url
