from PyQt5 import QtCore, QtGui, QtWidgets
from src.ui.widgets.img_tab_menu import ImgTabMenu
from src.ui.widgets.menu_bar import MenuBar
from src.ui.widgets.tool_bar import ToolBar
from src.classes.filemanager import FileManager
import os
import sys
import cv2


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

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)
        self.menu_bar.dir_opened.connect(lambda dirpath: self.open_folder(dirpath))

        self.tool_bar = ToolBar()
        self.tool_bar.next_img.clicked.connect(self.show_next_img)
        self.tool_bar.prev_img.clicked.connect(self.show_prev_img)

        self.test_button = QtWidgets.QPushButton("Press Me!")
        self.test_button.clicked.connect(lambda: print(self.tab_menu.get_tab_names()))

        self.layout.addWidget(self.tab_menu)
        self.layout.addWidget(self.test_button)
        self.layout.addWidget(self.tool_bar)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.show()

    def signal_test(self, a):
        print("Test signal recieved", a)

    def open_folder(self, dirpath):
        self.filemanager.open_dir(dirpath)
        current_tab = self.tab_menu.widget(self.tab_menu.currentIndex())
        current_tab.set_img(
            cv2.imread(
                self.filemanager.dirpath + "/" + self.filemanager.filepaths[self.tab_menu.get_current_tab().img_index]
            )
        )

    def show_next_img(self):
        if self.tab_menu.get_current_tab().img_index < len(self.filemanager.filepaths) - 1:
            self.tab_menu.get_current_tab().img_index += 1
            self.tab_menu.get_current_tab().set_img(
                cv2.imread(
                    self.filemanager.dirpath + "/" + self.filemanager.filepaths[self.tab_menu.get_current_tab().img_index]
                )
            )

    def show_prev_img(self):
        if self.tab_menu.get_current_tab().img_index > 0:
            self.tab_menu.get_current_tab().img_index -= 1
            self.tab_menu.get_current_tab().set_img(
                cv2.imread(
                    self.filemanager.dirpath + "/" + self.filemanager.filepaths[self.tab_menu.get_current_tab().img_index]
                )
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
