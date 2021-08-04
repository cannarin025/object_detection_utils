from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import cv2
import os
import sys

if sys.platform == "linux":
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

class ImgDisplayWidget(QtWidgets.QWidget):

    img_index: int = 0

    def __init__(self):
        super(ImgDisplayWidget, self).__init__()
        
        #self.container = QtWidgets.QFrame()
        self.layout = QtWidgets.QVBoxLayout()
        self.button = QtWidgets.QPushButton("test")
        self.display = QtWidgets.QLabel()
        self.layout.addWidget(self.display)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(lambda: self.set_img(cv2.imread("C:/Users/canna/OneDrive/Pictures/pepega.png")))

    def set_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        img = img.scaled(2000, 2000, Qt.KeepAspectRatio)
        #self.display.resize(img.width(), img.height())
        self.display.setPixmap(QtGui.QPixmap.fromImage(img))