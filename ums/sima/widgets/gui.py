from PySide2.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QSpinBox, QPushButton, QCheckBox, QTabWidget, QTableView
# from PySide2.QtGui import QPixmap, QImage, QIcon
# from PySide2.QtCore import Qt
# from os import path
# import pickle
import pandas as pd

from ums import __mainversion__, __subversion__
from ums.common.widgets import ErrorMessage
from ums.sima.common.classes import StarOrAsteroid
from ums.sima.common.for_table import DataFrameModel

class SimaMainWidget(QWidget):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.parent_widget = parent
        self.connection = conn
        self.session = self.connection.session

        self.initInterface()
        self.drawInterface()
        self.loadTable()

    def initInterface(self):
        self.tabWidget = QTabWidget()
        self.table = QTableView()
        # header = self.table.horizontalHeader()
        # print(header)
        # print(dir(header))
        self.b_add = QPushButton('Add object')
        self.b_add.clicked.connect(self.showAddWidget)
    
    def drawInterface(self):
        self.main_layout = QGridLayout()

        i = 0
        self.main_layout.addWidget(self.table, i, 0, 1, 10)

        i =+ 1
        self.main_layout.addWidget(self.b_add, i, 9)

        self.setLayout(self.main_layout)
    
    def showAddWidget(self):
        self.setEnabled(False)
        
    def loadTable(self):
        df = pd.read_sql(self.session.query(StarOrAsteroid).statement, self.session.bind) 
        model = DataFrameModel(df)
        self.table.setModel(model)