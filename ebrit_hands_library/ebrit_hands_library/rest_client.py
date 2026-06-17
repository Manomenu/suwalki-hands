import httpx
from pydantic import BaseModel

_TIMEOUT = httpx.Timeout(connect=10, read=None, write=10, pool=10)


async def post(url: str, body: BaseModel) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body.model_dump(), timeout=_TIMEOUT)
        response.raise_for_status()
    return response.json()
