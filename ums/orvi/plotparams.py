from PySide2.QtWidgets import QComboBox, QWidget, QGridLayout, QLineEdit, QLabel, QWidget, QGridLayout, QPushButton, QFileDialog, QSpinBox, QRadioButton, QDoubleSpinBox, QSlider
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtCore import Qt, QPoint

from ums.common.widgets import QBorderedLabel, ErrorMessage


class PlotParams(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.__init_interface()
        self.__draw_interface()

    def __init_interface(self):
        self.b_Colored = QPushButton('Режим цвета')
        self.b_Colored.setCheckable(True)

        self.b_ODirect = QPushButton('Направление орбиты')
        self.b_ODirect.setCheckable(True)

        self.b_NDirect = QPushButton('Направление на N')
        self.b_NDirect.setCheckable(True)

        self.b_Brake_1 = QPushButton('Разрыв подграфика №1')
        self.b_Brake_1.setCheckable(True)

        self.b_Brake_2 = QPushButton('Разрыв подграфика №2')
        self.b_Brake_2.setCheckable(True)

        self.b_OrbitBox = QPushButton('Орбитальное решение')
        self.b_OrbitBox.setCheckable(True)

        self.b_SubMode = QPushButton('Residuals')
        self.b_SubMode.setCheckable(True)
        self.b_SubMode.clicked.connect(self.c_SubMode)

        self.v_brake_1_rate = QSlider(Qt.Horizontal)
        self.v_brake_1_rate.setRange(1, 9)
        self.v_brake_1_rate.setValue(5)
        self.v_brake_1_rate.setTickPosition(QSlider.TicksAbove)
        self.v_brake_2_rate = QSlider(Qt.Horizontal)
        self.v_brake_2_rate.setRange(1, 9)
        self.v_brake_2_rate.setValue(5)
        self.v_brake_2_rate.setTickPosition(QSlider.TicksAbove)

        self.b_OrbitOnly = QPushButton('Only orbit')
        self.b_OrbitOnly.setCheckable(True)
        self.b_OrbitOnly.clicked.connect(self.c_OrbitOnly)

        self.v_lim_x_min = QDoubleSpinBox()
        self.v_lim_x_min.setRange(-5000, 5000)
        self.v_lim_y_min = QDoubleSpinBox()
        self.v_lim_y_min.setRange(-5000, 5000)
        self.v_lim_x_max = QDoubleSpinBox()
        self.v_lim_x_max.setRange(-5000, 5000)
        self.v_lim_y_max = QDoubleSpinBox()
        self.v_lim_y_max.setRange(-5000, 5000)

        self.v_dir_x = QDoubleSpinBox()
        self.v_dir_x.setRange(-5000, 5000)
        self.v_dir_y = QDoubleSpinBox()
        self.v_dir_y.setRange(-5000, 5000)
        self.v_dir_dx = QDoubleSpinBox()
        self.v_dir_dx.setRange(-5000, 5000)
        self.v_dir_dy = QDoubleSpinBox()
        self.v_dir_dy.setRange(-5000, 5000)

        self.v_sub_1_lim_f = QDoubleSpinBox()
        self.v_sub_1_lim_f.setRange(-1000, 1000)
        self.v_sub_1_lim_t = QDoubleSpinBox()
        self.v_sub_1_lim_t.setRange(-1000, 1000)
        self.v_sub_1_lim_s = QDoubleSpinBox()
        self.v_sub_1_lim_s.setRange(0, 1000)
        self.v_sub_2_lim_f = QDoubleSpinBox()
        self.v_sub_2_lim_f.setRange(-1000, 1000)
        self.v_sub_2_lim_t = QDoubleSpinBox()
        self.v_sub_2_lim_t.setRange(-1000, 1000)
        self.v_sub_2_lim_s = QDoubleSpinBox()
        self.v_sub_2_lim_s.setRange(0, 1000)

        self.v_sub_1_brake_f = QDoubleSpinBox()
        self.v_sub_1_brake_f.setRange(-1000, 1000)
        self.v_sub_1_brake_t = QDoubleSpinBox()
        self.v_sub_1_brake_t.setRange(-1000, 1000)
        self.v_sub_1_brake_s = QDoubleSpinBox()
        self.v_sub_1_brake_s.setRange(0, 1000)
        self.v_sub_2_brake_f = QDoubleSpinBox()
        self.v_sub_2_brake_f.setRange(-1000, 1000)
        self.v_sub_2_brake_t = QDoubleSpinBox()
        self.v_sub_2_brake_t.setRange(-1000, 1000)
        self.v_sub_2_brake_s = QDoubleSpinBox()
        self.v_sub_2_brake_s.setRange(0, 1000)

        self.b_Brake_2.setEnabled(False)
        self.v_sub_2_brake_f.setEnabled(False)
        self.v_sub_2_brake_t.setEnabled(False)
        self.v_sub_2_brake_s.setEnabled(False)
        self.v_sub_2_lim_f.setEnabled(False)
        self.v_sub_2_lim_t.setEnabled(False)
        self.v_sub_2_lim_s.setEnabled(False)

        self.v_north_x = QDoubleSpinBox()
        self.v_north_x.setRange(-5000, 5000)
        self.v_north_y = QDoubleSpinBox()
        self.v_north_y.setRange(-5000, 5000)
        self.v_north_s = QDoubleSpinBox()
        self.v_north_s.setRange(0.1, 100)

        self.v_box_x = QDoubleSpinBox()
        self.v_box_x.setRange(-5000, 5000)
        self.v_box_y = QDoubleSpinBox()
        self.v_box_y.setRange(-5000, 5000)

        self.v_padding = QDoubleSpinBox()
        self.v_padding.setRange(-25, 50)

        self.v_Lang = QComboBox()
        self.v_Lang.addItems(['English', 'Russian'])

    def __draw_interface(self):
        self.main_layout = QGridLayout()

        i = 0; j = 0
        self.main_layout.addWidget(QBorderedLabel('Пределы графика'), i, 0, 1, 4)
        self.main_layout.addWidget(self.b_ODirect, i, 4, 1, 4)
        
        i += 1; j = 0
        self.main_layout.addWidget(QLabel('x (мин)'), i, 0)
        self.main_layout.addWidget(self.v_lim_x_min,  i, 1)
        self.main_layout.addWidget(QLabel('x (макс)'), i, 2)
        self.main_layout.addWidget(self.v_lim_x_max,   i, 3)

        self.main_layout.addWidget(QLabel('x'), i, 4)
        self.main_layout.addWidget(self.v_dir_x, i, 5)
        self.main_layout.addWidget(QLabel('\u0394x'), i, 6)
        self.main_layout.addWidget(self.v_dir_dx, i, 7)

        i += 1; j = 0
        self.main_layout.addWidget(QLabel('y (мин)'),  i, 0)
        self.main_layout.addWidget(self.v_lim_y_min,   i, 1)
        self.main_layout.addWidget(QLabel('y (макс)'), i, 2)
        self.main_layout.addWidget(self.v_lim_y_max,   i, 3)
        
        self.main_layout.addWidget(QLabel('y'),       i, 4)
        self.main_layout.addWidget(self.v_dir_y,      i, 5)
        self.main_layout.addWidget(QLabel('\u0394y'), i, 6)
        self.main_layout.addWidget(self.v_dir_dy,     i, 7)

        i += 1; j = 0
        self.main_layout.addWidget(QBorderedLabel('Пределы подграфика №1'), i, j, 1, 2); j+=2
        self.main_layout.addWidget(self.b_Brake_1, i, j, 1, 2); j+=2
        self.main_layout.addWidget(QBorderedLabel('Пределы подграфика №2'), i, j, 1, 2); j+=2
        self.main_layout.addWidget(self.b_Brake_2, i, j, 1, 2); j+=2 
        
        i += 1; j = 0
        self.main_layout.addWidget(self.v_brake_1_rate, i, j, 1, 4); j+=4
        self.main_layout.addWidget(self.v_brake_2_rate, i, j, 1, 4)

        i += 1; j = 0
        self.main_layout.addWidget(QLabel('От'),        i, j); j+=1
        self.main_layout.addWidget(self.v_sub_1_lim_f,  i, j); j+=1
        self.main_layout.addWidget(QLabel('От'),        i, j); j+=1
        self.main_layout.addWidget(self.v_sub_1_brake_f,i, j); j+=1
        self.main_layout.addWidget(QLabel('От'),        i, j); j+=1
        self.main_layout.addWidget(self.v_sub_2_lim_f,  i, j); j+=1
        self.main_layout.addWidget(QLabel('От'),        i, j); j+=1
        self.main_layout.addWidget(self.v_sub_2_brake_f,i, j); j+=1

        i += 1; j = 0
        self.main_layout.addWidget(QLabel('До'),        i, j); j+=1
        self.main_layout.addWidget(self.v_sub_1_lim_t,  i, j); j+=1
        self.main_layout.addWidget(QLabel('До'),        i, j); j+=1
        self.main_layout.addWidget(self.v_sub_1_brake_t,i, j); j+=1
        self.main_layout.addWidget(QLabel('До'),        i, j); j+=1
        self.main_layout.addWidget(self.v_sub_2_lim_t,  i, j); j+=1
        self.main_layout.addWidget(QLabel('До'),        i, j); j+=1
        self.main_layout.addWidget(self.v_sub_2_brake_t,i, j); j+=1

        i += 1; j = 0
        self.main_layout.addWidget(QLabel('Шаг'),       i, j); j+=1
        self.main_layout.addWidget(self.v_sub_1_lim_s,  i, j); j+=1
        self.main_layout.addWidget(QLabel('Шаг'),       i, j); j+=1
        self.main_layout.addWidget(self.v_sub_1_brake_s,i, j); j+=1
        self.main_layout.addWidget(QLabel('Шаг'),       i, j); j+=1
        self.main_layout.addWidget(self.v_sub_2_lim_s,  i, j); j+=1
        self.main_layout.addWidget(QLabel('Шаг'),       i, j); j+=1
        self.main_layout.addWidget(self.v_sub_2_brake_s,i, j); j+=1
        
        i += 1; j = 0
        self.main_layout.addWidget(self.b_NDirect,  i, j, 1, 2); j+=2
        self.main_layout.addWidget(self.b_OrbitBox, i, j, 1, 2); j+=2
        self.main_layout.addWidget(QBorderedLabel('Прочие настройки'), i, j, 1, 4); j+=4

        i += 1; j = 0
        self.main_layout.addWidget(QLabel('x'),    i, j); j+=1
        self.main_layout.addWidget(self.v_north_x,       i, j); j+=1
        self.main_layout.addWidget(QLabel('x'),    i, j); j+=1
        self.main_layout.addWidget(self.v_box_x,       i, j); j+=1
        self.main_layout.addWidget(QLabel('Отступ'), i, j, Qt.AlignCenter); j+=1
        self.main_layout.addWidget(self.v_padding,     i, j); j+=1
        self.main_layout.addWidget(self.b_OrbitOnly, i, j, 1, 2); j+=2
        
        i += 1; j = 0
        self.main_layout.addWidget(QLabel('y'),    i, j); j+=1
        self.main_layout.addWidget(self.v_north_y,       i, j); j+=1
        self.main_layout.addWidget(QLabel('y'),    i, j); j+=1
        self.main_layout.addWidget(self.v_box_y,       i, j); j+=1
        self.main_layout.addWidget(QLabel('Язык'), i, j, Qt.AlignCenter); j+=1
        self.main_layout.addWidget(self.v_Lang, i, j); j+=1
        self.main_layout.addWidget(self.b_SubMode, i, j, 1, 2); j+=2
        
        i += 1; j = 0
        self.main_layout.addWidget(QLabel('Размер'),     i, j); j+=1
        self.main_layout.addWidget(self.v_north_s,       i, j); j+=5
        self.main_layout.addWidget(self.b_Colored, i, j, 1, 2); j+=2
        
        self.setLayout(self.main_layout)
        
    def clear_all(self):
        self.b_Colored.setChecked(False)
        self.b_ODirect.setChecked(False)
        self.b_NDirect.setChecked(False)
        self.b_Brake_1.setChecked(False)
        self.b_Brake_2.setChecked(False)
        self.b_OrbitBox.setChecked(False)
        self.b_SubMode.setChecked(False)
        self.c_SubMode()

        self.v_lim_x_min.setValue(0)
        self.v_lim_y_min.setValue(0)
        self.v_lim_x_max.setValue(0)
        self.v_lim_y_max.setValue(0)

        self.v_dir_x.setValue(0)
        self.v_dir_y.setValue(0)  
        self.v_dir_dx.setValue(0)
        self.v_dir_dy.setValue(0)

        self.v_sub_1_lim_f.setValue(0)
        self.v_sub_1_lim_t.setValue(0)
        self.v_sub_1_lim_s.setValue(0)
        self.v_sub_2_lim_f.setValue(0)
        self.v_sub_2_lim_t.setValue(0)
        self.v_sub_2_lim_s.setValue(0)

        self.v_sub_1_brake_f.setValue(0)
        self.v_sub_1_brake_t.setValue(0)
        self.v_sub_1_brake_s.setValue(0)
        self.v_sub_2_brake_f.setValue(0)
        self.v_sub_2_brake_t.setValue(0)
        self.v_sub_2_brake_s.setValue(0)

        self.v_north_x.setValue(0)
        self.v_north_y.setValue(0)
        self.v_north_s.setValue(0)

        self.v_box_x.setValue(0)
        self.v_box_y.setValue(0)
        self.v_padding.setValue(0)

    def c_OrbitOnly(self):
        pass
    
    def c_SubMode(self):
        if self.b_SubMode.isChecked():
            self.b_SubMode.setText('Errors(\u03B8 && \u03C1)')
            self.v_sub_2_brake_f.setEnabled(True)
            self.v_sub_2_brake_t.setEnabled(True)
            self.v_sub_2_brake_s.setEnabled(True)
            self.v_sub_2_lim_f.setEnabled(True)
            self.v_sub_2_lim_t.setEnabled(True)
            self.v_sub_2_lim_s.setEnabled(True)
            self.b_Brake_2.setEnabled(True)
        else:
            self.b_SubMode.setText('Residuals')
            self.v_sub_2_brake_f.setEnabled(False)
            self.v_sub_2_brake_t.setEnabled(False)
            self.v_sub_2_brake_s.setEnabled(False)
            self.v_sub_2_lim_f.setEnabled(False)
            self.v_sub_2_lim_t.setEnabled(False)
            self.v_sub_2_lim_s.setEnabled(False)
            self.b_Brake_2.setEnabled(False)

    def loadParameters(self, prm):
        self.b_ODirect.setChecked(prm['ODirect'])
        self.b_NDirect.setChecked(prm['NDirect'])
        self.b_Brake_1.setChecked(prm['Brake_1'])
        self.b_Brake_2.setChecked(prm['Brake_2'])
        self.b_OrbitBox.setChecked(prm['OrbitBox'])
        self.b_Colored.setChecked(True if prm['color2']=='red' else False)
        self.v_Lang.setCurrentIndex(0 if prm['year'] == 'y' else 1)
        if isinstance(prm['SubMode'], str):
            if prm['SubMode'] == 'residuals':
                self.b_SubMode.setChecked(False)
                self.c_SubMode()
            elif prm['SubMode'] == 'errors':
                self.b_SubMode.setChecked(True)
                self.c_SubMode()
            else:
                ErrorMessage('Unknown value of subgraph mode. Skip')
        elif isinstance(prm['SubMode'], bool):
            self.b_SubMode.setChecked(prm['SubMode'])
            self.c_SubMode()

        self.v_lim_x_min.setValue(prm['lim_x_min'])
        self.v_lim_y_min.setValue(prm['lim_y_min'])
        self.v_lim_x_max.setValue(prm['lim_x_max'])
        self.v_lim_y_max.setValue(prm['lim_y_max'])

        self.v_dir_x.setValue(prm['dir_x'])
        self.v_dir_dx.setValue(prm['dir_dx'])
        self.v_dir_y.setValue(prm['dir_y'])
        self.v_dir_dy.setValue(prm['dir_dy'])
        
        self.v_sub_1_lim_f.setValue(prm['sub_1_lim_f'])  
        self.v_sub_1_lim_t.setValue(prm['sub_1_lim_t'])  
        self.v_sub_1_lim_s.setValue(prm['sub_1_lim_s'])
        self.v_sub_2_lim_f.setValue(prm['sub_2_lim_f'])  
        self.v_sub_2_lim_t.setValue(prm['sub_2_lim_t'])  
        self.v_sub_2_lim_s.setValue(prm['sub_2_lim_s'])

        self.v_sub_1_brake_f.setValue(prm['sub_1_brake_f'])
        self.v_sub_1_brake_t.setValue(prm['sub_1_brake_t'])
        self.v_sub_1_brake_s.setValue(prm['sub_1_brake_s'])
        self.v_sub_2_brake_f.setValue(prm['sub_2_brake_f'])
        self.v_sub_2_brake_t.setValue(prm['sub_2_brake_t'])
        self.v_sub_2_brake_s.setValue(prm['sub_2_brake_s'])

        self.v_north_x.setValue(prm['north_x'])
        self.v_north_y.setValue(prm['north_y'])
        self.v_north_s.setValue(prm['north_s'])

        self.v_box_x.setValue(prm['box_x'])
        self.v_box_y.setValue(prm['box_y'])

        self.v_padding.setValue(prm['padding'])

    def collectParams(self):
        return {
            'epoch' : "Эпоха" if self.v_Lang.currentText() == 'Russian' else 'Epoch',
            'arcsec' : "мсд" if self.v_Lang.currentText() == 'Russian' else 'mas',
            'year' : "г" if self.v_Lang.currentText() == 'Russian' else 'y',

            'ODirect' : self.b_ODirect.isChecked(),
            'NDirect' : self.b_NDirect.isChecked(),
            'Brake_1' : self.b_Brake_1.isChecked(),
            'Brake_2' : self.b_Brake_2.isChecked(),
            'OrbitBox' : self.b_OrbitBox.isChecked(),
            'SubMode'   : 'errors' if self.b_SubMode.isChecked() else 'residuals',
            'OrbitOnly' : self.b_OrbitOnly.isChecked(),
            
            'color1'    :   'black',
            'color2'    :   'red' if self.b_Colored.isChecked() else 'gray',

            'lim_x_min' :   self.v_lim_x_min.value(),
            'lim_y_min' :   self.v_lim_y_min.value(),
            'lim_x_max' :   self.v_lim_x_max.value(),
            'lim_y_max' :   self.v_lim_y_max.value(),

            'dir_x'     :   self.v_dir_x.value(),
            'dir_dx'    :   self.v_dir_dx.value(),
            'dir_y'     :   self.v_dir_y.value(),
            'dir_dy'    :   self.v_dir_dy.value(),

            'sub_1_lim_f'   :   self.v_sub_1_lim_f.value(),  
            'sub_1_lim_t'   :   self.v_sub_1_lim_t.value(),  
            'sub_1_lim_s'   :   self.v_sub_1_lim_s.value(),
            'sub_2_lim_f'   :   self.v_sub_2_lim_f.value(),  
            'sub_2_lim_t'   :   self.v_sub_2_lim_t.value(),  
            'sub_2_lim_s'   :   self.v_sub_2_lim_s.value(),

            'sub_1_brake_f' :   self.v_sub_1_brake_f.value(),
            'sub_1_brake_t' :   self.v_sub_1_brake_t.value(),
            'sub_1_brake_s' :   self.v_sub_1_brake_s.value(),
            'sub_2_brake_f' :   self.v_sub_2_brake_f.value(),
            'sub_2_brake_t' :   self.v_sub_2_brake_t.value(),
            'sub_2_brake_s' :   self.v_sub_2_brake_s.value(),

            'sub_1_brake_rate' :   self.v_brake_1_rate.value(),
            'sub_2_brake_rate' :   self.v_brake_2_rate.value(),

            'north_x'       :   self.v_north_x.value(),
            'north_y'       :   self.v_north_y.value(),
            'north_s'       :   self.v_north_s.value(),

            'box_x'         :   self.v_box_x.value(),
            'box_y'         :   self.v_box_y.value(),

            'padding'       :   self.v_padding.value(),
        }

