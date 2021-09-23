from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from src.ui.widgets.pixmaptest import PixMap
from src.ui.widgets.image_display import ImgDisplay

import cv2
import os
import sys

if sys.platform == "linux":
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

class ImgViewer(QtWidgets.QWidget):

    img_index: int = 0
    img: QtGui.QPixmap

    def __init__(self):
        super(ImgViewer, self).__init__()
        
        #self.container = QtWidgets.QFrame()
        self.layout = QtWidgets.QVBoxLayout()
        self.button = QtWidgets.QPushButton("test")

        self.display = ImgDisplay()
        #self.display.mouseDoubleClickEvent = self.getPos

        #self.scroll = QtWidgets.QScrollArea()
        #self.scroll.setWidgetResizable(True)
        #self.scroll.setWidget(self.display)
        #self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.display)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.drawing = False
        self.button.clicked.connect(lambda: self.test_func())

    def test_func(self):
            self.set_img(cv2.imread("C:/Users/canna/OneDrive/Pictures/pepega.png"))
            #self.drawing = True

    def set_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #cv2.imshow("test", img)
        self.img = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        #self.img = img.scaled(2000, 2000, Qt.KeepAspectRatio)
        #self.display.resize(img.width(), img.height())
        #pImg = PixMap.load("C:/Users/canna/OneDrive/Pictures/pepega.png")
        #self.display.setMaximumSize(self.img.width(), self.img.height())
        self.display.setImage(QtGui.QPixmap.fromImage(self.img))
        #print(self.display.pixmap())

    def getPos(self, event): # demo function
        x = event.pos().x()
        y = event.pos().y()
        print("img coords x:", x, "y:", y)
        #print(QtGui.QColor(self.img.pixel(x,y)).getRgb())
        #return (x,y)

    # def mousePressEvent(self, event):
    #     self.drawing = True
    #     if self.drawing:
    #         if event.button() == 1:
    #             x0 = event.x()
    #             y0 = event.y()
    #             print("start:", x0, y0)
    #
    # def mouseMoveEvent(self, event):
    #     if self.drawing:
    #         x1 = event.x()
    #         y1 = event.y()
    #         print("end:", x1, y1)
    #
    # def mouseReleaseEvent(self, event):
    #     if event.button() == 1:
    #         self.drawing = False

    # def draw_label(self):
    #     self.display.mousePressEvent = self.getPos
    #     #coords = self.display.mousePressEvent.pos()
    #     # mouseup = self.display.mouseReleaseEvent()
    #     # label_coords = (mousedown.pos().x,
    #     #                 mousedown.pos().y,
    #     #                 mouseup.pos().x,
    #     #                 mouseup.pos().y)
    #
    #     print("label_coords", self.display.mousePressEvent)
