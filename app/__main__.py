from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app import api


def get_app() -> FastAPI:
    application = FastAPI()
    application.include_router(api.router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_app()
if __name__ == "__main__":  # pragma: no cover
    run(
        "app.__main__:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        reload_dirs=["app", "tests"],
        log_level="debug",
    )
