from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from src.ui.widgets.pixmaptest import PixMap
from src.ui.widgets.tab import Tab
from src.ui.widgets.image_display import ImgDisplay

import cv2
import os
import sys

if sys.platform == "linux":
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")


class ImgTab(Tab):
    img_index: int = 0

    def __init__(self):
        super(ImgTab, self).__init__()

        # self.container = QtWidgets.QFrame()
        self._layout = QtWidgets.QVBoxLayout()
        self._coord_label = QtWidgets.QLabel("--:--")
        self._test_button = QtWidgets.QPushButton("test button")
        self._display = ImgDisplay()

        self._layout.addWidget(self._display)
        self._layout.addWidget(self._coord_label)
        self._layout.addWidget(self._test_button)
        self.setLayout(self._layout)

        self.drawing = False
        self._test_button.clicked.connect(lambda: self.test_func())
        self._display.cursorMoved.connect(lambda cursor_pos: self.log_cursor_coords(cursor_pos))

    def test_func(self):
        self.set_img(cv2.imread("C:/Users/canna/OneDrive/Pictures/pepega.png"))
        # self.drawing = True

    def set_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self._display.setImage(QtGui.QPixmap.fromImage(self.img))

    def log_cursor_coords(self, cursor_pos):
        if cursor_pos != (None, None):
            self._coord_label.setText(f"x:{cursor_pos[0]} y:{cursor_pos[1]}")
        else:
            self._coord_label.setText(f"x:-- y:--")


