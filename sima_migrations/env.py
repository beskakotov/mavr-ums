from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import keyring
from getpass import getpass

from ums.sima.common.classes import Base

def get_login_data():
    result = {'password': False, 'hostname': False}
    username = keyring.get_password('ums.sima.alembic', 'username')
    if not username:
        username = input('Username: ')
        password = getpass('Password: ')
    else:
        answer = input(f"Найден пользователь '{username}'. Использовать? (y, n)")
        if answer.lower() in ['y', 'yes']:
            password = keyring.get_password('ums.sima.alembic', 'password')
            result['password'] = True
        else:
            username = input('Username: ')
            password = getpass('Password: ')
    
    hostname = keyring.get_password('ums.sima.alembic', 'hostname')
    if not hostname:
        hostname = input('Hostname: ')
        port = int(input('Port: '))
    else:
        port = int(keyring.get_password('ums.sima.alembic', 'port'))
        answer = input(f"Подключиться по адресу: {hostname}:{port}? (y, n)")
        if answer.lower() in ['y', 'yes']:
            result['hostname'] = True
        else:
            hostname = input('Hostname: ')
            port = int(input('Port: '))
    if not result['password'] or not result['hostname']:
        answer = input(f"Сохранить введённые данные? (y, n)")
        if answer.lower() in ['y', 'yes']:
            keyring.set_password('ums.sima.alembic', 'username', username)
            keyring.set_password('ums.sima.alembic', 'password', password)
            keyring.set_password('ums.sima.alembic', 'hostname', hostname)
            keyring.set_password('ums.sima.alembic', 'port', port)
    return dict(username=username, hostname=hostname, password=password, port=port)


        
        


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", "postgresql+psycopg2://{username}:{password}@{hostname}:{port}/sima".format(**get_login_data()))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
target_metadata = Base.metadata
# target_metadata = None

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
