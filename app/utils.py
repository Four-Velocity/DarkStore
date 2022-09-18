__all__ = [
    "get_ytd_borders",
    "profile_performance_generator",
    "get_currency_values",
    "get_profile_min_max",
    "populate_db",
]

import datetime as dt
from decimal import Decimal
from itertools import zip_longest
from typing import Generator, Iterable

import finnhub
from tortoise import Tortoise

from app.models import ProfileCurrency, User


def get_ytd_borders() -> tuple[int, int]:
    year_start_timestamp = round(dt.datetime(dt.date.today().year, 1, 1).timestamp())
    current_timestamp = round(dt.datetime.now().timestamp())
    return year_start_timestamp, current_timestamp


def profile_performance_generator(
    client: finnhub.Client, profile: list[ProfileCurrency]
) -> Generator[Decimal, None, None]:
    ytd_borders = get_ytd_borders()
    for currency in profile:
        data = client.crypto_candles(f"BINANCE:{currency}USDT", "D", *ytd_borders)
        if data["s"] == "no_data":
            yield 0
            continue
        yield currency.amount * Decimal(data["c"][-1]) - currency.amount * Decimal(
            data["c"][0]
        )


def get_currency_values(
    client: finnhub.Client, currency: str, ytd_borders: tuple[int, int]
) -> Iterable[Decimal]:
    data = client.crypto_candles(f"BINANCE:{currency}USDT", "D", *ytd_borders)
    if data["s"] == "no_data":
        return [Decimal(0)]
    return map(lambda x: Decimal(x), data["c"])


def get_profile_min_max(
    values: Iterable[Iterable[Decimal]],
) -> tuple[tuple[Decimal, int], tuple[Decimal, int]]:
    min_value = None
    max_value = None
    for index, daily_values in enumerate(zip_longest(*values, fillvalue=Decimal(0))):
        daily_value = sum(daily_values)
        if max_value is None or daily_value > max_value[0]:
            max_value = daily_value, index
        if min_value is None or daily_value < min_value[0]:
            min_value = daily_value, index
    return min_value, max_value


async def populate_db():
    await Tortoise.generate_schemas()
    users = ({"full_name": "John Doe"}, {"full_name": "admin"})
    currencies = (
        {"name": "BTC", "amount": Decimal(0.122)},
        {"name": "ETH", "amount": Decimal(1)},
    )
    if not len(await User.all()):
        for user in users:
            created_user = await User.create(**user)
            for currency in currencies:
                await ProfileCurrency.create(user=created_user, **currency)
