from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from src.ui.widgets.img_tab_menu import ImgTabMenu
from src.ui.widgets.menu_bar import MenuBar
from src.classes.filemanager import FileManager

import cv2

class ToolBar(QtWidgets.QWidget):

    def __init__(self, img_tab_menu: ImgTabMenu, filemanager: FileManager):
        super(ToolBar, self).__init__()
        self.img_tab_menu = img_tab_menu
        self.filemanager = filemanager

        # layout
        self.layout = QtWidgets.QVBoxLayout()

        # widgets
        self.next_img = QtWidgets.QPushButton("Next img")
        self.next_img.clicked.connect(lambda: self.set_next_img())
        self.prev_img = QtWidgets.QPushButton("Prev img")
        self.prev_img.clicked.connect(lambda: self.set_prev_img())

        self.layout.addWidget(self.next_img)
        self.layout.addWidget(self.prev_img)

        self.setLayout(self.layout)

    def set_next_img(self):
        if self.img_tab_menu.get_current_tab().img_index < len(self.filemanager.filepaths) - 1:
            self.img_tab_menu.get_current_tab().img_index += 1
            self.img_tab_menu.get_current_tab().set_img(cv2.imread(self.filemanager.dirpath + "/" + self.filemanager.filepaths[self.img_tab_menu.get_current_tab().img_index]))

    def set_prev_img(self):
        if self.img_tab_menu.get_current_tab().img_index > 0:
            self.img_tab_menu.get_current_tab().img_index -= 1
            self.img_tab_menu.get_current_tab().set_img(cv2.imread(self.filemanager.dirpath + "/" + self.filemanager.filepaths[self.img_tab_menu.get_current_tab().img_index]))

