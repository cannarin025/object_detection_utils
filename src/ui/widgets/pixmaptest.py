from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class PixMap(QtGui.QPixmap):
    def __init__(self):
        super(PixMap, self).__init__()
        self.drawing = False

    def mousePressEvent(self, event):
        self.drawing = True
        if self.drawing:
            if event.button() == 1:
                x0 = event.x()
                y0 = event.y()
                print("start:", x0, y0)

    def mouseMoveEvent(self, event):
        if self.drawing:
            x1 = event.x()
            y1 = event.y()
            print("end:", x1, y1)

    def mouseReleaseEvent(self, event):
        if event.button() == 1:
            self.drawing = False
