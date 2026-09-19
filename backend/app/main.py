from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.core.config import settings
from app.planner.router import router as planner_router

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)
app.include_router(auth_router, prefix="/api")
app.include_router(planner_router, prefix="/api")


@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    """No await is needed: this endpoint performs no I/O."""

    return {"status": "ok"}
