from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from src.ui.widgets.img_tab_menu import ImgTabMenu
from src.ui.widgets.menu_bar import MenuBar
from src.classes.filemanager import FileManager

import cv2

class ToolBar(QtWidgets.QWidget):

    def __init__(self):
        super(ToolBar, self).__init__()

        # layout
        self.layout = QtWidgets.QVBoxLayout()

        # widgets
        self.next_img = QtWidgets.QPushButton("Next img")
        self.prev_img = QtWidgets.QPushButton("Prev img")

        self.layout.addWidget(self.next_img)
        self.layout.addWidget(self.prev_img)

        self.setLayout(self.layout)