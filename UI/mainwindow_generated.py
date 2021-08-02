# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_template.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1248, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tool_menu = QtWidgets.QToolBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_menu.sizePolicy().hasHeightForWidth())
        self.tool_menu.setSizePolicy(sizePolicy)
        self.tool_menu.setMinimumSize(QtCore.QSize(118, 0))
        self.tool_menu.setBaseSize(QtCore.QSize(0, 0))
        self.tool_menu.setObjectName("tool_menu")
        self.label_page = QtWidgets.QWidget()
        self.label_page.setGeometry(QtCore.QRect(0, 0, 107, 74))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_page.sizePolicy().hasHeightForWidth())
        self.label_page.setSizePolicy(sizePolicy)
        self.label_page.setObjectName("label_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.label_page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.label_page)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_4 = QtWidgets.QPushButton(self.label_page)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.tool_menu.addItem(self.label_page, "")
        self.transform_tools = QtWidgets.QWidget()
        self.transform_tools.setGeometry(QtCore.QRect(0, 0, 107, 74))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transform_tools.sizePolicy().hasHeightForWidth())
        self.transform_tools.setSizePolicy(sizePolicy)
        self.transform_tools.setObjectName("transform_tools")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.transform_tools)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.transform_tools)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.transform_tools)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.tool_menu.addItem(self.transform_tools, "")
        self.dir_tools = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dir_tools.sizePolicy().hasHeightForWidth())
        self.dir_tools.setSizePolicy(sizePolicy)
        self.dir_tools.setObjectName("dir_tools")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dir_tools)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_5 = QtWidgets.QPushButton(self.dir_tools)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_3.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.dir_tools)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_3.addWidget(self.pushButton_6)
        self.tool_menu.addItem(self.dir_tools, "")
        self.horizontalLayout_2.addWidget(self.tool_menu)
        self.image_tab_menu = QtWidgets.QTabWidget(self.centralwidget)
        self.image_tab_menu.setObjectName("image_tab_menu")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.image_tab_menu.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.image_tab_menu.addTab(self.tab_2, "")
        self.horizontalLayout_2.addWidget(self.image_tab_menu)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1248, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tool_menu.setCurrentIndex(2)
        self.image_tab_menu.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.tool_menu.setItemText(self.tool_menu.indexOf(self.label_page), _translate("MainWindow", "Label Tools"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
        self.tool_menu.setItemText(self.tool_menu.indexOf(self.transform_tools), _translate("MainWindow", "Transform Tools"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton"))
        self.tool_menu.setItemText(self.tool_menu.indexOf(self.dir_tools), _translate("MainWindow", "Page"))
        self.image_tab_menu.setTabText(self.image_tab_menu.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.image_tab_menu.setTabText(self.image_tab_menu.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())