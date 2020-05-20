
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

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

config_file = 'Config.xml'


class RobThreadClass(QtCore.QThread):

    date_signal = QtCore.pyqtSignal(str)
    shift_num_signal = QtCore.pyqtSignal(str)
    graph_signal = QtCore.pyqtSignal(list, list, list, int)
    hours_signal = QtCore.pyqtSignal(list)
    plan_signal = QtCore.pyqtSignal(int)
    bdt_signal = QtCore.pyqtSignal(str)

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
        current_hour = 0
        while 1:
            current_date = self.request('Date')
            if current_date:
                self.date_signal.emit(current_date)

            bdt = self.request('BDT')
            if bdt:
                self.bdt_signal.emit(bdt)

            count = self.request('Count')
            plan = int(self.request('Plan'))
            shift_num = self.request('Nshift')
            current_time = self.request('Time')

            if plan and count and shift_num and current_time:
                current_hour = int(current_time[0:2])

                if shift_num == '1':
                    current_hour = current_hour - 7
                elif shift_num == '2':
                    if current_hour != 0:
                        current_hour = current_hour - 16
                    else:
                        current_hour = 8
                elif shift_num == '3':
                    pass
                else:
                    pass

                if (current_hour > 8) or (current_hour < 0):
                    current_hour = 0

                hour_counters = count.split('/')
                counter_array = []
                for counter in hour_counters:
                    counter_array.append(int(counter))

                available_minutes = []
                intervals = []
                if int(shift_num) == 1:
                    available_minutes, intervals = self.config.shift1()
                elif int(shift_num) == 2:
                    available_minutes, intervals = self.config.shift2()
                elif int(shift_num) == 3:
                    available_minutes, intervals = self.config.shift3()

                total_time = 0
                for available_minute in available_minutes.split('/'):
                    total_time = total_time + int(available_minute)
                time_per_peace = total_time / plan
                plan_array = []
                for available_minute in available_minutes.split('/'):
                    plan_array.append(round(int(available_minute)/time_per_peace))

                round_deviation = sum(plan_array) - plan
                plan_array[-1] = plan_array[-1] - round_deviation
                hours = []
                for interval in intervals.split('/'):
                    hours.append(interval.split('-')[0])

                self.hours_signal.emit(intervals.split('/'))
                self.graph_signal.emit(counter_array, plan_array, hours, current_hour)
                self.shift_num_signal.emit(shift_num)
                self.plan_signal.emit(plan)
            time.sleep(1)


class MainWin(QMainWindow, MainWindow.Ui_MainWindow):

    def showdate(self,  date: str):
        self.time.setText(date)

    def showshift(self, shift: str):
        self.shift.setText('Смена № %s' % shift)

    def show_plan(self, plan: int):
        self.label_5.setText('Количество за смену: %s' %plan)

    def show_bdt(self, bdt: int):
        self.label_4.setText('BDT: %s сек.' %bdt)

    def showlabels(self,
                   fact_label: QLabel,
                   plan_label: QLabel,
                   fact: int, plan: int,
                   sum_plan: int,
                   cur_hour: int,
                   order: int):

        plan_label.setText('%s / %s' % (str(plan), str(sum_plan)))
        fact_label.setText(str(fact))
        if fact < sum_plan:
            fact_label.setStyleSheet("background-color:red;")
        else:
            fact_label.setStyleSheet("background-color:green;")
        if order == cur_hour and fact < sum_plan:
            fact_label.setStyleSheet("background-color:blue;")
        elif order > cur_hour:
            fact_label.setStyleSheet(" ")
            fact_label.setText('')

    def plot(self, fact, plan, hours, cur_hour):
        self.dc.update_figure(fact, plan, hours, cur_hour)
        self.showlabels(self.fact, self.plan, fact[0], plan[0], plan[0], cur_hour, 0)
        self.showlabels(self.fact_2, self.plan_2, sum(fact[0:2]), plan[1], sum(plan[0:2]), cur_hour, 1)
        self.showlabels(self.fact_3, self.plan_3, sum(fact[0:3]), plan[2], sum(plan[0:3]), cur_hour, 2)
        self.showlabels(self.fact_4, self.plan_4, sum(fact[0:4]), plan[3], sum(plan[0:4]), cur_hour, 3)
        self.showlabels(self.fact_5, self.plan_5, sum(fact[0:5]), plan[4], sum(plan[0:5]), cur_hour, 4)
        self.showlabels(self.fact_6, self.plan_6, sum(fact[0:6]), plan[5], sum(plan[0:6]), cur_hour, 5)
        self.showlabels(self.fact_7, self.plan_7, sum(fact[0:7]), plan[6], sum(plan[0:7]), cur_hour, 6)
        self.showlabels(self.fact_8, self.plan_8, sum(fact[0:8]), plan[7], sum(plan[0:8]), cur_hour, 7)
        self.showlabels(self.fact_9, self.plan_9, sum(fact), plan[8], sum(plan), cur_hour, 8)

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
        self.robthread.plan_signal.connect(self.show_plan)
        self.robthread.bdt_signal.connect(self.show_bdt)
        config = XmlParser.ConfigParse(config_file)
        logopixmap = QPixmap(config.logopicture())
        self.label_2.setText(config.logotext())
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
        self.plt.tick_params('x', labelrotation=0)
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
            if height > 0:
                self.plt.text(rect.get_x() + rect.get_width() / 2., 0.5 * height,
                        '%d' % int(height),
                        ha='center', va='bottom', rotation="horizontal", fontsize="large", color="black")

    def update_figure(self, fact, plan, hours, cur_hour):
        # We want the axes cleared every time plot() is called
        self.plt.cla()
        l = [0 for i in range(9)]
        l[cur_hour] = fact[cur_hour]
        width = 0.95

        ok = [0 for i in range(9)]
        nok = [0 for i in range(9)]
        for i in range(9):
            if fact[i] >= plan[i]:
                ok[i] = fact[i]
            else:
                nok[i] = fact[i]

        print(fact)
        rect = self.plt.bar(hours, fact, color='b', label='текущий факт', align='edge', width=width, edgecolor='g')
        self.plt.bar(hours, ok, color='g', label='ok', align='edge', width=width)
        self.plt.bar(hours, nok, color='r', label='nok', align='edge', width=width)
        if fact[cur_hour] < plan[cur_hour]:
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
    # form.showFullScreen()
    # form.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
