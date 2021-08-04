from PyQt5 import QtCore, QtGui, QtWidgets
from src.ui.widgets.img_tab_menu import ImgTabMenu
from src.ui.widgets.menu_bar import MenuBar
from src.ui.widgets.tool_bar import ToolBar
from src.classes.filemanager import FileManager
import os
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(1248, 600)

        self.filemanager = FileManager()

        self.container = QtWidgets.QFrame()
        self.container.setObjectName("container")
        self.layout = QtWidgets.QHBoxLayout()

        self.tab_menu = ImgTabMenu()
        # self.tab_menu = CustomTabWidget()

        self.menu_bar = MenuBar(self.tab_menu, self.filemanager)
        self.setMenuBar(self.menu_bar)

        self.tool_bar = ToolBar(self.tab_menu, self.filemanager)

        self.test_button = QtWidgets.QPushButton("Press Me!")
        self.test_button.clicked.connect(lambda: print(self.tab_menu.get_tab_names()))

        self.layout.addWidget(self.tab_menu)
        self.layout.addWidget(self.test_button)
        self.layout.addWidget(self.tool_bar)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
