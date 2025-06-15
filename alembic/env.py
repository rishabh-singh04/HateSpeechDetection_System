# from logging.config import fileConfig

# from sqlalchemy import engine_from_config, create_engine

# from sqlalchemy import pool
# from app.db.base import Base  
# from alembic import context
# from app.db.models.user import User
# from app.db.models.policy import PolicyDocument

# # this is the Alembic Config object, which provides
# # access to the values within the .ini file in use.
# config = context.config

# # Interpret the config file for Python logging.
# # This line sets up loggers basically.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # add your model's MetaData object here
# # for 'autogenerate' support
# # from myapp import mymodel
# # target_metadata = mymodel.Base.metadata

# target_metadata = Base.metadata

# # other values from the config, defined by the needs of env.py,

# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode.

#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable
#     here as well.  By skipping the Engine creation
#     we don't even need a DBAPI to be available.

#     Calls to context.execute() here emit the given string to the
#     script output.

#     """
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode."""
#     # Use URL from alembic.ini directly (bypass .env issues)
#     url = config.get_main_option("sqlalchemy.url")
#     connectable = create_engine(url)  # Directly create engine from URL

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, 
#             target_metadata=target_metadata
#         )
#         with context.begin_transaction():
#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()

# else:
#     run_migrations_online()


############# docker  ###############
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine, pool
from alembic import context
from app.db.base import Base
from app.db.models.user import User
from app.db.models.policy import PolicyDocument

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    # return f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
    #        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    return os.getenv("SQLALCHEMY_DATABASE_URL")

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(get_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
