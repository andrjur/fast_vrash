from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
from logging.config import fileConfig
from models import TaskOrm  # Импортируйте вашу базу или модели

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = TaskOrm.metadata  # Убедитесь, что здесь указана ваша метадата

async def run_migrations_online() -> None:
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(context.configure, target_metadata=target_metadata)

        async with connection.begin():
            await context.run_migrations()

def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        import asyncio
        asyncio.run(run_migrations_online())

run_migrations()
