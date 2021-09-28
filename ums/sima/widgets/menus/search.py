from PySide2.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QSpinBox
from PySide2.QtCore import Qt

from ums.sima.common.classes import Program

class ByName(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.__init_interface()
        self.__draw_interface()
    
    def __init_interface(self):
        self.name = QLabel("Search by name of object")

        self.l_name = QLabel("Name:")
        self.v_name = QLineEdit()
        self.v_type = QComboBox()
        self.v_type.addItems(('Star', 'Asteroid'))
        self.b_search = QPushButton('Search')

    def __draw_interface(self):
        self.main_layout = QGridLayout()

        i = 0
        self.main_layout.addWidget(self.name, i, 0, 1, 4, Qt.AlignCenter)
        
        i += 1
        self.main_layout.addWidget(self.l_name, i, 0)
        self.main_layout.addWidget(self.v_name, i, 1)
        self.main_layout.addWidget(self.v_type, i, 2)
        self.main_layout.addWidget(self.b_search, i, 3)
        
        self.setLayout(self.main_layout)

class ByCoordinates(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.__init_interface()
        self.__draw_interface()

    def __init_interface(self):
        self.name = QLabel('Search by coordinates')

        self.l_ra = QLabel('R.a.:')
        self.v_ra = QLineEdit()
        self.v_ra.setToolTip('00 00 00.00')

        self.l_dec = QLabel('Dec.:')
        self.v_dec = QLineEdit()
        self.v_dec.setToolTip('(+/-)00 00 00.00')

        self.l_region = QLabel('Region:')
        self.v_region = QSpinBox()
        self.v_region.setRange(0, 60)
        self.v_region.setValue(2)
        self.t_region = QComboBox()
        self.t_region.addItems(('deg', 'min', 'sec'))
        self.t_region.setCurrentIndex(1)


        self.b_search = QPushButton('Search')
        self.b_search.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

    def __draw_interface(self):
        self.main_layout = QGridLayout()

        i = 0
        self.main_layout.addWidget(self.name, i, 0, 1, 4, Qt.AlignCenter)

        i =+ 1
        self.main_layout.addWidget(self.l_ra, i, 0)
        self.main_layout.addWidget(self.v_ra, i, 1, 1, 2)
        
        i += 1
        self.main_layout.addWidget(self.l_dec, i, 0)
        self.main_layout.addWidget(self.v_dec, i, 1, 1, 2)

        i += 1
        self.main_layout.addWidget(self.l_region, i, 0)
        self.main_layout.addWidget(self.v_region, i, 1)
        self.main_layout.addWidget(self.t_region, i, 2)


        self.main_layout.addWidget(self.b_search, 1, 3, i, 1)

        self.setLayout(self.main_layout)

class ByProgram(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_widget = parent

        self.__init_interface()
        self.__draw_interface()

    def __init_interface(self):
        self.name = QLabel('Search by program')
        self.l_program = QLabel('Program:')
        self.v_program = QComboBox()
        self.v_program.addItems(map(str, self.search_programs()))
        self.b_search = QPushButton('Search')

    def __draw_interface(self):
        self.main_layout = QGridLayout()
        i = 0
        self.main_layout.addWidget(self.name, i, 0, 1, 3, Qt.AlignCenter)

        i += 1
        self.main_layout.addWidget(self.l_program, i, 0)
        self.main_layout.addWidget(self.v_program, i, 1)
        self.main_layout.addWidget(self.b_search, i, 2)
        self.setLayout(self.main_layout)

    def search_programs(self):
        return self.parent().conn.session.query(Program).all()