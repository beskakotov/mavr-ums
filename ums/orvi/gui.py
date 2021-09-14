from PySide2.QtWidgets import QMessageBox, QWidget, QGridLayout, QLineEdit, QLabel, QWidget, QGridLayout, QPushButton, QFileDialog, QSpinBox, QRadioButton
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtCore import Qt
from os import path
import pickle

from ums import __mainversion__, __subversion__
from ums.orvi.orbitparams import OrbitParams
from ums.orvi.plotparams import PlotParams
from ums.orvi.image import OrbitImage
from ums.common.widgets import ErrorMessage

class OrVI_GUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('(Or)bits (V)isualisation (I)nterface) || UMS v{}.{}'.format(__mainversion__, __subversion__))
        self.setFixedSize(800, 0)
        # self.setFixedSize(0, 0)
        self.last_path = '.'

        self.__init_interface()
        self.__draw_interface()
        self.orbit_image_widget = OrbitImage(self)
    
    def show(self):
        super().show()
        self.orbit_image_widget.show()

    def __init_interface(self):
        self.l_input = QLabel('File.inp: ')
        self.v_input = QLineEdit()
        self.v_input.setReadOnly(True)

        self.l_output = QLabel('File.out: ')
        self.v_output = QLineEdit()
        self.v_output.setReadOnly(True)

        self.b_OpenI = QPushButton('Выбрать')
        self.b_OpenI.clicked.connect(self.c_OpenI)

        self.b_OpenO = QPushButton('Выбрать')
        self.b_OpenO.clicked.connect(self.c_OpenO)

        self.b_Show = QPushButton('Показать')
        self.b_Show.clicked.connect(self.c_Show)
        self.b_Load = QPushButton('Загрузить')
        self.b_Load.clicked.connect(self.c_Load)
        self.b_Save = QPushButton('Сохранить')
        self.b_Save.clicked.connect(self.c_Save)
        self.b_Save.setEnabled(False)
        self.b_Source = QPushButton('Из файла')
        self.b_Source.setCheckable(True)
        self.b_Source.clicked.connect(self.c_Source)

        self.OrbitParams = OrbitParams(self)
        self.OrbitParams.setEnabled(False)
        self.PlotParams = PlotParams(self)
        self.PlotParams.setEnabled(False)

    def __draw_interface(self):
        self.main_layout = QGridLayout()

        i = 0
        self.main_layout.addWidget(self.l_input, i, 0)
        self.main_layout.addWidget(self.v_input, i, 1, 1, 7)
        self.main_layout.addWidget(self.b_OpenI, i, 8)
        
        i += 1
        self.main_layout.addWidget(self.l_output, i, 0)
        self.main_layout.addWidget(self.v_output, i, 1, 1, 7)
        self.main_layout.addWidget(self.b_OpenO, i, 8)
        
        i += 1
        self.main_layout.addWidget(QLabel('Орбитальные параметры'), i, 0, 1, 2)
        self.main_layout.addWidget(self.b_Source, i, 2, 1, 2)

        i += 1
        self.main_layout.addWidget(self.OrbitParams, i, 0, 1, 9, Qt.AlignTop)

        i += 1
        self.main_layout.addWidget(self.PlotParams, i, 0, 1, 9, Qt.AlignTop)

        i += 1
        self.main_layout.addWidget(self.b_Show, i, 0, 1, 3)
        self.main_layout.addWidget(self.b_Save, i, 3, 1, 3)
        self.main_layout.addWidget(self.b_Load, i, 6, 1, 3)

        self.setLayout(self.main_layout)
    
    def c_OpenI(self):
        fName = QFileDialog.getOpenFileName(self, 'Open input file', self.last_path, "*.inp")[0]
        if fName:
            self.last_path = path.dirname(fName)
            self.v_input.setText(fName)
            self.OrbitParams.clear_all()
            self.PlotParams.clear_all()
    
    def c_OpenO(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open output file', self.last_path, "*.out")[0]
        if file_name:
            self.last_path = path.dirname(file_name)
            self.v_output.setText(file_name)
    
    def c_Source(self):
        if self.b_Source.isChecked():
            self.b_Source.setText('Из интерфейса')
        else:
            self.b_Source.setText('Из файла')

    def c_Show(self):
        self.orbital_parameters = self.OrbitParams.collectParams(
            self.v_input.text(),
            self.v_output.text(),
            self.b_Source.isChecked()
        )
        self.plot_parameters = self.PlotParams.collectParams()

        if self.orbital_parameters:
            self.b_Save.setEnabled(True)
            self.PlotParams.setEnabled(True)
            self.OrbitParams.setEnabled(True)
        else:
            ErrorMessage("Ошибка загрузки орбитального решения").show()
            return 0
        self.orbit_image_widget.plot(self.orbital_parameters, self.plot_parameters)

    def c_Save(self):
        self.orbit_image_widget.fig.savefig(self.get_save_file_name(self.v_input.text()[:-3]+'png'), bbox_inches='tight', dpi=300)
        self.orbit_image_widget.fig.savefig(self.get_save_file_name(self.v_input.text()[:-3]+'eps'), bbox_inches='tight', dpi=300)
        self.orbit_image_widget.fig.savefig(self.get_save_file_name(self.v_input.text()[:-3]+'pdf'), bbox_inches='tight', dpi=300)
        pickle.dump({'orbit':self.orbital_parameters, 'plot':self.plot_parameters}, open(self.get_save_file_name(self.v_input.text()[:-3]+'prm'), 'wb')) 
        msg = QMessageBox(self)
        msg.setText("Сохранение успешно!")
        msg.setWindowTitle("UMS - ВОР")
        msg.exec_()
    
    def get_save_file_name(self, name):
        if not path.isfile(name):
            return name
        else:
            i = 1
            while True:
                fname, ext = path.splitext(name)
                savename = fname+f'_{i}'+ext
                if not path.isfile(savename):
                    return savename

    def c_Load(self):
        fName = QFileDialog.getOpenFileName(self, 'Укажите файл настроек', self.last_path, "*.prm")[0]
        if fName:
            data = pickle.load(open(fName, 'rb'))
            self.PlotParams.loadParameters(data['plot'])
            self.OrbitParams.loadParameters(data['orbit'])
            self.c_Show()
    
    def closeEvent(self, evnt):
        self.orbit_image_widget.close()
        evnt.accept()