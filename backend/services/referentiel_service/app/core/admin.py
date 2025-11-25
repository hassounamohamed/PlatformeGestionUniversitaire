from fastapi import Header, HTTPException
from typing import Optional
from starlette.status import HTTP_401_UNAUTHORIZED
from app.core.config2 import settings


def admin_required(x_admin_token: Optional[str] = Header(None)):
    """Simple admin dependency that checks the X-Admin-Token header against the configured ADMIN_API_KEY.

    Development mode: when ADMIN_API_KEY is empty we allow access for convenience.
    For production, set ADMIN_API_KEY in the environment and the header X-Admin-Token must match.
    """
    configured = getattr(settings, "ADMIN_API_KEY", "")
    # If no admin key configured, allow admin actions in development (convenience)
    if not configured:
        return True
    if not x_admin_token or x_admin_token != configured:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid admin token")
    return True
