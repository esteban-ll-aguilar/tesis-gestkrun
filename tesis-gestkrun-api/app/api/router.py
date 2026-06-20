from fastapi import APIRouter

from app.api.v1 import (
    artifacts,
    auth,
    backlog,
    boards,
    dashboard,
    health,
    messages,
    modules,
    projects,
    sprints,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(modules.router)
api_router.include_router(backlog.router)
api_router.include_router(sprints.router)
api_router.include_router(boards.router)
api_router.include_router(messages.router)
api_router.include_router(artifacts.router)
api_router.include_router(dashboard.router)
