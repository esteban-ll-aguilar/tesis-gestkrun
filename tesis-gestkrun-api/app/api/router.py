from fastapi import APIRouter

from app.api.v1 import auth, backlog, boards, health, modules, projects, sprints

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(modules.router)
api_router.include_router(backlog.router)
api_router.include_router(sprints.router)
api_router.include_router(boards.router)
