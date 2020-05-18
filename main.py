
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
import math
config_file = 'Config.xml'

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import matplotlib.transforms

class RobThreadClass(QtCore.QThread):

    date_signal = QtCore.pyqtSignal(str)
    shift_num_signal = QtCore.pyqtSignal(str)
    graph_signal = QtCore.pyqtSignal(list, list, list, int)
    hours_signal = QtCore.pyqtSignal(list)

    def __init__(self):

        super(self.__class__, self).__init__()
        self.config = XmlParser.ConfigParse(config_file)
        self.rob = RobClient.Client(self.config.ip(), self.config.port())

    def request(self, message):
        answer = self.rob.request(message)
        if self.rob.connected:

            if answer.decode('utf-8') == 'N/A':
                print('Answer on request %s: Wrong request' % message)
                return False
            else:
                print('Answer on request %s: %s ' % (message, answer.decode('utf-8')))

            return answer.decode('utf-8')
        else:
            print('No server')
            return False

    def run(self):
        counter_array = [0 for i in range(9)]
        plan_array = [0 for i in range(9)]
        while 1:
            current_date = self.request('Date')
            if current_date:
                self.date_signal.emit(current_date)

            shift_num = self.request('Nshift')
            if shift_num:
                self.shift_num_signal.emit(shift_num)

            count = self.request('Count')
            if count:
                hour_counters = count.split('/')
                counter_array = []
                for counter in hour_counters:
                    counter_array.append(int(counter))

            current_time = self.request('Time')
            if current_time:
                print(int(current_time[0:2]))
            plan = int(self.request('Plan'))

            if plan:
                shift = []
                interval = []
                if int(shift_num) == 1:
                    shift, interval = self.config.shift1()
                elif int(shift_num) == 2:
                    shift, interval = self.config.shift2()
                elif int(shift_num) == 3:
                    shift, interval = self.config.shift3()

                total_time = 0
                for available_minute in shift.split('/'):
                    total_time = total_time + int(available_minute)
                time_per_peace = total_time / plan
                plan_array = []
                for available_minute in shift.split('/'):
                    plan_array.append(round(int(available_minute)/time_per_peace))

                self.hours_signal.emit(interval.split('/'))
                self.graph_signal.emit(counter_array, plan_array, interval.split('/'), 5)


            time.sleep(1)


class MainWin(QMainWindow, MainWindow.Ui_MainWindow):

    def showdate(self,  date: str):
        self.time.setText(date)

    def showshift(self, shift: str):
        self.shift.setText('Смена № %s' % shift)

    def plot(self, graph, bar, hours, cur_hour):
        self.dc.update_figure(graph, bar, hours, cur_hour)

    def hours_show(self, hours):
        self.hours = hours
        self.time_label.setText(self.hours[0])
        self.time_label_2.setText(self.hours[1])
        self.time_label_3.setText(self.hours[2])
        self.time_label_4.setText(self.hours[3])
        self.time_label_5.setText(self.hours[4])
        self.time_label_6.setText(self.hours[5])
        self.time_label_7.setText(self.hours[6])
        self.time_label_8.setText(self.hours[7])
        self.time_label_9.setText(self.hours[8])

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file

        l = QVBoxLayout(self.graph)
        self.dc = PlanCanvas(self.graph, width=10, height=4, dpi=100)
        l.addWidget(self.dc)

        self.robthread = RobThreadClass()
        self.robthread.start()
        self.robthread.date_signal.connect(self.showdate)
        self.robthread.shift_num_signal.connect(self.showshift)
        self.hours = ['07:20-08:00', '08:00-09:00', '09:00-10:00', '10:00-11:00',
                 '11:00-12:00',
                 '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00']

        self.robthread.graph_signal.connect(self.plot)
        self.robthread.hours_signal.connect(self.hours_show)
        #-time line


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
        hours = ['07:20', '08:00', '09:00', '10:00', '11:00',
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
                    ha='center', va='bottom', rotation="horizontal", fontsize="large", color="w")

    def update_figure(self, fact, plan, hours, cur_hour):
        # We want the axes cleared every time plot() is called
        self.plt.cla()

        #hours = ['07:20', '08:00', '09:00', '10:00', '11:00',
         #        '12:00', '13:00', '14:00', '15:00']
        l = [0 for i in range(9)]
        l[cur_hour] = fact[cur_hour]
        width = 0.95
        ok = [0 for i in range(9)]
        nok = [0 for i in range(9)]
        for i in range(9):
            if (fact[i] > plan[i]) and (i != cur_hour):
                ok[i] = fact[i]
            else:
                nok[i] = fact[i]

        rect = self.plt.bar(hours, fact, color='b', label='текущий факт', align='edge', width=width, edgecolor='g')
        self.plt.bar(hours, ok, color='g', label='ok', align='edge', width=width)
        self.plt.bar(hours, nok, color='r', label='nok', align='edge', width=width)
        self.plt.bar(hours, l, color='b', align='edge', width=width)

        p = []
        for i in range(9):
            p.append(plan[i])

        h = [i for i in range(9)]
        for i in range(9):
            k = 2 * i
            h.insert(k + 1, i + width)
            p.insert(k, p[k])

        self.plt.plot(h, p, color='r', label='план')
        self.plt.grid(which='major', axis='y', linestyle='--')
        self.plt.tick_params('x', labelrotation=0, direction='in', pad=5, labelright='True')
        self.plt.set_title('Мониторинг выполнения цели в день')
        self.plt.set_xlabel('Время')
        self.plt.set_ylabel('Количество деталей')
        self.plt.legend()

        self.autolabel(rect)
        self.draw()


def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWin()
    form.show()
    #form.showFullScreen()
    # form.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
