import os.path
from logging.config import fileConfig
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.auth.models import user_table, Users
from src.profiles.models import profiles_table, Profile
from src.likes.models import likes, Likes

from src.auth.models import metadata as user_metadata
from src.profiles.models import metadata as profiles_metadata
from src.likes.models import metadata as likes_metadata
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_USER

sys.path.append(os.path.join(sys.path[0], 'src'))

config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_PASS", DB_PASS)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_HOST", DB_HOST)

fileConfig(config.config_file_name)

target_metadata = [user_metadata, profiles_metadata, likes_metadata]

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
