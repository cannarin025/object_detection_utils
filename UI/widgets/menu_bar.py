from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class MenuBar(QtWidgets.QMenuBar):
    
    def __init__(self):
        super().__init__()
        #Menus
        self.file_menu = self.addMenu("File")
        self.action_open = QtWidgets.QAction()
        self.file_menu.addAction(self.action_open)
        self.action_open.setText("Open")
        
        self.view_menu = self.addMenu("View")

        self.example_menu = self.addMenu("Example")
        self.nested_menu = self.example_menu.addMenu("Nested menu")
        self.example_action = QtWidgets.QAction()
        self.nested_menu.addAction("Nested action")
        self.example_action.setText("Nested action")
