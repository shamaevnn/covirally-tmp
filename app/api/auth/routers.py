from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth.utils import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)
from app.api.errors import InvalidCredentials
from app.schemas import TokenResponse
from app.types import JWTData

auth_router = APIRouter(tags=["Authentication"], prefix="/auth")


@auth_router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenResponse:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise InvalidCredentials()
    access_token = create_access_token(
        data=JWTData(username=user.username), expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    res: TokenResponse = TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
    return res
