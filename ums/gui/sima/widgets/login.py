from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QSpinBox, QCheckBox
from ast import literal_eval
import keyring
from ums.sima import Connection

class LoginWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent_widget = parent

        self.initIntreface()
        self.drawInterface()
    
    def initIntreface(self):
        username = keyring.get_password('ums.sima', 'DB_USER')
        self.l_username = QLabel('Username:')
        self.v_username = QLineEdit(username if username else '')

        password = keyring.get_password('ums.sima', 'DB_PASS')
        self.l_password = QLabel('Password:')
        self.v_password = QLineEdit()
        self.v_password.setEchoMode(QLineEdit.Password)
        self.v_password.setText(password if password else '')

        hostname = keyring.get_password('ums.sima', 'DB_HOST')
        self.l_hostname = QLabel('Hostname:')
        self.v_hostname = QLineEdit(hostname if hostname else '')

        port = keyring.get_password('ums.sima', 'DB_PORT')
        self.l_port = QLabel('Port:')
        self.v_port = QSpinBox()
        self.v_port.setRange(1, 99999)
        self.v_port.setValue(int(port) if port else 5432)
        
        dbname = keyring.get_password('ums.sima', 'DB_NAME')
        self.l_dbname = QLabel('Database name:')
        self.v_dbname = QLineEdit(dbname if dbname else '')

        self.l_save_password = QLabel('Save Password:')
        self.v_save_password = QCheckBox()
        save_password = keyring.get_password('ums.sima', 'SAVE')
        self.v_save_password.setChecked(literal_eval(save_password) if save_password else False)

        self.b_login = QPushButton('LOGIN')
        self.b_login.clicked.connect(self.login)
    
    def drawInterface(self):
        self.login_layout = QGridLayout()
        i = 0
        self.login_layout.addWidget(self.l_hostname, i, 0)
        self.login_layout.addWidget(self.v_hostname, i, 1)

        i += 1
        self.login_layout.addWidget(self.l_port, i, 0)
        self.login_layout.addWidget(self.v_port, i, 1)

        i += 1
        self.login_layout.addWidget(self.l_username, i, 0)
        self.login_layout.addWidget(self.v_username, i, 1)

        i += 1
        self.login_layout.addWidget(self.l_password, i, 0)
        self.login_layout.addWidget(self.v_password, i, 1)
        
        i += 1
        self.login_layout.addWidget(self.l_dbname, i, 0)
        self.login_layout.addWidget(self.v_dbname, i, 1)

        i += 1
        self.login_layout.addWidget(self.l_save_password, i, 0)
        self.login_layout.addWidget(self.v_save_password, i, 1)

        i += 1
        self.login_layout.addWidget(self.b_login, i, 0, 1, 2)

        self.setLayout(self.login_layout)

    def login(self):
        login_data = dict(
            DB_USER = self.v_username.text(),
            DB_PASS = self.v_password.text(),
            DB_HOST = self.v_hostname.text(),
            DB_PORT = self.v_port.value(),
            DB_NAME = self.v_dbname.text(),
        )

        if self.v_save_password.isChecked():
            self.saveLoginData(login_data)
        else:
            self.clearLoginData()

        Connection.login(**login_data)

        if Connection.getStatus:
            self.parent_widget.connectionEstablished.emit()
    
    def saveLoginData(self, login_data):
        for key in login_data.keys():
            keyring.set_password('ums.sima', key, login_data[key])
        keyring.set_password('ums.sima', 'SAVE', True)
    
    def clearLoginData(self):
        keyring.delete_password('ums.sima', 'DB_USER')
        keyring.delete_password('ums.sima', 'DB_PASS')
        keyring.delete_password('ums.sima', 'DB_HOST')
        keyring.delete_password('ums.sima', 'DB_PORT')
        keyring.delete_password('ums.sima', 'DB_NAME')
        keyring.delete_password('ums.sima', 'SAVE')