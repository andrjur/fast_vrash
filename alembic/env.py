from logging.config import fileConfig
from sqlalchemy import engine_from_config
from alembic import context
from datab import Model
from config import settings

config = context.config
fileConfig(config.config_file_name)
target_metadata = Model.metadata

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = engine_from_config(configuration)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations() 