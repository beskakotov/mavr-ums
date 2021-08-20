from PySide2.QtWidgets import QWidget, QGridLayout
from PySide2.QtCore import Qt, QPoint
from matplotlib.figure import Figure
from matplotlib.pyplot import subplot2grid, GridSpec
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import array, random, ceil, unique, floor, append, sqrt, cos, deg2rad, linspace, arange

class OrbitImage(QWidget):
    def __init__(self, parent = None):
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
    
    def on_press(self, event):
        if self.ax1.axes != event.inaxes: return
        self.press = [event.xdata, event.ydata, self.ax1.get_xlim(), self.ax1.get_ylim()]

    def on_motion(self, event):
        if self.press is None: return
        if self.ax1.axes != event.inaxes: return
        
        if event.xdata and event.ydata:
            x, y, xlim, ylim = self.press
            self.ax1.set_xlim(xlim[0] - (event.xdata - x), xlim[1] - (event.xdata - x))
            self.ax1.set_ylim(ylim[0] - (event.ydata - y), ylim[1] - (event.ydata - y))
            self.img.draw()

            self.press = [x, y, self.ax1.get_xlim(), self.ax1.get_ylim()]

            self.parent_widget.PlotParams.v_lim_x_min.setValue(self.ax1.get_xlim()[0])
            self.parent_widget.PlotParams.v_lim_x_max.setValue(self.ax1.get_xlim()[1])
            self.parent_widget.PlotParams.v_lim_y_min.setValue(self.ax1.get_ylim()[0])
            self.parent_widget.PlotParams.v_lim_y_max.setValue(self.ax1.get_ylim()[1])

    def on_resize(self, event):
        if self.ax1.axes != event.inaxes: return
        if event.button == 'up':
            k = 0.95
        elif event.button == 'down':
            k = 1.05
        else:
            k = 1
        self.ax1.set_xlim(self.ax1.get_xlim()[0]*k, self.ax1.get_xlim()[1]*k)
        self.ax1.set_ylim(self.ax1.get_ylim()[0]*k, self.ax1.get_ylim()[1]*k)
        self.img.draw()

        self.parent_widget.PlotParams.v_lim_x_min.setValue(self.ax1.get_xlim()[0])
        self.parent_widget.PlotParams.v_lim_x_max.setValue(self.ax1.get_xlim()[1])
        self.parent_widget.PlotParams.v_lim_y_min.setValue(self.ax1.get_ylim()[0])
        self.parent_widget.PlotParams.v_lim_y_max.setValue(self.ax1.get_ylim()[1])

    def on_release(self, event):
        self.press = None
        self.img.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)
    
    def plot(self, orbit_params, plot_params):
        self.fig.clear()
        if plot_params['OrbitOnly']:
            self._plot_orbit_only(orbit_params, plot_params)
        else:
            if plot_params['SubMode'] == 'errors' or plot_params['SubMode'] == True:
                self._plot_with_errors(orbit_params, plot_params)
            elif plot_params['SubMode'] == 'residuals' or plot_params['SubMode'] == False:
                self._plot_with_residuals(orbit_params, plot_params)
        self.img.draw()
    
    def _plot_orbit_only(self, orbit_params, plot_params):
        self.setFixedSize(600, 600)
        # ax = self.fig.add_subplot(111)
        
    
    def _plot_with_residuals(self, orbit_params, plot_params):
        self.setFixedSize(600, 700)
        gridspec = self.fig.add_gridspec(7, 2,
                      width_ratios=(7, 2), height_ratios=(75, 5, 5, 5, 5, 5, 5),
                      left=0.1, right=0.95, bottom=0.05, top=0.95,
                      wspace=0.2, hspace=0)
        if plot_params['Brake_1']:
            pass

    def _plot_with_errors(self, orbit_params, plot_params):
        self.setFixedSize(600, 800)
        ax = self.fig.add_subplot()
        ax = self.__main_axis_settings(ax)
    
    def __main_axis_settings(self, axis):
        axis.axis('equal')
        axis.tick_params(direction='in')
        return axis
    
    def __standart_axis(self, axis):
        pass

    def __axis_without_bottom(self, axis):
        pass

    def __axis_without_top(self, axis):
        pass

        # gs = self.fig.add_gridspec(7, 2,  width_ratios=(7, 2), height_ratios=(16, 1, 2, 2, 2, 2, 2),
                    #   left=0.1, right=0.95, bottom=0.05, top=0.95,
                    #   wspace=0.2, hspace=0)

        # ax1 = self.fig.add_subplot(gs[0, :])

        # self.img.draw()
        return
        
        
        grid = GridSpec(50, 5, wspace=0.5, hspace=0)
        d = .025
        k = 6
        if plot_params['SubMode']:
            r1, r2, w, r = 75*2, 20*2, 5*2, 1
            if plot_params['Brake_1'] and plot_params['Brake_2']:
                self.ax1 =   subplot2grid((r1 + r2*2 + w + r*2, 5), (0, 0),                            rowspan=r1,        colspan=5, fig=self.fig)
                ax2 =   subplot2grid((r1 + r2*2 + w + r*2, 5), (r1 + w, 0),                       rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax3 =   subplot2grid((r1 + r2*2 + w + r*2, 5), (r1 + w + int(r2/2) + r, 0),       rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax4 =   subplot2grid((r1 + r2*2 + w + r*2, 5), (r1 + w + r2 + r, 0),            rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax5 =   subplot2grid((r1 + r2*2 + w + r*2, 5), (r1 + w + int(r2*1.5) + r*2, 0), rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax6 =   subplot2grid((r1 + r2*2 + w + r*2, 5), (r1 + w, 4),                       rowspan=int(r2/2), colspan=1, fig=self.fig)
                ax7 =   subplot2grid((r1 + r2*2 + w + r*2, 5), (r1 + w + int(r2/2) + r, 4),       rowspan=int(r2/2), colspan=1, fig=self.fig)
                ax8 =   subplot2grid((r1 + r2*2 + w + r*2, 5), (r1 + w + r2 + r, 4),            rowspan=int(r2/2), colspan=1, fig=self.fig)
                ax9 =   subplot2grid((r1 + r2*2 + w + r*2, 5), (r1 + w + int(r2*1.5) + r*2, 4), rowspan=int(r2/2), colspan=1, fig=self.fig)

                self.ax1.axis('equal')
                self.ax1.tick_params(direction='in')
                ax2.tick_params(direction='in')
                ax2.xaxis.set_ticks_position('top')
                ax3.tick_params(direction='in')
                ax3.xaxis.set_ticks_position('bottom')
                ax4.tick_params(direction='in')
                ax4.xaxis.set_ticks_position('top')
                ax5.tick_params(direction='in')
                ax5.xaxis.set_ticks_position('bottom')
                ax6.tick_params(direction='in')
                ax7.tick_params(direction='in')
                ax8.tick_params(direction='in')
                ax9.tick_params(direction='in')

                ax2.spines['bottom'].set_visible(False)
                ax2.tick_params(labelbottom='off')
                ax3.spines['top'].set_visible(False)

                ax6.xaxis.set_visible(False)
                ax6.spines['bottom'].set_visible(False)
                ax6.tick_params(direction='in')
                ax6.tick_params(labelbottom='off')
                ax7.spines['top'].set_visible(False)

                kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
                ax2.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
                ax2.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax3.transAxes)  # switch to the bottom axes
                ax3.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax3.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

                kwargs.update(transform=ax6.transAxes)
                ax6.plot((-d * k, +d * k), (-d, +d), **kwargs)  # top-left diagonal
                ax6.plot((1 - d * k, 1 + d * k), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax7.transAxes)  # switch to the bottom axes
                ax7.plot((-d * k, +d * k), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax7.plot((1 - d * k, 1 + d * k), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

                ax4.spines['bottom'].set_visible(False)
                ax4.tick_params(labelbottom='off')
                ax5.spines['top'].set_visible(False)

                ax8.xaxis.set_visible(False)
                ax8.spines['bottom'].set_visible(False)
                ax8.tick_params(direction='in')
                ax8.tick_params(labelbottom='off')
                ax9.spines['top'].set_visible(False)

                kwargs = dict(transform=ax4.transAxes, color='k', clip_on=False)
                ax4.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
                ax4.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax5.transAxes)  # switch to the bottom axes
                ax5.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax5.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

                kwargs.update(transform=ax8.transAxes)
                ax8.plot((-d * k, +d * k), (-d, +d), **kwargs)  # top-left diagonal
                ax8.plot((1 - d * k, 1 + d * k), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax9.transAxes)  # switch to the bottom axes
                ax9.plot((-d * k, +d * k), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax9.plot((1 - d * k, 1 + d * k), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

            elif plot_params['Brake_1'] and not plot_params['Brake_2']:
                self.ax1 =   subplot2grid((r1 + w + r2*2 + r, 5), (0, 0),                      rowspan=r1,        colspan=5, fig=self.fig)
                ax2 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w, 0),                 rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax3 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w + int(r2/2) + r, 0), rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax5 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w + r2 + r, 0),      rowspan=r2,        colspan=4, fig=self.fig)
                ax6 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w, 4),                 rowspan=int(r2/2), colspan=1, fig=self.fig)
                ax7 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w + int(r2/2) + r, 4), rowspan=int(r2/2), colspan=1, fig=self.fig)
                ax9 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w + r2 + r, 4),      rowspan=r2,        colspan=1, fig=self.fig)

                self.ax1.axis('equal')
                self.ax1.tick_params(direction='in')
                ax2.tick_params(direction='in')
                ax2.xaxis.set_ticks_position('top')
                ax3.tick_params(direction='in')
                ax3.xaxis.set_ticks_position('bottom')
                ax5.tick_params(direction='in')
                ax5.xaxis.set_ticks_position('both')
                ax6.tick_params(direction='in')
                ax7.tick_params(direction='in')
                ax9.tick_params(direction='in')

                ax2.spines['bottom'].set_visible(False)
                ax2.tick_params(labelbottom='off')
                ax3.spines['top'].set_visible(False)

                ax6.xaxis.set_visible(False)
                ax6.spines['bottom'].set_visible(False)
                ax6.tick_params(direction='in')
                ax6.tick_params(labelbottom='off')
                ax7.spines['top'].set_visible(False)

                kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
                ax2.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
                ax2.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax3.transAxes)  # switch to the bottom axes
                ax3.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax3.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

                kwargs.update(transform=ax6.transAxes)
                ax6.plot((-d * k, +d * k), (-d, +d), **kwargs)  # top-left diagonal
                ax6.plot((1 - d * k, 1 + d * k), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax7.transAxes)  # switch to the bottom axes
                ax7.plot((-d * k, +d * k), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax7.plot((1 - d * k, 1 + d * k), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

            elif not plot_params['Brake_1'] and plot_params['Brake_2']:
                self.ax1 =   subplot2grid((r1 + w + r2*2 + r, 5), (0, 0),                          rowspan=r1,        colspan=5, fig=self.fig)
                ax3 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w, 0),                     rowspan=r2,        colspan=4, fig=self.fig)
                ax4 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w + r2, 0),              rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax5 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w + int(r2*1.5) + r, 0), rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax7 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w, 4),                     rowspan=r2,        colspan=1, fig=self.fig)
                ax8 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w + r2, 4),              rowspan=int(r2/2), colspan=1, fig=self.fig)
                ax9 =   subplot2grid((r1 + w + r2*2 + r, 5), (r1 + w + int(r2*1.5) + r, 4), rowspan=int(r2/2), colspan=1, fig=self.fig)

                self.ax1.axis('equal')
                self.ax1.tick_params(direction='in')
                ax3.tick_params(direction='in')
                ax3.xaxis.set_ticks_position('both')
                ax4.tick_params(direction='in')
                ax4.xaxis.set_ticks_position('top')
                ax5.tick_params(direction='in')
                ax5.xaxis.set_ticks_position('bottom')
                ax7.tick_params(direction='in')
                ax8.tick_params(direction='in')
                ax9.tick_params(direction='in')

                ax4.spines['bottom'].set_visible(False)
                ax4.tick_params(labelbottom='off')
                ax5.spines['top'].set_visible(False)

                ax8.xaxis.set_visible(False)
                ax8.spines['bottom'].set_visible(False)
                ax8.tick_params(direction='in')
                ax8.tick_params(labelbottom='off')
                ax9.spines['top'].set_visible(False)

                kwargs = dict(transform=ax4.transAxes, color='k', clip_on=False)
                ax4.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
                ax4.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax5.transAxes)  # switch to the bottom axes
                ax5.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax5.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

                kwargs.update(transform=ax8.transAxes)
                ax8.plot((-d * k, +d * k), (-d, +d), **kwargs)  # top-left diagonal
                ax8.plot((1 - d * k, 1 + d * k), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax9.transAxes)  # switch to the bottom axes
                ax9.plot((-d * k, +d * k), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax9.plot((1 - d * k, 1 + d * k), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

            else:
                self.ax1 =   subplot2grid((r1 + r2*2 + w, 5), (0, 0),                  rowspan=r1,        colspan=5, fig=self.fig)
                ax3 =   subplot2grid((r1 + r2*2 + w, 5), (r1 + w, 0),             rowspan=r2, colspan=4, fig=self.fig)
                ax5 =   subplot2grid((r1 + r2*2 + w, 5), (r1 + r2 + w, 0),        rowspan=r2, colspan=4, fig=self.fig)
                ax7 =   subplot2grid((r1 + r2*2 + w, 5), (r1 + w, 4),             rowspan=r2, colspan=1, fig=self.fig)
                ax9 =   subplot2grid((r1 + r2*2 + w, 5), (r1 + r2 + w, 4),        rowspan=r2, colspan=1, fig=self.fig)

                self.ax1.axis('equal')
                self.ax1.tick_params(direction='in')
                ax3.tick_params(direction='in')
                ax3.xaxis.set_ticks_position('both')
                ax5.tick_params(direction='in')
                ax5.xaxis.set_ticks_position('both')
                ax7.tick_params(direction='in')
                ax9.tick_params(direction='in')
        else:
            r1, r2, w, r = 75*2, 20*2, 5*2, 1
            if plot_params['Brake_1']:
                self.ax1 =   subplot2grid((r1 + r2 + w + r, 5), (0, 0),                          rowspan=r1, colspan=5, fig=self.fig)
                ax2 =   subplot2grid((r1 + r2 + w + r, 5), (r1 + w, 0),                     rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax3 =   subplot2grid((r1 + r2 + w + r, 5), (r1 + int(r2/2) + w + r, 0),     rowspan=int(r2/2), colspan=4, fig=self.fig)
                ax6 =   subplot2grid((r1 + r2 + w + r, 5), (r1 + w, 4),                     rowspan=int(r2/2), colspan=1, fig=self.fig)
                ax7 =   subplot2grid((r1 + r2 + w + r, 5), (r1 + int(r2/2) + w + r, 4),     rowspan=int(r2/2), colspan=1, fig=self.fig)

                self.ax1.axis('equal')
                self.ax1.tick_params(direction='in')
                ax2.tick_params(direction='in')
                ax2.xaxis.set_ticks_position('top')
                ax3.tick_params(direction='in')
                ax3.xaxis.set_ticks_position('bottom')
                ax6.tick_params(direction='in')
                ax7.tick_params(direction='in')

                ax2.spines['bottom'].set_visible(False)
                ax2.tick_params(labelbottom='off')
                ax3.spines['top'].set_visible(False)

                ax6.xaxis.set_visible(False)
                ax6.spines['bottom'].set_visible(False)
                ax6.tick_params(direction='in')
                ax6.tick_params(labelbottom='off')
                ax7.spines['top'].set_visible(False)

                kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
                ax2.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
                ax2.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax3.transAxes)  # switch to the bottom axes
                ax3.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax3.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

                k = 6
                kwargs.update(transform=ax6.transAxes)
                ax6.plot((-d * k, +d * k), (-d, +d), **kwargs)  # top-left diagonal
                ax6.plot((1 - d * k, 1 + d * k), (-d, +d), **kwargs)  # top-right diagonal
                kwargs.update(transform=ax7.transAxes)  # switch to the bottom axes
                ax7.plot((-d * k, +d * k), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax7.plot((1 - d * k, 1 + d * k), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

            else:
                self.ax1 =   subplot2grid((r1 + r2 + w, 5), (0, 0),      rowspan=r1, colspan=5, fig=self.fig)
                ax3 =   subplot2grid((r1 + r2 + w, 5), (r1 + w, 0), rowspan=r2, colspan=4, fig=self.fig)
                ax7 =   subplot2grid((r1 + r2 + w, 5), (r1 + w, 4), rowspan=r2, colspan=1, fig=self.fig)

                self.ax1.axis('equal')
                self.ax1.tick_params(direction='in')
                ax3.tick_params(direction='in')
                ax3.xaxis.set_ticks_position('both')
                ax7.tick_params(direction='in')
        
        self.cidpress   = self.img.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.img.mpl_connect('button_release_event', self.on_release)
        self.cidmotion  = self.img.mpl_connect('motion_notify_event', self.on_motion)
        self.cidmotion  = self.img.mpl_connect('scroll_event', self.on_resize)

        self.ax1.plot(-orbit_params['model'][:, 1], orbit_params['model'][:, 0], color=plot_params['color1'], linewidth=1)
        for i in range(len(orbit_params['x'])):
            self.ax1.plot([orbit_params['x'][i], -orbit_params['bind'][i, 1]], [orbit_params['y'][i], orbit_params['bind'][i, 0]], color=plot_params['color1'], linestyle='--', linewidth=0.8)
        self.ax1.plot(orbit_params['x'][0], orbit_params['y'][0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
        self.ax1.plot(orbit_params['x'][orbit_params['libPoints']], orbit_params['y'][orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
        self.ax1.plot(orbit_params['x'][orbit_params['badPoints']], orbit_params['y'][orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='w', ms=5)
        self.ax1.plot(orbit_params['x'][orbit_params['newPoints']], orbit_params['y'][orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
        self.ax1.plot([0, -orbit_params['model'][0, 1]], [0, orbit_params['model'][0, 0]], color=plot_params['color1'], linestyle='-', linewidth=1.2)
        
        if orbit_params['litplot']:
            self.ax1.plot(-orbit_params['lit_model'][:, 1], orbit_params['lit_model'][:, 0], color = plot_params['color2'], ls='-', linewidth=0.5)
            for i in range(len(orbit_params['lit_x'])):
                self.ax1.plot([orbit_params['lit_x'][i], -orbit_params['lit_bind'][i, 1]], [orbit_params['lit_y'][i], orbit_params['lit_bind'][i, 0]], color=plot_params['color2'], linestyle='--', linewidth=0.5)
            self.ax1.plot([0, -orbit_params['lit_model'][0, 1]], [0, orbit_params['lit_model'][0, 0]], color=plot_params['color2'], linestyle='-', linewidth=0.5)
        if plot_params['OrbitBox']:
            text_params = dict(
                porb_t = '$P_{orb}$',
                T0_t = '$T_{0}$',
                obj_name = orbit_params['name'],
                p_orb = '{}$ \pm ${}'.format(*orbit_params['P'].split('|')) if len(orbit_params['P'].split('|')) == 2 else orbit_params['P'],
                y = plot_params['year'],
                T_0 = '{}$ \pm ${}'.format(*orbit_params['T0'].split('|')) if len(orbit_params['T0'].split('|')) == 2 else orbit_params['T0'],
                e = '{}$ \pm ${}'.format(*orbit_params['e'].split('|')) if len(orbit_params['e'].split('|')) == 2 else orbit_params['e'],
                a = '{}$ \pm ${}'.format(*orbit_params['a'].split('|')) if len(orbit_params['a'].split('|')) == 2 else orbit_params['a'],
                arcsec = plot_params['arcsec'],
                W = '{}$ \pm ${}'.format(*orbit_params['W'].split('|')) if len(orbit_params['W'].split('|')) == 2 else orbit_params['W'],
                w = '{}$ \pm ${}'.format(*orbit_params['w'].split('|')) if len(orbit_params['w'].split('|')) == 2 else orbit_params['w'],
                i = '{}$ \pm ${}'.format(*orbit_params['i'].split('|')) if len(orbit_params['i'].split('|')) == 2 else orbit_params['i']    
            )
            textstr = ('''     {obj_name}
{porb_t} = {p_orb} {y}
{T0_t}  = {T_0} {y}
$e$   = {e}
$a$   = {a} {arcsec}
$\Omega$   = {W}\u00B0
$\omega$   = {w}\u00B0
$i$    = {i}\u00B0'''.format(**text_params))
            props = dict(boxstyle='round', facecolor='white', alpha=0.2)
            self.ax1.text(plot_params['box_x'], plot_params['box_y'], textstr, fontsize=10, fontname='monospace', style='normal', va='top', ha='left', bbox=props)
        if not orbit_params['fplot']:
            xmin = plot_params['lim_x_min']#self.pd.v_x_min.value()
            xmax = plot_params['lim_x_max']
            ymin = plot_params['lim_y_min']
            ymax = plot_params['lim_y_max']
            #if xmax - xmin > ymax - ymin:
            #    ymin, ymax = [(ymax+ymin)/2 - (xmax-xmin)/2, (ymax+ymin)/2 + (xmax-xmin)/2]
            #elif xmax - xmin < ymax - ymin:
            #    xmin, xmax = [(xmax+xmin)/2 - (ymax-ymin)/2, (xmax+xmin)/2 + (ymax-ymin)/2]
            self.ax1.set_xlim(xmin, xmax)
            self.ax1.set_ylim(ymin, ymax)
            
        self.parent_widget.PlotParams.v_lim_x_min.setValue(self.ax1.get_xlim()[0])
        self.parent_widget.PlotParams.v_lim_x_max.setValue(self.ax1.get_xlim()[1])
        self.parent_widget.PlotParams.v_lim_y_min.setValue(self.ax1.get_ylim()[0])
        self.parent_widget.PlotParams.v_lim_y_max.setValue(self.ax1.get_ylim()[1])
        
        if plot_params['NDirect']:
            self.ax1.arrow(plot_params['north_x'], plot_params['north_y'], -plot_params['north_s']*6, 0, head_width=plot_params['north_s'], head_length=plot_params['north_s']*2, fc='k', ec='k')
            self.ax1.arrow(plot_params['north_x'], plot_params['north_y'], 0, plot_params['north_s']*6, head_width=plot_params['north_s'], head_length=plot_params['north_s']*2, fc='k', ec='k')
            self.ax1.text(plot_params['north_x']-plot_params['north_s']*8 , plot_params['north_y']+plot_params['north_s'], 'E', fontsize=10, fontname='monospace', style='oblique')
            self.ax1.text(plot_params['north_x']-plot_params['north_s']*2, plot_params['north_y']+plot_params['north_s']*8, 'N', fontsize=10, fontname='monospace', style='oblique')
        if plot_params['ODirect']:    
            self.ax1.arrow(plot_params['dir_x'], plot_params['dir_y'], plot_params['dir_dx'], plot_params['dir_dy'], head_width=plot_params['north_s'], head_length=plot_params['north_s']*2, fc='k', ec='k')
        
        with open(self.parent_widget.v_output.text()) as f:
            raw = f.read().split('\n')
        output = array([])
        data = array([])
        theta = array([])
        rho = array([])
        fastcalc = lambda rho, drho, dtheta: sqrt(rho**2 + (rho + drho)**2 - 2*rho*(rho+drho)*cos(deg2rad(dtheta)))
        for line in raw[15:]:
            if not line or line.startswith('#'): continue
            data = append(data, float(line.split()[0]))
            theta = append(theta, float(line.split()[3]))
            rho = append(rho, float(line.split()[4]))
        dtheta = theta[:]
        drho = rho[:]
        rho = orbit_params['pos'][:, 2]
        resultdata = []
        calcdata = array([rho, drho, dtheta]).T
        for i, j, k in calcdata:
            resultdata.append(fastcalc(i, j, k))
        resultdata = array(resultdata)
        if data.max() - data.min() > 2:
            epochs_ticks = unique(linspace(floor(data.min()), ceil(data.max()), 6, dtype='uint16'))
        else:
            step = 0
            while True:
                step += 0.1
                if step > data.max() - data.min():
                    exit()
                epochs_ticks = arange(floor((data.min()-0.05)*10)/10, ceil((data.max()+0.05)*10)/10+step/2, step)
                if epochs_ticks.min() < data.min() and epochs_ticks.max() > data.max() and epochs_ticks.size <= 7:
                    break

        if plot_params['SubMode']:
            ax3.plot(data[0], drho[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
            ax3.plot(data[orbit_params['newPoints']], drho[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
            ax3.plot(data[orbit_params['badPoints']], drho[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
            ax3.plot(data[orbit_params['libPoints']], drho[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
            ax3.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
            ax3.set_ylabel('$\u0394\u03C1$, {}'.format(plot_params['arcsec']), labelpad=plot_params['padding'])
            # ax3.xaxis.set_ticks(epochs_ticks)
            ax3.xaxis.set_ticks(epochs_ticks)
            ax3.set_xticklabels(['']*len(epochs_ticks))

            ax5.plot(data[0], dtheta[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
            ax5.plot(data[orbit_params['newPoints']], dtheta[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
            ax5.plot(data[orbit_params['badPoints']], dtheta[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
            ax5.plot(data[orbit_params['libPoints']], dtheta[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
            ax5.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
            ax5.set_xlabel(plot_params['epoch'])
            ax5.set_ylabel('$\u0394\u03B8$, \u00B0', labelpad=plot_params['padding'])
            ax5.xaxis.set_ticks(epochs_ticks)
           
            ax7.boxplot(drho, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
            ax7.get_xaxis().set_visible(False)

            ax9.boxplot(dtheta, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
            ax9.get_xaxis().set_visible(False)

            if plot_params['sub_1_lim_s'] > 0:
                ax3.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
                ax7.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
                ax3.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])
                ax7.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])
            
            if plot_params['sub_2_lim_s'] > 0:
                ax5.yaxis.set_ticks(arange(plot_params['sub_2_lim_f'], plot_params['sub_2_lim_t']+1, plot_params['sub_2_lim_s']))
                ax9.yaxis.set_ticks(arange(plot_params['sub_2_lim_f'], plot_params['sub_2_lim_t']+1, plot_params['sub_2_lim_s']))
                ax5.set_ylim(plot_params['sub_2_lim_f'] - plot_params['sub_2_lim_s'], plot_params['sub_2_lim_t'] + plot_params['sub_2_lim_s'])
                ax9.set_ylim(plot_params['sub_2_lim_f'] - plot_params['sub_2_lim_s'], plot_params['sub_2_lim_t'] + plot_params['sub_2_lim_s'])

            if plot_params['Brake_1']:
                ax2.plot(data[0], drho[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
                ax2.plot(data[orbit_params['newPoints']], drho[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
                ax2.plot(data[orbit_params['badPoints']], drho[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
                ax2.plot(data[orbit_params['libPoints']], drho[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
                ax2.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
                ax2.xaxis.set_ticks(epochs_ticks)
                ax2.set_xticklabels(['']*len(epochs_ticks))

                ax3.set_ylabel('$\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \u0394\u03C1$, {}'.format(plot_params['arcsec']), labelpad=plot_params['padding'])
                ax6.boxplot(drho, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
                ax6.get_xaxis().set_visible(False)

                if plot_params['sub_1_brake_s'] > 0 and plot_params['sub_1_lim_s'] > 0:
                    ax2.yaxis.set_ticks(arange(plot_params['sub_1_brake_t'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_brake_s']))
                    ax6.yaxis.set_ticks(arange(plot_params['sub_1_brake_t'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_brake_s']))
                    ax2.set_ylim(plot_params['sub_1_brake_t'] - plot_params['sub_1_brake_s']/2, plot_params['sub_1_lim_t'] + plot_params['sub_1_brake_s']/2)
                    ax6.set_ylim(plot_params['sub_1_brake_t'] - plot_params['sub_1_brake_s']/2, plot_params['sub_1_lim_t'] + plot_params['sub_1_brake_s']/2)
                    ax3.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_brake_f']+1, plot_params['sub_1_lim_s']))
                    ax7.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_brake_f']+1, plot_params['sub_1_lim_s']))
                    ax3.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s']/2, plot_params['sub_1_brake_f'] + plot_params['sub_1_lim_s']/2)
                    ax7.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s']/2, plot_params['sub_1_brake_f'] + plot_params['sub_1_lim_s']/2)

            if plot_params['Brake_2']:
                ax4.plot(data[0], dtheta[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
                ax4.plot(data[orbit_params['newPoints']], dtheta[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
                ax4.plot(data[orbit_params['badPoints']], dtheta[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
                ax4.plot(data[orbit_params['libPoints']], dtheta[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
                ax4.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
                ax4.xaxis.set_ticks(epochs_ticks)
                ax4.set_xticklabels(['']*len(epochs_ticks))

                ax5.set_ylabel('$\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \u0394\u03B8$, \u00B0'.format(plot_params['arcsec']), labelpad=plot_params['padding'])
                ax8.boxplot(dtheta, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
                ax8.get_xaxis().set_visible(False)
                
                if plot_params['sub_2_brake_s'] > 0 and plot_params['sub_2_lim_s'] > 0:
                    ax4.yaxis.set_ticks(arange(plot_params['sub_2_brake_t'], plot_params['sub_2_lim_t']+1, plot_params['sub_2_brake_s']))
                    ax8.yaxis.set_ticks(arange(plot_params['sub_2_brake_t'], plot_params['sub_2_lim_t']+1, plot_params['sub_2_brake_s']))
                    ax4.set_ylim(plot_params['sub_2_brake_t'] - plot_params['sub_2_brake_s']/2, plot_params['sub_2_lim_t'] + plot_params['sub_2_brake_s']/2)
                    ax8.set_ylim(plot_params['sub_2_brake_t'] - plot_params['sub_2_brake_s']/2, plot_params['sub_2_lim_t'] + plot_params['sub_2_brake_s']/2)
                    ax5.yaxis.set_ticks(arange(plot_params['sub_2_lim_f'], plot_params['sub_2_brake_f']+1, plot_params['sub_2_lim_s']))
                    ax9.yaxis.set_ticks(arange(plot_params['sub_2_lim_f'], plot_params['sub_2_brake_f']+1, plot_params['sub_2_lim_s']))
                    ax5.set_ylim(plot_params['sub_2_lim_f'] - plot_params['sub_2_lim_s']/2, plot_params['sub_2_brake_f'] + plot_params['sub_2_lim_s']/2)
                    ax9.set_ylim(plot_params['sub_2_lim_f'] - plot_params['sub_2_lim_s']/2, plot_params['sub_2_brake_f'] + plot_params['sub_2_lim_s']/2)

        else:
            ax3.set_ylabel('$\u0394$, {}'.format(plot_params['arcsec'], labelpad=plot_params['padding']))  # Delta
            ax3.plot(data[0], resultdata[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
            ax3.plot(data[orbit_params['newPoints']], resultdata[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
            ax3.plot(data[orbit_params['badPoints']], resultdata[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
            ax3.plot(data[orbit_params['libPoints']], resultdata[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
            ax3.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
            ax3.set_xlabel(plot_params['epoch'])
            ax3.xaxis.set_ticks(epochs_ticks)

            ax7.boxplot(resultdata, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
            ax7.get_xaxis().set_visible(False)

            if plot_params['sub_1_lim_s'] > 0:
                ax3.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
                ax7.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_lim_s']))
                ax3.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])
                ax7.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s'], plot_params['sub_1_lim_t'] + plot_params['sub_1_lim_s'])
            
            if plot_params['Brake_1']:
                ax2.plot(data[0], resultdata[0], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=10)
                ax2.plot(data[orbit_params['newPoints']], resultdata[orbit_params['newPoints']], color=plot_params['color1'], ls='', marker='o', mec='k', mfc='w', ms=5)
                ax2.plot(data[orbit_params['badPoints']], resultdata[orbit_params['badPoints']], color=plot_params['color1'], ls='', marker='x', mec='k', mfc='k', ms=5)
                ax2.plot(data[orbit_params['libPoints']], resultdata[orbit_params['libPoints']], color=plot_params['color1'], ls='', marker='^', mec='k', mfc='k', ms=5)
                ax2.axhline(0, color=plot_params['color1'], linestyle='--', linewidth=1)
                ax2.xaxis.set_ticks(epochs_ticks)
                ax2.set_xticklabels(['']*len(epochs_ticks))

                ax6.boxplot(resultdata, boxprops={'color': plot_params['color1']}, medianprops={'color': plot_params['color1']}, whiskerprops={'linestyle': '-', 'color': plot_params['color1']})
                ax6.get_xaxis().set_visible(False)
                ax3.set_ylabel('$\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \u0394$, {}'.format(plot_params['arcsec']), labelpad=plot_params['padding'])  # Delta
                if plot_params['sub_1_brake_s'] > 0 and plot_params['sub_1_lim_s'] > 0:
                    ax2.yaxis.set_ticks(arange(plot_params['sub_1_brake_t'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_brake_s']))
                    ax6.yaxis.set_ticks(arange(plot_params['sub_1_brake_t'], plot_params['sub_1_lim_t']+1, plot_params['sub_1_brake_s']))
                    ax2.set_ylim(plot_params['sub_1_brake_t'] - plot_params['sub_1_brake_s']/2, plot_params['sub_1_lim_t'] + plot_params['sub_1_brake_s']/2)
                    ax6.set_ylim(plot_params['sub_1_brake_t'] - plot_params['sub_1_brake_s']/2, plot_params['sub_1_lim_t'] + plot_params['sub_1_brake_s']/2)
                    ax3.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_brake_f']+1, plot_params['sub_1_lim_s']))
                    ax7.yaxis.set_ticks(arange(plot_params['sub_1_lim_f'], plot_params['sub_1_brake_f']+1, plot_params['sub_1_lim_s']))
                    ax3.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s']/2, plot_params['sub_1_brake_f'] + plot_params['sub_1_lim_s']/2)
                    ax7.set_ylim(plot_params['sub_1_lim_f'] - plot_params['sub_1_lim_s']/2, plot_params['sub_1_brake_f'] + plot_params['sub_1_lim_s']/2)

        self.img.draw()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()