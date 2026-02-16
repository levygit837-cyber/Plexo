from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.proxy_parser import parse_proxy
from backend.services.proxy_checker import check_proxy

router = APIRouter(prefix="/api/proxy", tags=["proxy"])


class ProxyParseRequest(BaseModel):
    raw: str


class ProxyValidateRequest(BaseModel):
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None


@router.post("/parse")
def parse_proxy_endpoint(request: ProxyParseRequest):
    result = parse_proxy(request.raw)
    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Could not parse proxy string. Supported formats: "
            "host:port:user:pass, user:pass@host:port, host:port, "
            "http://user:pass@host:port",
        )
    return result


@router.post("/validate")
async def validate_proxy_endpoint(request: ProxyValidateRequest):
    result = await check_proxy(
        host=request.host,
        port=request.port,
        username=request.username,
        password=request.password,
    )
    return {
        "valid": result.valid,
        "ip": result.ip,
        "city": result.city,
        "country": result.country,
        "timezone": result.timezone,
        "error": result.error,
    }
