import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from core.models import Base

config = context.config

load_dotenv()

db_user = os.getenv("DATABASE_USER", "postgres")
db_password = os.getenv("DATABASE_PASSWORD", "mysecretpassword")
db_host = os.getenv("DATABASE_HOST", "localhost")
db_port = os.getenv("DATABASE_PORT", "5432")
db_name = os.getenv("DATABASE_NAME", "mydatabase")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
COUNTER_FILE = os.path.join(os.path.dirname(__file__), "migration_counter.txt")


config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def get_next_revision_id() -> str:
    """Reads a counter from a file, increments it, and returns the new value as a string."""
    # If the file does not exist, create it with an initial counter of 1.
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("1")
        return "1"

    # Otherwise, read the current counter, increment it, and write it back.
    with open(COUNTER_FILE, "r+") as f:
        contents = f.read().strip()
        try:
            current_val = int(contents)
        except ValueError:
            current_val = 0
        next_val = current_val + 1

        # Rewind and overwrite with the incremented value.
        f.seek(0)
        f.write(str(next_val))
        f.truncate()

    return str(next_val)


def process_revision_directives(context, revision, directives):
    """Custom callback that sets the numeric revision ID before Alembic creates the file."""
    script = directives[0]
    script.rev_id = get_next_revision_id()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
