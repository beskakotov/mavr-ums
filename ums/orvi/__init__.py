from PySide2.QtWidgets import QApplication
from ums.orvi.gui import OrVI_GUI
import sys

def run():
    app = QApplication(sys.argv)
    w = OrVI_GUI()
    w.show()
    app.exec_()