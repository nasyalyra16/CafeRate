import os
from typing import Optional

from fastapi import Header, HTTPException, status

# Bisa diganti lewat environment variable CAFERATE_API_KEY.
API_KEY = os.getenv("CAFERATE_API_KEY", "caferate-dev-key")


def verify_api_key(x_api_key: Optional[str] = Header(default=None)) -> str:
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key tidak ada atau tidak valid.",
        )
    return "authorized-client"
