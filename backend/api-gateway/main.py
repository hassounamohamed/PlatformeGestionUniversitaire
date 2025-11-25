"""Simple API Gateway for local development.

Features:
- Route /api/<service>/... to configured backend service URLs
- Optional JWT validation for protected routes (uses auth service settings)
- Forwards method, headers, query params and body transparently

Usage:
- Configure target service URLs via environment variables or edit the defaults below.
"""
from typing import Dict

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
import httpx

# Import shared settings from auth service so we validate tokens with the same secret
try:
    from services.auth_service.app.config import settings as auth_settings
except Exception:
    # Fallback defaults if import fails
    class _S:  # pragma: no cover - fallback for limited envs
        SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
        ALGORITHM = os.getenv("ALGORITHM", "HS256")

    auth_settings = _S()

app = FastAPI(title="API Gateway", version="1.0.0")

# Development CORS (allow all). For production restrict this to your frontend origin(s).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routing table: map the first path segment after /api to a service base URL.
# These can be overridden with environment variables.
ROUTES: Dict[str, str] = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://127.0.0.1:8001/api/auth"),
    "admin": os.getenv("ADMIN_SERVICE_URL", "http://127.0.0.1:8002/api/admin"),
    "student": os.getenv("STUDENT_SERVICE_URL", "http://127.0.0.1:8003/api/student"),
    "teacher": os.getenv("TEACHER_SERVICE_URL", "http://127.0.0.1:8004/api/teacher"),
}

# Public prefixes that do not require JWT validation
PUBLIC_PREFIXES = {"auth"}


async def validate_jwt_if_required(request: Request):
    """Raise 401 if the route is protected and JWT is missing/invalid.

    This is deliberately lightweight: it decodes/validates the token signature and
    expiry using the auth service settings, and attaches the token payload to
    request.state.jwt_payload when valid.
    """
    path = request.url.path
    # Expect paths like /api/<service>/...
    parts = path.lstrip("/").split("/")
    if len(parts) < 2 or parts[0] != "api":
        return
    service = parts[1]
    if service in PUBLIC_PREFIXES:
        return

    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = auth_header.split()
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Unsupported auth scheme")

    # Validate token signature and expiry using python-jose if available,
    # otherwise perform a minimal base64 decode check (best-effort fallback).
    try:
        from jose import jwt, JWTError

        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        # Attach to request state for downstream handlers if needed
        request.state.jwt_payload = payload
    except Exception as e:  # noqa: BLE001 - broad catch here to keep gateway resilient
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


@app.api_route("/api/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def proxy(full_path: str, request: Request):
    """Generic proxy endpoint.

    It takes the incoming request path /api/<service>/... and routes it to the
    corresponding backend based on the ROUTES table while forwarding method,
    headers, query params and body.
    """
    # Validate JWT for protected routes
    await validate_jwt_if_required(request)

    parts = full_path.split("/")
    if not parts:
        raise HTTPException(status_code=400, detail="Invalid path")

    service_key = parts[0]
    target_base = ROUTES.get(service_key)
    if not target_base:
        raise HTTPException(status_code=404, detail=f"Unknown service: {service_key}")

    # Reconstruct target URL
    remaining_path = "/".join(parts[1:])
    if remaining_path:
        if target_base.endswith("/"):
            target_url = f"{target_base}{remaining_path}"
        else:
            target_url = f"{target_base}/{remaining_path}"
    else:
        target_url = target_base

    # Forward request
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Prepare headers: forward most headers but override host-related ones
        headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}

        try:
            body = await request.body()
            resp = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                content=body if body else None,
                headers=headers,
                allow_redirects=False,
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Error contacting upstream service: {exc}")

    # Build response back to the caller
    excluded_headers = {"transfer-encoding", "content-encoding", "content-length", "connection"}
    response_headers = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded_headers]
    return Response(content=resp.content, status_code=resp.status_code, headers=dict(response_headers))


@app.get("/")
async def root():
    return {"message": "API Gateway running", "routes": list(ROUTES.keys())}
