from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QSpinBox, QCheckBox
from ast import literal_eval
import keyring

from ums import __mainversion__, __subversion__
from ums.sima.common.connection import Connection

class LoginWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent_widget = parent

        self.initIntreface()
        self.drawInterface()
    
    def initIntreface(self):
        username = keyring.get_password('ums.sima.login_form', 'username')
        self.l_username = QLabel('Username:')
        self.v_username = QLineEdit(username if username else '')

        password = keyring.get_password('ums.sima.login_form', 'password')
        self.l_password = QLabel('Password:')
        self.v_password = QLineEdit()
        self.v_password.setEchoMode(QLineEdit.Password)
        self.v_password.setText(password if password else '')

        hostname = keyring.get_password('ums.sima.login_form', 'hostname')
        self.l_hostname = QLabel('Hostname:')
        self.v_hostname = QLineEdit(hostname if hostname else '')

        self.l_port = QLabel('Port:')
        self.v_port = QSpinBox()
        self.v_port.setRange(1, 99999)
        port = keyring.get_password('ums.sima.login_form', 'port')
        self.v_port.setValue(int(port) if port else 5432)

        self.l_save_password = QLabel('Save Password:')
        self.v_save_password = QCheckBox()
        save_password = keyring.get_password('ums.sima.login_form', 'saveparams')
        self.v_save_password.setChecked(literal_eval(save_password) if save_password else False)

        self.b_login = QPushButton('LOGIN')
        self.b_login.clicked.connect(self.login)
    
    def drawInterface(self):
        self.login_layout = QGridLayout()

        self.login_layout.addWidget(self.l_hostname, 0, 0)
        self.login_layout.addWidget(self.v_hostname, 0, 1)

        self.login_layout.addWidget(self.l_port, 1, 0)
        self.login_layout.addWidget(self.v_port, 1, 1)

        self.login_layout.addWidget(self.l_username, 2, 0)
        self.login_layout.addWidget(self.v_username, 2, 1)

        self.login_layout.addWidget(self.l_password, 3, 0)
        self.login_layout.addWidget(self.v_password, 3, 1)

        self.login_layout.addWidget(self.l_save_password, 4, 0)
        self.login_layout.addWidget(self.v_save_password, 4, 1)

        self.login_layout.addWidget(self.b_login, 5, 0, 1, 2)

        self.setLayout(self.login_layout)

    def login(self):
        login_data = dict(
            username = self.v_username.text(),
            password = self.v_password.text(),
            hostname = self.v_hostname.text(),
            port = self.v_port.value(),
        )

        if self.v_save_password.isChecked():
            self.saveLoginData(login_data)
        else:
            self.clearLoginData()

        conn = Connection(**login_data)

        if conn.status:
            self.parent_widget.connectionEstablished.emit(conn)
    
    def saveLoginData(self, login_data):
        for key in login_data.keys():
            keyring.set_password('ums.sima.login_form', key, login_data[key])
        keyring.set_password('ums.sima.login_form', 'saveparams', True)
    
    def clearLoginData(self):
        keyring.set_password('ums.sima.login_form', 'username', '')
        keyring.set_password('ums.sima.login_form', 'password', '')
        keyring.set_password('ums.sima.login_form', 'hostname', '')
        keyring.set_password('ums.sima.login_form', 'port', '')
        keyring.set_password('ums.sima.login_form', 'saveparams', False)