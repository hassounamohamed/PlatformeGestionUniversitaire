from fastapi import Header, HTTPException
from typing import Optional
from starlette.status import HTTP_401_UNAUTHORIZED
from app.core.config2 import settings


def admin_required(x_admin_token: Optional[str] = Header(None)):
    """Simple admin dependency that checks the X-Admin-Token header against the configured ADMIN_API_KEY.

    - If ADMIN_API_KEY is empty (not configured) the dependency will deny access.
    - This is intentionally simple: for production use integrate with your auth service.
    """
    configured = getattr(settings, "ADMIN_API_KEY", "")
    if not configured:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Admin access disabled by server configuration")
    if not x_admin_token or x_admin_token != configured:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid admin token")
    return True
