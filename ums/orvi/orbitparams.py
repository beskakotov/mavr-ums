from PySide2.QtWidgets import QGraphicsItem, QWidget, QGridLayout, QLineEdit, QLabel, QWidget, QGridLayout, QPushButton, \
    QFileDialog, QSpinBox, QRadioButton
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtCore import Qt, QPoint

from numpy import fromiter

from ums.orvi.services import get_orbit, get_points, OrbitalSolution
from ums.common.functions import is_numeric


class OrbitParams(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.__init_interface()
        self.__draw_interface()

    def __init_interface(self):
        self.l_name = QLabel('Name')
        self.l_name.setAlignment(Qt.AlignCenter)
        self.v_name = QLineEdit()

        self.l_P = QLabel('P')
        self.l_P.setAlignment(Qt.AlignCenter)
        self.v_P = QLineEdit()

        self.l_T0 = QLabel('T0')
        self.l_T0.setAlignment(Qt.AlignCenter)
        self.v_T0 = QLineEdit()

        self.l_e = QLabel('e')
        self.l_e.setAlignment(Qt.AlignCenter)
        self.v_e = QLineEdit()

        self.l_a = QLabel('a')
        self.l_a.setAlignment(Qt.AlignCenter)
        self.v_a = QLineEdit()

        self.l_W = QLabel('\u03A9')
        self.l_W.setAlignment(Qt.AlignCenter)
        self.v_W = QLineEdit()

        self.l_w = QLabel('\u03C9')
        self.l_w.setAlignment(Qt.AlignCenter)
        self.v_w = QLineEdit()

        self.l_i = QLabel('i')
        self.l_i.setAlignment(Qt.AlignCenter)
        self.v_i = QLineEdit()

        self.lit_l = QLabel('Орбита сравнения')
        self.lit_l.setAlignment(Qt.AlignCenter)

        self.lit_v_P = QLineEdit()
        self.lit_v_T0 = QLineEdit()
        self.lit_v_e = QLineEdit()
        self.lit_v_a = QLineEdit()
        self.lit_v_W = QLineEdit()
        self.lit_v_w = QLineEdit()
        self.lit_v_i = QLineEdit()

    def __draw_interface(self):
        self.main_layout = QGridLayout()

        i = 0
        self.main_layout.addWidget(self.l_name, i, 0)
        self.main_layout.addWidget(self.l_P, i, 1)
        self.main_layout.addWidget(self.l_T0, i, 2)
        self.main_layout.addWidget(self.l_e, i, 3)
        self.main_layout.addWidget(self.l_a, i, 4)
        self.main_layout.addWidget(self.l_W, i, 5)
        self.main_layout.addWidget(self.l_w, i, 6)
        self.main_layout.addWidget(self.l_i, i, 7)

        i += 1
        self.main_layout.addWidget(self.v_name, i, 0)
        self.main_layout.addWidget(self.v_P, i, 1)
        self.main_layout.addWidget(self.v_T0, i, 2)
        self.main_layout.addWidget(self.v_e, i, 3)
        self.main_layout.addWidget(self.v_a, i, 4)
        self.main_layout.addWidget(self.v_W, i, 5)
        self.main_layout.addWidget(self.v_w, i, 6)
        self.main_layout.addWidget(self.v_i, i, 7)

        i += 1
        self.main_layout.addWidget(self.lit_l, i, 0)
        self.main_layout.addWidget(self.lit_v_P, i, 1)
        self.main_layout.addWidget(self.lit_v_T0, i, 2)
        self.main_layout.addWidget(self.lit_v_e, i, 3)
        self.main_layout.addWidget(self.lit_v_a, i, 4)
        self.main_layout.addWidget(self.lit_v_W, i, 5)
        self.main_layout.addWidget(self.lit_v_w, i, 6)
        self.main_layout.addWidget(self.lit_v_i, i, 7)

        self.setLayout(self.main_layout)

    def clear_all(self):
        self.clear_main_orbit()
        self.clear_lit_orbit()

    def clear_main_orbit(self):
        self.v_name.setText("")
        self.v_P.setText("")
        self.v_T0.setText("")
        self.v_e.setText("")
        self.v_a.setText("")
        self.v_W.setText("")
        self.v_w.setText("")
        self.v_i.setText("")

    def clear_lit_orbit(self):
        self.lit_v_P.setText("")
        self.lit_v_T0.setText("")
        self.lit_v_e.setText("")
        self.lit_v_a.setText("")
        self.lit_v_W.setText("")
        self.lit_v_w.setText("")
        self.lit_v_i.setText("")

    def loadParameters(self, prm):
        self.v_name.setText(prm['name'])
        self.v_P.setText(prm['P'])
        self.v_T0.setText(prm['T0'])
        self.v_e.setText(prm['e'])
        self.v_a.setText(prm['a'])
        self.v_W.setText(prm['W'])
        self.v_w.setText(prm['w'])
        self.v_i.setText(prm['i'])
        if prm['litplot']:
            self.lit_v_P.setText(prm['lit_P'])
            self.lit_v_T0.setText(prm['lit_T0'])
            self.lit_v_a.setText(prm['lit_a'])
            self.lit_v_e.setText(prm['lit_e'])
            self.lit_v_W.setText(prm['lit_W'])
            self.lit_v_w.setText(prm['lit_w'])
            self.lit_v_i.setText(prm['lit_i'])

    def collectParams(self, i_path, o_path, from_interface=False):
        orbital_solution = OrbitalSolution()
        literature_orbital_solution = None
        if not i_path or not o_path:
            return 0

        with open(o_path) as f:
            data = f.read().split('\n')
            adata = data[:13]
            bdata = data[15:]
        first_time_plot = not bool(self.v_name.text())
        for line in adata:
            if not line or line.startswith('#'):
                continue
            b = line.split()
            if b[0] == 'Object:':
                orbital_solution.set_info('name', ' '.join(b[1:]))
            elif b[0] == 'RA:':
                orbital_solution.set_info('RA', 15 * float(b[1]))
            elif b[0] == 'Dec:':
                orbital_solution.set_info('DEC', float(b[1]))
            elif b[0] == 'P':
                o_P = [b[1], b[2]]
            elif b[0] == 'T0':
                o_T0 = [b[1], b[2]]
            elif b[0] == 'e':
                o_e = [b[1], b[2]]
            elif b[0] == 'a':
                o_a = [b[1], b[2]]
            elif b[0] == 'W':
                o_W = [b[1], b[2]]
            elif b[0] == 'w':
                o_w = [b[1], b[2]]
            elif b[0] == 'i':
                o_i = [b[1], b[2]]

        if first_time_plot:
            self.v_name.setText(orbital_solution.NAME)
            self.v_P.setText(f'{o_P[0]}|{o_P[1]}')
            self.v_T0.setText(f'{o_T0[0]}|{o_T0[1]}')
            self.v_a.setText(f'{o_a[0]}|{o_a[1]}')
            self.v_e.setText(f'{o_e[0]}|{o_e[1]}')
            self.v_W.setText(f'{o_W[0]}|{o_W[1]}')
            self.v_w.setText(f'{o_w[0]}|{o_w[1]}')
            self.v_i.setText(f'{o_i[0]}|{o_i[1]}')

        if from_interface:
            o_P[0] = float(self.v_P.text().split('|')[0])
            o_T0[0] = float(self.v_T0.text().split('|')[0])
            o_e[0] = float(self.v_e.text().split('|')[0])
            o_a[0] = float(self.v_a.text().split('|')[0])
            o_W[0] = float(self.v_W.text().split('|')[0])
            o_w[0] = float(self.v_w.text().split('|')[0])
            o_i[0] = float(self.v_i.text().split('|')[0])

            o_P[1] = float(self.v_P.text().split('|')[1])
            o_T0[1] = float(self.v_T0.text().split('|')[1])
            o_e[1] = float(self.v_e.text().split('|')[1])
            o_a[1] = float(self.v_a.text().split('|')[1])
            o_W[1] = float(self.v_W.text().split('|')[1])
            o_w[1] = float(self.v_w.text().split('|')[1])
            o_i[1] = float(self.v_i.text().split('|')[1])
        
        libPoints = []
        newPoints = []
        badPoints = []

        line_number = 0
        for line_number, line in enumerate(bdata):
            if not line:
                continue
            if line.split()[-1].endswith('_NP'):
                newPoints.append(line_number)
            elif line.split()[-1].endswith('_BP'):
                badPoints.append(line_number)
            else:
                libPoints.append(line_number)
        orbital_solution.set_parameters_with_errors(
            *map(float, o_P),
            *map(float, o_T0),
            *map(float, o_a),
            *map(float, o_e),
            *map(float, o_W),
            *map(float, o_w),
            *map(float, o_i)
        )

        all_lit_orbit_params = (
            self.lit_v_P.text(),
            self.lit_v_T0.text(),
            self.lit_v_a.text(),
            self.lit_v_e.text(),
            self.lit_v_W.text(),
            self.lit_v_w.text(),
            self.lit_v_i.text()
        )

        if all(all_lit_orbit_params) and all(fromiter(map(is_numeric, all_lit_orbit_params), bool)):
            literature_orbital_solution = OrbitalSolution()
            literature_orbital_solution.set_parameters(
                *map(float, (
                    self.lit_v_P.text(),
                    self.lit_v_T0.text(),
                    self.lit_v_a.text(),
                    self.lit_v_e.text(),
                    self.lit_v_W.text(),
                    self.lit_v_w.text(),
                    self.lit_v_i.text()
                ))
            )

        position_list = get_points(i_path, orbital_solution)
        model, bind, x, y = get_orbit(position_list, orbital_solution)

        if literature_orbital_solution:
            literature_position_list = get_points(i_path, literature_orbital_solution)
            literature_model, literature_bind, literature_x, literature_y = get_orbit(literature_position_list, literature_orbital_solution)

        orbit_params = {
            'orbital_solution': orbital_solution,
            'literature_orbital_solution': literature_orbital_solution,
            'position_list': position_list,
            'model': model,
            'bind': bind,
            'x': x,
            'y': y,
            'libPoints': libPoints,
            'newPoints': newPoints,
            'badPoints': badPoints,
            'first_time_plot': first_time_plot,
        }

        if literature_orbital_solution:
            orbit_params['literature_position_list'] = literature_position_list
            orbit_params['literature_model'] = literature_model
            orbit_params['literature_bind'] = literature_bind
            orbit_params['literature_x'] = literature_x
            orbit_params['literature_y'] = literature_y

        return orbit_params
