__all__ = [
    "ProfileCurrencyPydantic",
    "ProfileCurrencyPydanticPartial",
    "YTDPerformance",
    "YTDMinMax",
    "Error"
]

import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models import User, ProfileCurrency

from tortoise.contrib.pydantic import pydantic_model_creator

UserPydantic = pydantic_model_creator(User)
ProfileCurrencyPydantic = pydantic_model_creator(ProfileCurrency)

class ProfileCurrencyPydanticPartial(ProfileCurrencyPydantic):
    name: str | None = None
    amount: Decimal | None = None

class YTDPerformance(BaseModel):
    performance: Decimal

class YTDPoint(BaseModel):
    amount: Decimal
    date: datetime.date

class YTDMinMax(BaseModel):
    min: YTDPoint
    max: YTDPoint

class Error(BaseModel):
    detail: str