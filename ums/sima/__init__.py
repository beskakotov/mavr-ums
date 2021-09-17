from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import Signal, Slot, Qt
import sys

from ums.sima.widgets.login import LoginWidget
from ums.sima.widgets.gui import SimaMainWidget
from ums.sima.common.connection import Connection

from ums import __mainversion__, __subversion__

class SimaGUI(QMainWindow):
    connectionEstablished = Signal(Connection)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('SIMA login form || UMS v{}.{}'.format(__mainversion__, __subversion__))
        self.connectionEstablished.connect(self.setConnection)
        self.setCentralWidget(LoginWidget(parent=self))
        self.setMinimumSize(325, 100)
    
    @Slot()
    def setConnection(self, conn):
        self.setWindowTitle('(S)peckle (I)nterferometry (M)easurements (A)rchive || UMS v{}.{}'.format(__mainversion__, __subversion__))
        self.setCentralWidget(SimaMainWidget(parent=self, conn=conn))
        self.setWindowState(Qt.WindowMaximized)

def run():
    app = QApplication(sys.argv)
    w = SimaGUI()
    w.show()
    app.exec_()