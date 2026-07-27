import logging
from datetime import datetime

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def compute_dashboard_metrics(project_id: str) -> dict:
    logger.info("Computing dashboard metrics for project %s", project_id)
    return {
        "project_id": project_id,
        "total_tasks": 0,
        "in_progress": 0,
        "blocked": 0,
        "completed": 0,
        "computed_at": datetime.utcnow().isoformat(),
    }


@celery_app.task
def compute_sprint_velocity(sprint_id: str) -> dict:
    logger.info("Computing sprint velocity for sprint %s", sprint_id)
    return {
        "sprint_id": sprint_id,
        "velocity": 0,
        "computed_at": datetime.utcnow().isoformat(),
    }


@celery_app.task
def send_password_reset_email(email: str, reset_token: str) -> None:
    logger.info("Sending password reset email to %s", email)


@celery_app.task
def cleanup_expired_sessions() -> int:
    logger.info("Cleaning up expired sessions")
    return 0


@celery_app.task
def generate_daily_summary(project_id: str) -> dict:
    logger.info("Generating daily summary for project %s", project_id)
    return {
        "project_id": project_id,
        "generated_at": datetime.utcnow().isoformat(),
    }
