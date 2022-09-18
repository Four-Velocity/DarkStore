__all__ = [
    "JWTBearer",
    "admin_user",
    "finnhub_client"
]

from typing import Any

import finnhub
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status, Depends

from app.models import User
from app.config import get_settings

import jwt

settings = get_settings()


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> User:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            payload = self.get_jwt_payload(credentials.credentials)
            user = await self.identify_user(payload["name"])
            if not user:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")
            return user

    @staticmethod
    def get_jwt_payload(token: str) -> dict[str, Any]:
        return jwt.decode(token, algorithms="HS256", options={"verify_signature": False})

    @staticmethod
    async def identify_user(user_name) -> User | None:
        return await User.get_or_none(full_name=user_name)


def admin_user(user: User = Depends(JWTBearer())):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin permission required")


def finnhub_client() -> finnhub.Client:
    return finnhub.Client(api_key=settings.FINNHUB_SECRET)
