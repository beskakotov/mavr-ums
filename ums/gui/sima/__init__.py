from PySide2.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PySide2.QtCore import Signal, Slot, Qt
import sys
from time import sleep
from ums.sima import Connection
from ums.gui.sima.widgets import LoginWidget
from ums.gui.sima.widgets import MenuWidget

from ums import __version__

class SimaGUI(QMainWindow):
    connectionEstablished = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'SIMA || Login form || {__version__.get()}')
        self.connectionEstablished.connect(self.setConnection)
        self.setCentralWidget(LoginWidget(parent=self))
        self.setMaximumSize(325, 175)
    
    @Slot()
    def setConnection(self):
        self.setWindowTitle(f'SIMA || Main menu || {__version__.get()}')
        self.setCentralWidget(MenuWidget(parent=self))
        self.setMinimumSize(350, 250)

def run():
    app = QApplication(sys.argv)
    w = SimaGUI()
    w.show()
    app.exec_()