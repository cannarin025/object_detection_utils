from PyQt5 import QtCore, QtGui, QtWidgets
from widgets.TabMenu import TabMenu
from widgets.img_tab_menu import ImgTabMenu
from widgets.menu_bar import MenuBar
import os
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(1248, 600)
        
        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)

        self.container = QtWidgets.QFrame()
        self.container.setObjectName("container")
        self.layout = QtWidgets.QVBoxLayout()

        self.tab_menu = ImgTabMenu()
        #self.tab_menu = CustomTabWidget()

        self.test_button = QtWidgets.QPushButton("Press Me!")
        self.test_button.clicked.connect(lambda: print(self.tab_menu.get_tab_names()))

        self.layout.addWidget(self.tab_menu)
        self.layout.addWidget(self.test_button)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
