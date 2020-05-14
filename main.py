
import RobClient
import time
import MainWindow
import sys

# This gets the Qt stuff
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui


class RobThreadClass(QtCore.QThread):

    date_signal = QtCore.pyqtSignal(str)

    def __init__(self):

        super(self.__class__, self).__init__()
        self.rob = RobClient.Client('localhost', 10000)

    def run(self):
        current_date = ''
        while 1:
            #print(self.rob.request('1'), self.rob.connected)
            #time.sleep(5)
            current_date = self.rob.request('Date')
            print(current_date.decode('utf-8'))
            self.date_signal.emit(current_date.decode('utf-8'))
            time.sleep(1)


class MainWin(QMainWindow, MainWindow.Ui_MainWindow):

    def showdate(self,  date: str):
        self.time.setText(date)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file

        self.robthread = RobThreadClass()
        self.robthread.start()
        self.robthread.date_signal.connect(self.showdate)


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
