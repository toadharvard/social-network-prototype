from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["Check health"])


@router.get("")
async def health_check() -> str:
    return "Pong!"
