from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFile, Qt
import cv2

#from src.ui.main_window import window
from src.ui.widgets.image_display import ImgDisplayWidget

import os

class MenuBar(QtWidgets.QMenuBar):

    #signals
    dir_opened = QtCore.pyqtSignal(str)

    def __init__(self):

        super().__init__()

        #Menus
        # File menu
        self.file_menu = self.addMenu("File")

        self.action_open_folder = QtWidgets.QAction("Open Folder")
        self.file_menu.addAction(self.action_open_folder)
        self.action_open_folder.setShortcut("Ctrl+O")
        self.action_open_folder.triggered.connect(self.open_folder_click)

        self.action_open_file = QtWidgets.QAction("Open File")
        self.file_menu.addAction(self.action_open_file)
        #self.action_open.setText("Open")
        self.action_open_file.setShortcut('Ctrl+Shift+O')
        self.action_open_file.triggered.connect(self.open_files)



        # View menu
        self.view_menu = self.addMenu("View")



        # Example menu
        self.example_menu = self.addMenu("Example")
        self.nested_menu = self.example_menu.addMenu("Nested menu")
        self.example_action = QtWidgets.QAction()
        self.nested_menu.addAction("Nested action")
        self.example_action.setText("Nested action")


    def open_folder_click(self):
        dirpath = QFileDialog.getExistingDirectory()
        if dirpath:
            self.dir_opened.emit(dirpath)

    def open_files(self):
        print("opening file")
        fnames = QFileDialog.getOpenFileNames()
        print(fnames)
        file_exts = []
        for fname in fnames[0]:
            file_exts.append(os.path.splitext(os.path.basename(fname))[1])

        if all(ext in [".png", ".jpg"] for ext in file_exts):
            pass

        else:
            # todo: this does not appear unless run in debug mode
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Files must be image files with .jpg or .png extensions!")
            #error_dialog.setFocus()
