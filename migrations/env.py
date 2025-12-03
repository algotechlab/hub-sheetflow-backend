import os
import sys
import pathlib
import asyncio
from logging.config import fileConfig

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))


from alembic import context
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from src.core.config.settings import get_settings
from src.core.domain.models import load_all_models
from src.core.domain.models.base import BaseModel


settings = get_settings()

config = context.config
config.set_main_option('sqlalchemy.url', settings.SQLALCHEMY_DATABASE_URI_MIGRATIONS)

target_metdata = BaseModel.metadata
load_all_models()


if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
    
def run_migrations_offline() -> None:
    context.configure(
        url=settings.SQLALCHEMY_DATABASE_URI_MIGRATIONS,
        target_metadata=target_metdata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        versions_table_schema=settings.POSTGRES_SCHEMA,
    )
    with context.begin_transaction():
        context.run_migrations()
        
        
def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metdata,
        compare_type=True,
        include_schemas=True,
        versions_table_schema=settings.POSTGRES_SCHEMA,
    )
    with context.begin_transaction():
        context.run_migrations()
        
async def run_migrations_online() -> None:
    connectable = create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI_MIGRATIONS,
        pool_pre_ping=True,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()
    
    
def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())
        
run_migrations()