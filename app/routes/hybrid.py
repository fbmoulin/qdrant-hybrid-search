"""
Hybrid search routes (to be expanded).
"""

from fastapi import APIRouter

router = APIRouter(prefix="/hybrid", tags=["hybrid"])

# Future: dedicated endpoints if we want /hybrid/search separate from the root /search