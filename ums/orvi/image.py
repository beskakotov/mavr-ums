from PySide2.QtCore import Qt, QPoint
from PySide2.QtWidgets import QWidget, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import fromiter, arange

from ums.orvi.services import create_axis, calculate_residuals, get_tick_positions_for_epochs


class OrbitImage(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, None)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.parent_widget = parent
        self.setFixedSize(600, 800)
        self.setStyleSheet('background-color: #aaa')
        self.press = None
        self.__init_interface()
        self.__draw_interface()

    def __init_interface(self):
        self.fig = Figure()
        self.fig.subplots_adjust(left=0.1, bottom=0.08, right=0.95, top=0.98, wspace=0.5, hspace=0.5)
        self.img = FigureCanvas(self.fig)
        self.fig.add_subplot(111)

    def __draw_interface(self):
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.img)
        self.setLayout(self.main_layout)

    def plot(self, orbit_params, plot_params):
        self.fig.clear()
        if plot_params['OrbitOnly']:
            self._setup_plot_orbit_only(plot_params)
        else:
            if plot_params['SubMode'] == 'errors' or plot_params['SubMode'] == True:
                self._setup_plot_rhos_and_thetas(plot_params)

            elif plot_params['SubMode'] == 'residuals' or plot_params['SubMode'] == False:
                self._setup_plot_residuals(plot_params)
                self._plot_residuals(orbit_params, plot_params)

        self.cidpress = self.img.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.img.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.img.mpl_connect('motion_notify_event', self.on_motion)
        self.cidmotion = self.img.mpl_connect('scroll_event', self.on_resize)

        self._plot_orbit(orbit_params, plot_params)
        if orbit_params['literature_orbital_solution']:
            self._plot_literature_orbit(orbit_params, plot_params)

        if plot_params['OrbitBox']:
            self._plot_orbit_box(orbit_params, plot_params)

        if not orbit_params['first_time_plot']:
            self._set_limits_orbit_plot(plot_params)

        self.parent_widget.PlotParams.v_lim_x_min.setValue(self.ax_orbit.get_xlim()[0])
        self.parent_widget.PlotParams.v_lim_x_max.setValue(self.ax_orbit.get_xlim()[1])
        self.parent_widget.PlotParams.v_lim_y_min.setValue(self.ax_orbit.get_ylim()[0])
        self.parent_widget.PlotParams.v_lim_y_max.setValue(self.ax_orbit.get_ylim()[1])

        if plot_params['NDirect']:
            self._plot_north_direction(plot_params)

        if plot_params['ODirect']:
            self._plot_orbit_direction(plot_params)

        ##########################
        # main algorithm
        ##########################

        self.img.draw()

    def _setup_plot_orbit_only(self, plot_params):
        self.setFixedSize(600, 600)
        self.ax_orbit = create_axis(
            self.fig.add_subplot(111),
            plot_params,
        )

    def _setup_plot_residuals(self, plot_params):
        self.setFixedSize(600, 600 + 25 + 60 + 60)
        gridspec = self.fig.add_gridspec(5, 2,
            width_ratios=(8, 2), height_ratios=(600, 25, 60, 5, 60),
            left=0.1, right=0.95, bottom=0.05, top=0.95,
            wspace=0, hspace=0)

        self.ax_orbit = create_axis(
            self.fig.add_subplot(gridspec[0, :]),
            plot_params
        )
        if plot_params['Brake_1']:
            self.ax_residuals_2 = create_axis(
                self.fig.add_subplot(gridspec[2, 0]),
                plot_params,
                axis_type='residuals',
                bottom=False,
            )
            self.ax_residuals_1 = create_axis(
                self.fig.add_subplot(gridspec[4, 0]),
                plot_params,
                axis_type='residuals',
                top=False,
            )
            self.ax_box_2 = create_axis(
                self.fig.add_subplot(gridspec[2, 1]),
                plot_params,
                axis_type='box',
                bottom=False
            )
            self.ax_box_1 = create_axis(
                self.fig.add_subplot(gridspec[4, 1]),
                plot_params,
                axis_type='box',
                top=False,
            )
        else:
            self.ax_residuals_1 = create_axis(
                self.fig.add_subplot(gridspec[2:, 0]),
                plot_params,
                axis_type='residuals'
            )
            self.ax_box_1 = create_axis(
                self.fig.add_subplot(gridspec[2:, 1]),
                plot_params,
                axis_type='box'
            )

        

    def _setup_plot_rhos_and_thetas(self, plot_params):
        self.setFixedSize(600, 600 + 25 + 60 + 60 + 60 + 60)
        gridspec = self.fig.add_gridspec(8, 2,
                                         width_ratios=(8, 2), height_ratios=(600, 25, 60, 5, 60, 60, 5, 60),
                                         left=0.1, right=0.95, bottom=0.05, top=0.95,
                                         wspace=0.2, hspace=0)

        self.ax_orbit = create_axis(
            self.fig.add_subplot(gridspec[0, :]),
            plot_params
        )

        if plot_params['Brake_1']:
            self.ax_rho_1 = create_axis(
                self.fig.add_subplot(gridspec[2, 0]),
                plot_params,
                axis_type='errors',
                bottom=False,
            )
            self.ax_rho_2 = create_axis(
                self.fig.add_subplot(gridspec[4, 0]),
                plot_params,
                axis_type='errors',
                top=False,
            )
        else:
            self.ax_rho_1 = create_axis(
                self.fig.add_subplot(gridspec[2:5, 0]),
                plot_params,
                axis_type='errors'
            )

        if plot_params['Brake_2']:
            self.ax_theta_1 = create_axis(
                self.fig.add_subplot(gridspec[5, 0]),
                plot_params,
                axis_type='errors',
                bottom=False,
            )
            self.ax_theta_2 = create_axis(
                self.fig.add_subplot(gridspec[7, 0]),
                plot_params,
                axis_type='errors',
                top=False,
            )
        else:
            self.ax_theta_1 = create_axis(
                self.fig.add_subplot(gridspec[5:, 0]),
                plot_params,
                axis_type='errors'
            )

        self.ax_box_1 = create_axis(
            self.fig.add_subplot(gridspec[2:5, 1]),
            plot_params,
            axis_type='box'
        )

        self.ax_box_2 = create_axis(
            self.fig.add_subplot(gridspec[5:, 1]),
            plot_params,
            axis_type='box'
        )


        return

        # === Calculate residuals
        # with open(self.parent_widget.v_output.text()) as f:
        #     raw = f.read().split('\n')
        # data = array([])
        # theta = array([])
        # rho = array([])
        # fastcalc = lambda rho, drho, dtheta: sqrt(
        #     rho ** 2 + (rho + drho) ** 2 - 2 * rho * (rho + drho) * cos(deg2rad(dtheta)))
        # for line in raw[15:]:
        #     if not line or line.startswith('#'): continue
        #     data = append(data, float(line.split()[0]))
        #     theta = append(theta, float(line.split()[3]))
        #     rho = append(rho, float(line.split()[4]))
        # dtheta = theta[:]
        # drho = rho[:]
        # rho = orbit_params['position_list'][:, 2]
        # resultdata = []
        # calcdata = array([rho, drho, dtheta]).T
        # for i, j, k in calcdata:
        #     resultdata.append(fastcalc(i, j, k))
        # resultdata = array(resultdata)

        # === Calculate ticks for residuals plots
        # if data.max() - data.min() > 2:
        #     epochs_ticks = unique(linspace(floor(data.min()), ceil(data.max()), 6, dtype='uint16'))
        # else:
        #     step = 0
        #     while True:
        #         step += 0.1
        #         if step > data.max() - data.min():
        #             exit()
        #         epochs_ticks = arange(floor((data.min() - 0.05) * 10) / 10,
        #                               ceil((data.max() + 0.05) * 10) / 10 + step / 2, step)
        #         if epochs_ticks.min() < data.min() and epochs_ticks.max() > data.max() and epochs_ticks.size <= 7:
        #             break
        # if plot_params['SubMode']:
        #     ax3.plot(data[0], drho[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
        #     ax3.plot(data[orbit_params['newPoints']], drho[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
        #     ax3.plot(data[orbit_params['badPoints']], drho[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
        #     ax3.plot(data[orbit_params['libPoints']], drho[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
        #     ax3.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
        #     ax3.set_ylabel('$\u0394\u03C1$, {}'.format(plot_params['arcsec']), labelpad=plot_params['padding'])
        #     # ax3.xaxis.set_ticks(epochs_ticks)
        #     ax3.xaxis.set_ticks(epochs_ticks)
        #     ax3.set_xticklabels(['']*len(epochs_ticks))
        #
        #     ax5.plot(data[0], dtheta[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
        #     ax5.plot(data[orbit_params['newPoints']], dtheta[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
        #     ax5.plot(data[orbit_params['badPoints']], dtheta[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
        #     ax5.plot(data[orbit_params['libPoints']], dtheta[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
        #     ax5.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
        #     ax5.set_xlabel(plot_params['epoch'])
        #     ax5.set_ylabel('$\u0394\u03B8$, \u00B0', labelpad=plot_params['padding'])
        #     ax5.xaxis.set_ticks(epochs_ticks)
        #
        #     ax7.boxplot(drho, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
        #     ax7.get_xaxis().set_visible(False)
        #
        #     ax9.boxplot(dtheta, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
        #     ax9.get_xaxis().set_visible(False)
        #
        #     if plot_params['sub_1_lim_s'] > 0:
        #         ax3.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
        #         ax7.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
        #         ax3.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])
        #         ax7.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])
        #
        #     if plot_params['sub_2_lim_s'] > 0:
        #         ax5.yaxis.set_ticks(arange(plot_params['sub_2_lim_f'], plot_params['sub_2_lim_t']+1, plot_params['sub_2_lim_s']))
        #         ax9.yaxis.set_ticks(arange(plot_params['sub_2_lim_f'], plot_params['sub_2_lim_t']+1, plot_params['sub_2_lim_s']))
        #         ax5.set_ylim(plot_params['sub_2_lim_f'] - plot_params['sub_2_lim_s'], plot_params['sub_2_lim_t'] + plot_params['sub_2_lim_s'])
        #         ax9.set_ylim(plot_params['sub_2_lim_f'] - plot_params['sub_2_lim_s'], plot_params['sub_2_lim_t'] + plot_params['sub_2_lim_s'])
        #
        #     if plot_params['Brake_1']:
        #         ax2.plot(data[0], drho[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
        #         ax2.plot(data[orbit_params['newPoints']], drho[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
        #         ax2.plot(data[orbit_params['badPoints']], drho[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
        #         ax2.plot(data[orbit_params['libPoints']], drho[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
        #         ax2.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
        #         ax2.xaxis.set_ticks(epochs_ticks)
        #         ax2.set_xticklabels(['']*len(epochs_ticks))
        #
        #         ax3.set_ylabel('$\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \u0394\u03C1$, {}'.format(plot_params['arcsec']), labelpad=plot_params['padding'])
        #         ax6.boxplot(drho, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
        #         ax6.get_xaxis().set_visible(False)
        #
        #         if plot_params['sub_1_brake_s'] > 0 and plot_params['sub_1_lim_s'] > 0:
        #             ax2.yaxis.set_ticks(arange(plot_params['sub_1_brake_t'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_brake_s']))
        #             ax6.yaxis.set_ticks(arange(plot_params['sub_1_brake_t'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_brake_s']))
        #             ax2.set_ylim(plot_params['sub_1_brake_t'] - plot_params['sub_1_brake_s']/2, plot_params['sub_1_lim_t'] + plot_params['sub_1_brake_s']/2)
        #             ax6.set_ylim(plot_params['sub_1_brake_t'] - plot_params['sub_1_brake_s']/2, plot_params['sub_1_lim_t'] + plot_params['sub_1_brake_s']/2)
        #             ax3.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_brake_f']+1, plot_params['sub_1_lim_s']))
        #             ax7.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_brake_f']+1, plot_params['sub_1_lim_s']))
        #             ax3.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s']/2, plot_params['sub_1_brake_f'] + plot_params['sub_1_lim_s']/2)
        #             ax7.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s']/2, plot_params['sub_1_brake_f'] + plot_params['sub_1_lim_s']/2)
        #
        #     if plot_params['Brake_2']:
        #         ax4.plot(data[0], dtheta[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
        #         ax4.plot(data[orbit_params['newPoints']], dtheta[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
        #         ax4.plot(data[orbit_params['badPoints']], dtheta[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
        #         ax4.plot(data[orbit_params['libPoints']], dtheta[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
        #         ax4.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
        #         ax4.xaxis.set_ticks(epochs_ticks)
        #         ax4.set_xticklabels(['']*len(epochs_ticks))
        #
        #         ax5.set_ylabel('$\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \u0394\u03B8$, \u00B0'.format(plot_params['arcsec']), labelpad=plot_params['padding'])
        #         ax8.boxplot(dtheta, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
        #         ax8.get_xaxis().set_visible(False)
        #
        #         if plot_params['sub_2_brake_s'] > 0 and plot_params['sub_2_lim_s'] > 0:
        #             ax4.yaxis.set_ticks(arange(plot_params['sub_2_brake_t'], plot_params['sub_2_lim_t']+1, plot_params['sub_2_brake_s']))
        #             ax8.yaxis.set_ticks(arange(plot_params['sub_2_brake_t'], plot_params['sub_2_lim_t']+1, plot_params['sub_2_brake_s']))
        #             ax4.set_ylim(plot_params['sub_2_brake_t'] - plot_params['sub_2_brake_s']/2, plot_params['sub_2_lim_t'] + plot_params['sub_2_brake_s']/2)
        #             ax8.set_ylim(plot_params['sub_2_brake_t'] - plot_params['sub_2_brake_s']/2, plot_params['sub_2_lim_t'] + plot_params['sub_2_brake_s']/2)
        #             ax5.yaxis.set_ticks(arange(plot_params['sub_2_lim_f'], plot_params['sub_2_brake_f']+1, plot_params['sub_2_lim_s']))
        #             ax9.yaxis.set_ticks(arange(plot_params['sub_2_lim_f'], plot_params['sub_2_brake_f']+1, plot_params['sub_2_lim_s']))
        #             ax5.set_ylim(plot_params['sub_2_lim_f'] - plot_params['sub_2_lim_s']/2, plot_params['sub_2_brake_f'] + plot_params['sub_2_lim_s']/2)
        #             ax9.set_ylim(plot_params['sub_2_lim_f'] - plot_params['sub_2_lim_s']/2, plot_params['sub_2_brake_f'] + plot_params['sub_2_lim_s']/2)
        #
        # else:
        #     ax3.set_ylabel('$\u0394$, {}'.format(plot_params['arcsec'], labelpad=plot_params['padding']))  # Delta
        #     ax3.plot(data[0], resultdata[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
        #     ax3.plot(data[orbit_params['newPoints']], resultdata[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
        #     ax3.plot(data[orbit_params['badPoints']], resultdata[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
        #     ax3.plot(data[orbit_params['libPoints']], resultdata[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
        #     ax3.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
        #     ax3.set_xlabel(plot_params['epoch'])
        #     ax3.xaxis.set_ticks(epochs_ticks)
        #
        #     ax7.boxplot(resultdata, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
        #     ax7.get_xaxis().set_visible(False)
        #
        #     if plot_params['sub_1_lim_s'] > 0:
        #         ax3.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
        #         ax7.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
        #         ax3.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])
        #         ax7.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])
        #
        #     if plot_params['Brake_1']:
        #         ax2.plot(data[0], resultdata[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
        #         ax2.plot(data[orbit_params['newPoints']], resultdata[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
        #         ax2.plot(data[orbit_params['badPoints']], resultdata[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
        #         ax2.plot(data[orbit_params['libPoints']], resultdata[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
        #         ax2.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
        #         ax2.xaxis.set_ticks(epochs_ticks)
        #         ax2.set_xticklabels(['']*len(epochs_ticks))
        #
        #         ax6.boxplot(resultdata, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
        #         ax6.get_xaxis().set_visible(False)
        #         ax3.set_ylabel('$\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \u0394$, {}'.format(plot_params['arcsec']), labelpad=plot_params['padding'])  # Delta
        #         if plot_params['sub_1_brake_s'] > 0 and plot_params['sub_1_lim_s'] > 0:
        #             ax2.yaxis.set_ticks(arange(plot_params['sub_1_brake_t'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_brake_s']))
        #             ax6.yaxis.set_ticks(arange(plot_params['sub_1_brake_t'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_brake_s']))
        #             ax2.set_ylim(plot_params['sub_1_brake_t'] - plot_params['sub_1_brake_s']/2, plot_params['sub_1_lim_t'] + plot_params['sub_1_brake_s']/2)
        #             ax6.set_ylim(plot_params['sub_1_brake_t'] - plot_params['sub_1_brake_s']/2, plot_params['sub_1_lim_t'] + plot_params['sub_1_brake_s']/2)
        #             ax3.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_brake_f']+1, plot_params['sub_1_lim_s']))
        #             ax7.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_brake_f']+1, plot_params['sub_1_lim_s']))
        #             ax3.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s']/2, plot_params['sub_1_brake_f'] + plot_params['sub_1_lim_s']/2)
        #             ax7.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s']/2, plot_params['sub_1_brake_f'] + plot_params['sub_1_lim_s']/2)

        # self.img.draw()

    def _plot_orbit(self, orbit_params, plot_params):
        self.ax_orbit.plot(
            -orbit_params['model'][:, 1],
            orbit_params['model'][:, 0],
            color=plot_params['color1'],
            linewidth=1)
        for i in range(len(orbit_params['x'])):
            self.ax_orbit.plot([orbit_params['x'][i], -orbit_params['bind'][i, 1]],
                               [orbit_params['y'][i], orbit_params['bind'][i, 0]],
                               color=plot_params['color1'],
                               linestyle='--',
                               linewidth=0.8)
        self.ax_orbit.plot(orbit_params['x'][0],
                           orbit_params['y'][0],
                           color=plot_params['color1'],
                           ls='', marker='o',
                           mec='k', mfc='w',
                           ms=10)
        self.ax_orbit.plot(orbit_params['x'][orbit_params['libPoints']],
                           orbit_params['y'][orbit_params['libPoints']],
                           color=plot_params['color1'],
                           ls='', marker='^',
                           mec='k', mfc='k',
                           ms=5)
        self.ax_orbit.plot(orbit_params['x'][orbit_params['badPoints']],
                           orbit_params['y'][orbit_params['badPoints']],
                           color=plot_params['color1'],
                           ls='', marker='x',
                           mec='k', mfc='w',
                           ms=5)
        self.ax_orbit.plot(orbit_params['x'][orbit_params['newPoints']],
                           orbit_params['y'][orbit_params['newPoints']],
                           color=plot_params['color1'],
                           ls='', marker='o',
                           mec='k', mfc='w',
                           ms=5)
        self.ax_orbit.plot([0, -orbit_params['model'][0, 1]],
                           [0, orbit_params['model'][0, 0]],
                           color=plot_params['color1'],
                           linestyle='-',
                           linewidth=1.2)

    def _plot_literature_orbit(self, orbit_params, plot_params):
        self.ax_orbit.plot(-orbit_params['lit_model'][:, 1],
                           orbit_params['lit_model'][:, 0],
                           color=plot_params['color2'],
                           ls='-', linewidth=0.5)
        for i in range(len(orbit_params['lit_x'])):
            self.ax_orbit.plot([orbit_params['lit_x'][i], -orbit_params['lit_bind'][i, 1]],
                               [orbit_params['lit_y'][i], orbit_params['lit_bind'][i, 0]],
                               color=plot_params['color2'],
                               linestyle='--', linewidth=0.5)
        self.ax_orbit.plot([0, -orbit_params['lit_model'][0, 1]],
                           [0, orbit_params['lit_model'][0, 0]],
                           color=plot_params['color2'],
                           linestyle='-', linewidth=0.5)

    def _plot_orbit_box(self, orbit_params, plot_params):
        text_params = dict(
            porb_t='$P_{orb}$',
            T0_t='$T_{0}$',
            obj_name=orbit_params['name'],
            p_orb='{}$ \pm ${}'.format(*orbit_params['P'].split('|')) if len(orbit_params['P'].split('|')) == 2 else
            orbit_params['P'],
            y=plot_params['year'],
            T_0='{}$ \pm ${}'.format(*orbit_params['T0'].split('|')) if len(orbit_params['T0'].split('|')) == 2 else
            orbit_params['T0'],
            e='{}$ \pm ${}'.format(*orbit_params['e'].split('|')) if len(orbit_params['e'].split('|')) == 2 else
            orbit_params['e'],
            a='{}$ \pm ${}'.format(*orbit_params['a'].split('|')) if len(orbit_params['a'].split('|')) == 2 else
            orbit_params['a'],
            arcsec=plot_params['arcsec'],
            W='{}$ \pm ${}'.format(*orbit_params['W'].split('|')) if len(orbit_params['W'].split('|')) == 2 else
            orbit_params['W'],
            w='{}$ \pm ${}'.format(*orbit_params['w'].split('|')) if len(orbit_params['w'].split('|')) == 2 else
            orbit_params['w'],
            i='{}$ \pm ${}'.format(*orbit_params['i'].split('|')) if len(orbit_params['i'].split('|')) == 2 else
            orbit_params['i']
        )
        textstr = ('     {obj_name}\n\
                {porb_t} = {p_orb} {y}\n\
                {T0_t}  = {T_0} {y}\n\
                $e$   = {e}\n\
                $a$   = {a} {arcsec}\n\
                $\Omega$   = {W}\u00B0\n\
                $\omega$   = {w}\u00B0\n\
                $i$    = {i}\u00B0'.format(**text_params))
        props = dict(boxstyle='round', facecolor='white', alpha=0.2)
        self.ax_orbit.text(plot_params['box_x'], plot_params['box_y'], textstr, fontsize=10, fontname='monospace',
                           style='normal', va='top', ha='left', bbox=props)

    def _set_limits_orbit_plot(self, plot_params):
        xmin = plot_params['lim_x_min']
        xmax = plot_params['lim_x_max']
        ymin = plot_params['lim_y_min']
        ymax = plot_params['lim_y_max']
        self.ax_orbit.set_xlim(xmin, xmax)
        self.ax_orbit.set_ylim(ymin, ymax)

    def _plot_north_direction(self, plot_params):
        self.ax_orbit.arrow(plot_params['north_x'], plot_params['north_y'], -plot_params['north_s'] * 6, 0,
                            head_width=plot_params['north_s'], head_length=plot_params['north_s'] * 2, fc='k', ec='k')
        self.ax_orbit.arrow(plot_params['north_x'], plot_params['north_y'], 0, plot_params['north_s'] * 6,
                            head_width=plot_params['north_s'], head_length=plot_params['north_s'] * 2, fc='k', ec='k')
        self.ax_orbit.text(plot_params['north_x'] - plot_params['north_s'] * 8,
                           plot_params['north_y'] + plot_params['north_s'], 'E', fontsize=10, fontname='monospace',
                           style='oblique')
        self.ax_orbit.text(plot_params['north_x'] - plot_params['north_s'] * 2,
                           plot_params['north_y'] + plot_params['north_s'] * 8, 'N', fontsize=10, fontname='monospace',
                           style='oblique')

    def _plot_orbit_direction(self, plot_params):
        self.ax_orbit.arrow(plot_params['dir_x'], plot_params['dir_y'], plot_params['dir_dx'], plot_params['dir_dy'],
                            head_width=plot_params['north_s'], head_length=plot_params['north_s'] * 2, fc='k', ec='k')

    def _plot_residuals(self, orbit_params, plot_params):
        residuals = calculate_residuals(orbit_params)
        epochs = fromiter((point.epoch for point in orbit_params['position_list']), float)
        self.ax_residuals_1.plot(epochs[0], residuals[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
        self.ax_residuals_1.plot(epochs[orbit_params['newPoints']], residuals[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
        self.ax_residuals_1.plot(epochs[orbit_params['badPoints']], residuals[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
        self.ax_residuals_1.plot(epochs[orbit_params['libPoints']], residuals[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
        # self.ax_residuals_1.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
        # self.ax_residuals_1.set_ylabel('$\u0394\u03C1$, {}'.format(plot_params['arcsec']), labelpad=plot_params['padding'])

        self.ax_box_1.boxplot(residuals, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
        # self.ax_box_1.get_xaxis().set_visible(False)
        
        epoch_ticks = get_tick_positions_for_epochs(epochs)
        self.ax_residuals_1.xaxis.set_ticks(epoch_ticks)

        if plot_params['sub_1_lim_s'] > 0:
            self.ax_residuals_1.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
            self.ax_residuals_1.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])

        if plot_params['Brake_1']:
            self.ax_residuals_2.plot(epochs[0], residuals[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
            self.ax_residuals_2.plot(epochs[orbit_params['newPoints']], residuals[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
            self.ax_residuals_2.plot(epochs[orbit_params['badPoints']], residuals[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
            self.ax_residuals_2.plot(epochs[orbit_params['libPoints']], residuals[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
        
            self.ax_residuals_2.xaxis.set_ticks(epoch_ticks)
            self.ax_residuals_2.set_xticklabels(['']*len(get_tick_positions_for_epochs(epoch_ticks)))
            if plot_params['sub_1_lim_s'] > 0:
                pass
                # ax7.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
                # ax7.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])

    def _plot_rhos_and_thetas(self, orbit_params, plot_params):
        pass

    def on_press(self, event):
        if self.ax_orbit.axes != event.inaxes: return
        self.press = [event.xdata, event.ydata, self.ax_orbit.get_xlim(), self.ax_orbit.get_ylim()]

    def on_motion(self, event):
        if self.press is None: return
        if self.ax_orbit.axes != event.inaxes: return

        if event.xdata and event.ydata:
            x, y, xlim, ylim = self.press
            self.ax_orbit.set_xlim(xlim[0] - (event.xdata - x), xlim[1] - (event.xdata - x))
            self.ax_orbit.set_ylim(ylim[0] - (event.ydata - y), ylim[1] - (event.ydata - y))
            self.img.draw()

            self.press = [x, y, self.ax_orbit.get_xlim(), self.ax_orbit.get_ylim()]

            self.parent_widget.PlotParams.v_lim_x_min.setValue(self.ax_orbit.get_xlim()[0])
            self.parent_widget.PlotParams.v_lim_x_max.setValue(self.ax_orbit.get_xlim()[1])
            self.parent_widget.PlotParams.v_lim_y_min.setValue(self.ax_orbit.get_ylim()[0])
            self.parent_widget.PlotParams.v_lim_y_max.setValue(self.ax_orbit.get_ylim()[1])

    def on_resize(self, event):
        if self.ax_orbit.axes != event.inaxes: return
        if event.button == 'up':
            k = 0.95
        elif event.button == 'down':
            k = 1.05
        else:
            k = 1
        self.ax_orbit.set_xlim(self.ax_orbit.get_xlim()[0] * k, self.ax_orbit.get_xlim()[1] * k)
        self.ax_orbit.set_ylim(self.ax_orbit.get_ylim()[0] * k, self.ax_orbit.get_ylim()[1] * k)
        self.img.draw()

        self.parent_widget.PlotParams.v_lim_x_min.setValue(self.ax_orbit.get_xlim()[0])
        self.parent_widget.PlotParams.v_lim_x_max.setValue(self.ax_orbit.get_xlim()[1])
        self.parent_widget.PlotParams.v_lim_y_min.setValue(self.ax_orbit.get_ylim()[0])
        self.parent_widget.PlotParams.v_lim_y_max.setValue(self.ax_orbit.get_ylim()[1])

    def on_release(self, event):
        self.press = None
        self.img.draw()

    def disconnect_(self):
        """disconnect all the stored connection ids"""
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
