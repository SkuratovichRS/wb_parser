from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.settings import Settings

jobstores = {
    "default": SQLAlchemyJobStore(
        url=f"postgresql://{Settings.POSTGRES_USER}:{Settings.POSTGRES_PASSWORD}@{Settings.POSTGRES_HOST}:"
        f"{Settings.POSTGRES_PORT}/{Settings.POSTGRES_DB}",
        tablename="jobstore",
    ),
}

job_defaults = {"coalesce": False, "max_instances": 1}
scheduler = AsyncIOScheduler(jobstores=jobstores, job_defaults=job_defaults)
