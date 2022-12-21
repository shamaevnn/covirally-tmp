from typing import TypedDict


class Token(TypedDict):
    access_token: str
    token_type: str


class JWTData(TypedDict):
    username: str
