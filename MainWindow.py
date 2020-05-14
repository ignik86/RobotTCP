# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(827, 613)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalWidget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.time = QtWidgets.QLabel(self.horizontalWidget)
        self.time.setObjectName("time")
        self.horizontalLayout_4.addWidget(self.time)
        self.label_2 = QtWidgets.QLabel(self.horizontalWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.widget = QtWidgets.QWidget(self.horizontalWidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4.addWidget(self.widget)
        self.verticalLayout.addWidget(self.horizontalWidget)
        self.horizontalWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalWidget_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.horizontalWidget_2.setObjectName("horizontalWidget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.horizontalWidget_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.horizontalWidget_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.label_5 = QtWidgets.QLabel(self.horizontalWidget_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.verticalLayout.addWidget(self.horizontalWidget_2)
        self.horizontalWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalWidget_3.setObjectName("horizontalWidget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graph = QtWidgets.QWidget(self.horizontalWidget_3)
        self.graph.setObjectName("graph")
        self.horizontalLayout_2.addWidget(self.graph)
        self.verticalLayout.addWidget(self.horizontalWidget_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 827, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.time.setText(_translate("MainWindow", "date-time"))
        self.label_2.setText(_translate("MainWindow", "Project"))
        self.label_4.setText(_translate("MainWindow", "BDT"))
        self.label_3.setText(_translate("MainWindow", "номер смены"))
        self.label_5.setText(_translate("MainWindow", "количество за смену"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

