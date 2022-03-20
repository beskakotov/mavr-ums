from PySide2.QtWidgets import QWidget, QVBoxLayout #, QPushButton, QLabel, QLineEdit, QSpinBox, QCheckBox
from ast import literal_eval
import keyring

from ums import __mainversion__, __subversion__
from ums.sima.common.connection import Connection

from ums.sima.widgets.menus import search

class MenuWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent_widget = parent

        self.drawInterface()

    def drawInterface(self):
        self.menu_layout = QVBoxLayout()

        widget_list = search.ByName, search.ByCoordinates, search.ByProgram

        for widget in widget_list:
            self.menu_layout.addWidget(widget(self.parent_widget))

        self.setLayout(self.menu_layout)