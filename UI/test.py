from PyQt5 import QtCore, QtGui, QtWidgets
from widgets.TabMenu import TabMenu
import os
import sys

class TestWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(1248, 600)

        self.container = QtWidgets.QFrame()
        self.container.setObjectName("container")
        self.layout = QtWidgets.QVBoxLayout()

        self.tab_menu = TabMenu()
        self.layout.addWidget(self.tab_menu)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TestWindow()
    sys.exit(app.exec_())
