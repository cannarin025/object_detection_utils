from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import cv2
import os
import sys
import copy

from src.classes.labelled_img import Label

if sys.platform == "linux":
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")


class ImgDisplay(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    img_index = 0
    _drawing = False
    _cursor_pos = (None, None)
    _rects = []
    _labels = []
    #_painter = QtGui.QPainter()
    cursorMoved = QtCore.pyqtSignal(tuple)

    label_origin = QtCore.QPoint(0, 0)

    def __init__(self):
        super(ImgDisplay, self).__init__()
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._image = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._image)
        # self.qp = QtWidgets.QStylePainter()
        # self._scene.addWidget(self.qp)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self._image.mouseDoubleClickEvent = self.getPos

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.setImage(QtGui.QPixmap("D:/Code/Projects/object_detection_utils/src/ui/testing/image.jpg")) # testing
        self._drawing = True

    def hasImage(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._image.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasImage():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setImage(self, image: QtGui.QPixmap):
        self._zoom = 0
        self._empty = False
        #self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.enableDragMode()
        self._image.setPixmap(image)
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasImage():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            #     pass
            # elif self._zoom < 0:
            #     self.scale(factor,factor)
            else:
                self._zoom = 0

    # def toggleDragMode(self):
    #     if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
    #         self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
    #     elif not self._image.pixmap().isNull():
    #         self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def enableDragMode(self):
        if not self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def disableDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    # def paintEvent(self, event: QtGui.QPaintEvent) -> None:
    #     #qp = QtWidgets.QStylePainter()
    #     #qp.begin(self)
    #     br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
    #     self.qp.setBrush(br)
    #     #pic = QtGui.QPixmap("D:/Code/Projects/object_detection_utils/src/ui/testing/image.jpg") # testing
    #     #qp.drawPixmap(self.rect(), pic)
    #     self.qp.drawRect(40, 40, 400, 200)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if self._image.isUnderMouse():
            self._cursor_pos = (int(self.mapToScene(event.pos()).x()),
                                int(self.mapToScene(event.pos()).y()))
            if self._drawing:
                label_x1 = self._cursor_pos[0] #- 0.5
                label_y1 = self._cursor_pos[1] #- 0.5
                self.label_origin = QtCore.QPoint(label_x1, label_y1)
                #print(label_x1, label_y1)
            # #todo: delete testing feature
            # else:
            #     label_x1 = self._cursor_pos[0]  # - 0.5
            #     label_y1 = self._cursor_pos[1]  # - 0.5
            #     #point = QtCore.QPoint(label_x1, label_y1)
            #     rad = 1
            #     self._scene.addEllipse(label_x1 - rad, label_y1 - rad, rad * 2.0, rad * 2.0)
            #     self._scene.addPoint


    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.enableDragMode()
        if self._image.isUnderMouse():
            self._cursor_pos = (int(self.mapToScene(event.pos()).x()),
                                int(self.mapToScene(event.pos()).y()))
            if self._drawing and self.label_origin:
                label_x2 = self._cursor_pos[0] + 1 # +1 ensures that box appears to contain selected pixels
                label_y2 = self._cursor_pos[1] + 1
                #print(label_x2, label_y2)

                #correcting rect coordinates such that start is top right and end is bottom left
                width = abs(self.label_origin.x() - label_x2)
                height = abs(self.label_origin.y() - label_y2)
                label_start = self.label_origin
                if label_x2 >= self.label_origin.x() and label_y2 >= self.label_origin.y():
                    self.label_end = QtCore.QPoint(label_x2, label_y2)
                elif label_x2 <= self.label_origin.x() and label_y2 <= self.label_origin.y():
                    self.label_end = self.label_origin
                    label_start = QtCore.QPoint(label_x2, label_y2)
                elif label_x2 > self.label_origin.x() and label_y2 < self.label_origin.y():
                    self.label_end = QtCore.QPoint(label_x2, self.label_origin.y())
                    label_start = QtCore.QPoint(self.label_origin.x(), self.label_origin.y() - height)
                elif label_x2 < self.label_origin.x() and label_y2 > self.label_origin.y():
                    self.label_end = QtCore.QPoint(self.label_origin.x(), label_y2)
                    label_start = QtCore.QPoint(self.label_origin.x() - width, self.label_origin.y())


                rect = QtCore.QRectF(label_start, self.label_end)
                rect_item = self._scene.addRect(rect, Qt.green)
                if len(self._rects) > 1:
                    #print(self._rects)
                    #print(self._scene.items())
                    self._scene.removeItem(self._rects.pop())
                self._rects.append(rect_item)

        self.cursorMoved.emit(self._cursor_pos)


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self._image.isUnderMouse():
            self._cursor_pos = (int(self.mapToScene(event.pos()).x()),
                                int(self.mapToScene(event.pos()).y()))
            if self._drawing:
                label_x2 = self._cursor_pos[0]
                label_y2 = self._cursor_pos[1]
                print(label_x2, label_y2)

            # # correcting rect coordinates such that start is top right and end is bottom left
            # width = abs(self.label_start.x() - label_x2)
            # height = abs(self.label_start.y() - label_y2)
            # if label_x2 >= self.label_start.x() and label_y2 >= self.label_start.y():
            #     self.label_end = QtCore.QPoint(label_x2, label_y2)
            # elif label_x2 <= self.label_start.x() and label_y2 <= self.label_start.y():
            #     self.label_end = copy.copy(self.label_start)
            #     self.label_start = QtCore.QPoint(label_x2, label_y2)
            # elif label_x2 > self.label_start.x() and label_y2 < self.label_start.y():
            #     self.label_end = QtCore.QPoint(label_x2, self.label_start.y())
            #     self.label_start = QtCore.QPoint(self.label_start.x(), self.label_start.y() - height)
            # elif label_x2 < self.label_start.x() and label_y2 > self.label_start.y():
            #     self.label_end = QtCore.QPoint(self.label_start.x(),label_y2)
            #     self.label_start = QtCore.QPoint(self.label_start.x() - width, self.label_start.y())
            #
            #
            # r = QtCore.QRectF(self.label_start, self.label_end)
            # self._scene.addRect(r)

    def getPos(self, event): # demo function
        x = int(event.pos().x())
        y = int(event.pos().y())
        print("img coords x:", x, "y:", y)

    def correct_rect_coords(self, start: QtCore.QPoint, end: QtCore.QPoint) -> None:
        """"A function to compare the start and end coordinates of a rectangle and adjust them accordingly"""
        width = abs(end.x() - start.x())
        height = abs(end.y() - start.y())
        if end.x() > start.x() and end.y() > start.y():
            pass
        elif start.x() > end.x() and start.y() > end.y():
            end = start
        else:
            self.label_end = self.label_origin
            self.label_origin = QtCore.QPoint(label_x2, label_y2)

