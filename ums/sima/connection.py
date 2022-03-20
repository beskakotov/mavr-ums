from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class Connection:
    __role__ = 'guest'
    status = False
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.session = Session(create_engine(f"postgresql+psycopg2://{self.username}:{self.password}@{self.hostname}:{self.port}/sima"))
        self.updateRole()

    def updateRole(self):
        result = self.session.execute(f"""SELECT rolname FROM pg_roles WHERE pg_has_role('{self.username}', oid, 'member') and rolname != '{self.username}';""")
        self.__role__ = result.fetchone()[0]
        self.status = True
        
    def getRole(self):
        return self.__role__