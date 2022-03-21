from PySide2.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PySide2.QtCore import Signal, Slot, Qt
import sys
from time import sleep
from ums.sima import Connection
from ums.gui.sima.widgets.login import LoginWidget
from ums.gui.sima.widgets.main import MenuWidget

from ums import __mainversion__, __subversion__, __debugversion__

PROGRAM_NAME = f'UMS v{__mainversion__}.{__subversion__}.{__debugversion__}'

class SimaGUI(QMainWindow):
    connectionEstablished = Signal(Connection)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'SIMA || Login form || {PROGRAM_NAME}')
        self.connectionEstablished.connect(self.setConnection)
        self.setCentralWidget(LoginWidget(parent=self))
        self.setMaximumSize(325, 175)
    
    @Slot()
    def setConnection(self, conn):
        self.conn = conn
        self.setWindowTitle(f'SIMA || Main menu || {PROGRAM_NAME}')
        self.setCentralWidget(MenuWidget(parent=self))
        self.setMinimumSize(350, 250)
        # self.setWindowState(Qt.WindowMaximized)

def run():
    app = QApplication(sys.argv)
    w = SimaGUI()
    w.show()
    app.exec_()