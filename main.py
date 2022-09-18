import datetime as dt

import finnhub
from fastapi import Depends, FastAPI, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise

from app.config import get_settings
from app.dependencies import *
from app.models import *
from app.pydantic_models import *
from app.utils import *

settings = get_settings()
app = FastAPI(title="DarkStore Crypto Portfolio", docs_url="/", redoc_url=None)


@app.get(
    "/profile", response_model=list[ProfileCurrencyPydantic], tags=["Basic Profile"]
)
async def profile_list(user: User = Depends(JWTBearer())):
    return await ProfileCurrencyPydantic.from_queryset(
        ProfileCurrency.filter(user=user)
    )


@app.post("/profile", response_model=ProfileCurrencyPydantic, tags=["Basic Profile"])
async def add_profile_currency(
    profile_currency: ProfileCurrencyPydantic, user: User = Depends(JWTBearer())
):
    profile_currency_obj = await ProfileCurrency.create(
        user=user, **profile_currency.dict()
    )
    return await ProfileCurrencyPydantic.from_tortoise_orm(profile_currency_obj)


@app.patch(
    "/profile/{currency}",
    response_model=ProfileCurrencyPydantic,
    responses={status.HTTP_404_NOT_FOUND: {"model": Error}},
    tags=["Basic Profile"],
)
async def update_profile_currency(
    currency: str,
    profile_currency: ProfileCurrencyPydanticPartial,
    user: User = Depends(JWTBearer()),
):
    await ProfileCurrency.filter(name=currency, user=user).update(
        **profile_currency.dict(exclude_unset=True)
    )
    return await ProfileCurrencyPydantic.from_queryset_single(
        ProfileCurrency.get(name=currency, user=user)
    )


@app.delete(
    "/profile/{currency}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"model": Error}},
    tags=["Basic Profile"],
)
async def delete_profile_currency(currency: str, user: User = Depends(JWTBearer())):
    deleted_count = await ProfileCurrency.filter(user=user, name=currency).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Object does not exist"
        )


@app.get(
    "/ytd",
    response_model=YTDPerformance,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Error}},
    tags=["YTD"],
)
async def get_profile_ytd(
    client: finnhub.Client = Depends(finnhub_client), user: User = Depends(JWTBearer())
):
    profile = await ProfileCurrency.filter(user=user)
    try:
        performance = sum(profile_performance_generator(client, profile))
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )
    return {"performance": performance}


@app.get(
    "/ytd/min-max",
    response_model=YTDMinMax,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Error}},
    tags=["YTD"],
)
async def get_profile_ytd_min_max(
    client: finnhub.Client = Depends(finnhub_client), user: User = Depends(JWTBearer())
):
    profile = await ProfileCurrency.filter(user=user)
    if len(profile):
        try:
            values = (
                get_currency_values(client, currency.name, get_ytd_borders())
                for currency in profile
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong.",
            )
        (min_value, min_value_index), (
            max_value,
            max_value_index,
        ) = get_profile_min_max(values)
        min_date = dt.date(dt.date.today().year, 1, 1) + dt.timedelta(
            days=min_value_index
        )
        max_date = dt.date(dt.date.today().year, 1, 1) + dt.timedelta(
            days=max_value_index
        )
    else:
        min_value = max_value = 0
        min_date = max_date = dt.date.today()
    return {
        "min": {"amount": min_value, "date": min_date},
        "max": {"amount": max_value, "date": max_date},
    }


@app.post(
    "/wipe",
    dependencies=[Depends(admin_user)],
    status_code=204,
    responses={status.HTTP_403_FORBIDDEN: {"model": Error}},
    tags=["Administration"],
)
async def wipe():
    await ProfileCurrency.all().delete()
    await User.all().delete()


@app.post(
    "/populate",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Error}},
    tags=["Administration"],
)
async def populate():
    try:
        await populate_db()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )


register_tortoise(
    app,
    db_url=settings.POSTGRES_URI,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(reload=True)
