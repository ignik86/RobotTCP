
import RobClient
import time
import MainWindow
import sys

# This gets the Qt stuff
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

import XmlParser

config_file = 'Config.xml'

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class RobThreadClass(QtCore.QThread):

    date_signal = QtCore.pyqtSignal(str)

    def __init__(self):

        super(self.__class__, self).__init__()
        config = XmlParser.ConfigParse(config_file)
        self.rob = RobClient.Client(config.ip(), config.port())

    def run(self):
        while 1:
            current_date = self.rob.request('Date')
            if self.rob.connected:
                print(current_date.decode('utf-8'))
                self.date_signal.emit(current_date.decode('utf-8'))

            time.sleep(1)


class MainWin(QMainWindow, MainWindow.Ui_MainWindow):

    def showdate(self,  date: str):
        self.time.setText(date)

    def plot(self, graph, bar, cur_hour):
        self.dc.update_figure(graph, bar, cur_hour)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file

        l = QVBoxLayout(self.graph)
        self.dc = PlanCanvas(self.graph, width=10, height=4, dpi=100)
        l.addWidget(self.dc)

        self.robthread = RobThreadClass()
        self.robthread.start()
        self.robthread.date_signal.connect(self.showdate)

        config = XmlParser.ConfigParse(config_file)
        logopixmap = QPixmap(config.logopicture())
        h = self.logo.height()
        w = self.logo.width()
        self.logo.setPixmap(logopixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.plt = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        # self.plot.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class PlanCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update_figure)
        # timer.start(2000)

    def compute_initial_figure(self):
        hours = ['07:00', '08:00', '09:00', '10:00', '11:00',
                 '12:00', '13:00', '14:00', '15:00', '16:00']

        l = [0 for i in range(10)]
        self.plt.bar(hours, l, color='g')
        self.plt.grid(which='major', axis='y', linestyle='--')
        self.plt.tick_params('x', labelrotation=25)
        self.plt.set_title('Мониторинг выполнения плана в день')
        self.plt.set_xlabel('Время')
        self.plt.set_ylabel('Количество деталей')
        self.plt.legend()

    def autolabel(self, rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            self.plt.text(rect.get_x() + rect.get_width() / 2., 0.5 * height,
                    '%d' % int(height),
                    ha='center', va='bottom', rotation="vertical", fontsize="large", color="w")

    def update_figure(self, fact, plan, cur_hour):
        # We want the axes cleared every time plot() is called
        self.plt.cla()

        hours = ['07:00', '08:00', '09:00', '10:00', '11:00',
                 '12:00', '13:00', '14:00', '15:00', '16:00']
        l = [0 for i in range(10)]
        l[cur_hour] = fact[cur_hour]
        width = 0.95

        rect = self.plt.bar(hours, fact, color='b', label='факт', align='edge', width=width, edgecolor='g')
        self.plt.bar(hours, l, color='r', label='текущий', align='edge', width=width)

        p = []
        for i in range(10):
            p.append(plan[i])

        h = [i for i in range(10)]
        for i in range(10):
            k = 2 * i
            h.insert(k + 1, i + width)
            p.insert(k, p[k])

        self.plt.plot(h, p, color='r', label='план')
        self.plt.grid(which='major', axis='y', linestyle='--')
        self.plt.tick_params('x', labelrotation=25)
        self.plt.set_title('Мониторинг выполнения цели в день')
        self.plt.set_xlabel('Время')
        self.plt.set_ylabel('Количество ударов')
        self.plt.legend()

        self.autolabel(rect)
        self.draw()

def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWin()
    form.show()
    # form.showFullScreen()
    # form.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
