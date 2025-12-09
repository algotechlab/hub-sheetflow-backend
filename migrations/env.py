import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import Connection

from src.core.domain.models.base import BaseModel
from src.core.domain.models import load_all_models

config = context.config
fileConfig(config.config_file_name)

DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    os.getenv("SQLALCHEMY_DATABASE_URI")
)
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL para migrações não foi definida!")

load_all_models()
target_metadata = BaseModel.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    engine = create_async_engine(
        DATABASE_URL,
        future=True,
    )
    async with engine.connect() as conn:
        await conn.run_sync(do_run_migrations)
    await engine.dispose()


def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


run_migrations()
