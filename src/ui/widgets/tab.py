from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import re

class Tab(QtWidgets.QWidget):
    """
    Tab baseclass for use with TabMenu
    """

    def __init__(self, tab_name: str = None):
        super().__init__()
        
        self.tab_name: str = tab_name
            