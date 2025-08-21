import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import create_async_engine

parent_dir = os.path.abspath(os.getcwd())
sys.path.append(parent_dir)

from app.models.model_base import ModelBase

load_dotenv()


# Alembic config object
config = context.config

# Set sqlalchemy.url from environment variable
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Set target metadata for autogenerate
target_metadata = ModelBase.metadata
print(f"Registered tables: {list(ModelBase.metadata.tables.keys())}")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode with synchronous engine."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()