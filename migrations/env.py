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


# Add project root to Python path (Windows-compatible)
project_root = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, project_root)
print(f"Project root: {project_root}")
print(f"sys.path: {sys.path}")

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
    """Run migrations in 'online' mode with async engine."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        echo=True
    )

    def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    import asyncio
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()