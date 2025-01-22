from typing import Annotated

from fastapi import Header, HTTPException

from app.settings import Settings


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != Settings.API_TOKEN:
        raise HTTPException(status_code=401, detail="X-Token header invalid")