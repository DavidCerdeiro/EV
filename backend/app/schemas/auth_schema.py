from pydantic import BaseModel

class TokenRequest(BaseModel):
    """
    Schema for token request.
    """
    application: str
    token: str
    refresh_token: str | None = None

class TokenPayload(TokenRequest):
    pass