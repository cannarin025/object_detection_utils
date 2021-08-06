from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFile, Qt
import cv2

from src.ui.widgets.img_tab_menu import ImgTabMenu
from src.classes.filemanager import FileManager

#from src.ui.main_window import window
from src.ui.widgets.image_display import ImgDisplayWidget

import os

class MenuBar(QtWidgets.QMenuBar):

    def __init__(self, img_tab_menu: ImgTabMenu, filemanager: FileManager):
        super().__init__()

        self.img_tab_menu = img_tab_menu
        self.filemanager = filemanager

        #Menus
        # File menu
        self.file_menu = self.addMenu("File")

        self.action_open_folder = QtWidgets.QAction("Open Folder")
        self.file_menu.addAction(self.action_open_folder)
        self.action_open_folder.setShortcut("Ctrl+O")
        self.action_open_folder.triggered.connect(self.open_folder)

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


    def open_folder(self):
        dirpath = QFileDialog.getExistingDirectory()
        if dirpath:
            self.filemanager.dirpath = dirpath
            self.filemanager.filepaths = [x for x in os.listdir(dirpath) if x.endswith((".jpg", ".png"))]

            if isinstance(self.img_tab_menu.widget(self.img_tab_menu.currentIndex()), ImgDisplayWidget):
                current_tab = self.img_tab_menu.widget(self.img_tab_menu.currentIndex())
                current_tab.set_img(cv2.imread(dirpath + "/" + self.filemanager.filepaths[self.img_tab_menu.get_current_tab().img_index]))

        else:
           # add img_display tab first and then display image
           pass

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
