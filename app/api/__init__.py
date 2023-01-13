from fastapi import APIRouter

from . import auth, ping, post

router = APIRouter(prefix="/api")
router.include_router(ping.router)
router.include_router(auth.router)
router.include_router(post.router)
