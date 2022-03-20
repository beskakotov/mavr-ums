from logging.config import fileConfig
from matplotlib.style import use

from sqlalchemy import engine_from_config
from sqlalchemy import pool
import psycopg2
from getpass import getpass

from alembic import context

import keyring

def get_keyring_values(force_new=False):
    def validate_parameters():
        username = keyring.get_password('ums.sima', 'username')
        password = keyring.get_password('ums.sima', 'password')
        host = keyring.get_password('ums.sima', 'host')
        port = keyring.get_password('ums.sima', 'port')
        dbname = keyring.get_password('ums.sima', 'dbname')
        try:
            connection = psycopg2.connect(
                dbname=dbname,
                user=username,
                password=password,
                host=host,
                port=port
            )
        except:
            return get_keyring_values(force_new=True)
        else:
            return dict(DB_USER=username, DB_PASS=password, DB_HOST=host, DB_PORT=port, DB_NAME=dbname)


    username = keyring.get_password('ums.sima', 'username')
    if force_new or username is None:
        if force_new and username is not None:
            print('Error in login data. Please, input new.')
        keyring.set_password('ums.sima', 'username', input('Enter database username: '))
        keyring.set_password('ums.sima', 'password', getpass('Enter database password: '))
        keyring.set_password('ums.sima', 'host', input('Enter database host: '))
        keyring.set_password('ums.sima', 'port', input('Enter database port: '))
        keyring.set_password('ums.sima', 'dbname', input('Enter database name: '))
        return validate_parameters()
    else:
        return validate_parameters()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
section = config.config_ini_section

db_data = get_keyring_values()

config.set_section_option(section, "DB_USER", db_data['DB_USER'])
config.set_section_option(section, "DB_PASS", db_data['DB_PASS'])
config.set_section_option(section, "DB_HOST", db_data['DB_HOST'])
config.set_section_option(section, "DB_PORT", db_data['DB_PORT'])
config.set_section_option(section, "DB_NAME", db_data['DB_NAME'])

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from ums import sima
target_metadata = sima.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
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


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
