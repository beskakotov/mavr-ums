from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from keyring import get_password, set_password
from getpass import getpass
import psycopg2

def get_db_login_data(force_new=False):
    def validate_parameters():
        DB_USER = get_password('ums.sima', 'DB_USER')
        DB_PASS = get_password('ums.sima', 'DB_PASS')
        DB_HOST = get_password('ums.sima', 'DB_HOST')
        DB_PORT = get_password('ums.sima', 'DB_PORT')
        DB_NAME = get_password('ums.sima', 'DB_NAME')
        try:
            connection = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT
            )
        except Exception as e:
            print(e)
            return get_db_login_data(force_new=True)
        else:
            return dict(DB_USER=DB_USER, DB_PASS=DB_PASS, DB_HOST=DB_HOST, DB_PORT=DB_PORT, DB_NAME=DB_NAME)


    username = get_password('ums.sima', 'DB_USER')
    if force_new or username is None:
        if force_new and username is not None:
            print('Error in login data. Please, input new.')
        set_password('ums.sima', 'DB_USER', input('Enter database username: '))
        set_password('ums.sima', 'DB_PASS', getpass('Enter database password: '))
        set_password('ums.sima', 'DB_HOST', input('Enter database host: '))
        set_password('ums.sima', 'DB_PORT', input('Enter database port: '))
        set_password('ums.sima', 'DB_NAME', input('Enter database name: '))
        return validate_parameters()
    else:
        return validate_parameters()

class Connection:
    __database_data__ = get_db_login_data()
    __engine__ = create_engine(f"""postgresql+psycopg2://{__database_data__['DB_USER']}:{__database_data__['DB_PASS']}@{__database_data__['DB_HOST']}:{__database_data__['DB_PORT']}/{__database_data__['DB_NAME']}""")
    __session__ = Session(__engine__)
    __role__ = __session__.execute(f"""SELECT rolname FROM pg_roles WHERE pg_has_role('{__database_data__['DB_USER']}', oid, 'member') and rolname != '{__database_data__['DB_USER']}';""").fetchone()[0]
    # __status__ = True

    @classmethod
    def getRole(cls):
        return cls.__role__
    
    @classmethod
    def getSession(cls):
        return cls.__session__
    
    @classmethod
    def getStatus(cls):
        return cls.__session__.is_active
    
    @classmethod
    def getDatabaseLoginData(cls):
        return cls.__database_data__
    
    @classmethod
    def login(cls, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME):
        if cls.__session__.is_active:
            cls.__session__.close()
        cls.__engine__ = create_engine(f"""postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}""")
        cls.__session__ = Session(cls.__engine__)
        cls._role__ = cls.__session__.execute(f"""SELECT rolname FROM pg_roles WHERE pg_has_role('{DB_USER}', oid, 'member') and rolname != '{DB_USER}';""").fetchone()[0]
        pass