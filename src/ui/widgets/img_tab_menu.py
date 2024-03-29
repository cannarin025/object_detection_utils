from PyQt5 import QtWidgets
import re

from src.ui.widgets.image_display import ImgDisplay
from src.ui.widgets.image_tab import ImgTab

class ImgTabMenu(QtWidgets.QTabWidget):

    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)

        self.add_tab_button = QtWidgets.QToolButton()
        self.add_tab_button.setText('+')
        font = self.add_tab_button.font()
        font.setBold(True)
        self.add_tab_button.setFont(font)
        self.setCornerWidget(self.add_tab_button)

        self.add_tab_button.clicked.connect(lambda: self.add_tab())
        self.tabCloseRequested.connect(lambda index: self.remove_tab(index)) # enables tabs to be closed

        self.add_tab()
    
    def add_tab(self, tab_name: str = None):
        if tab_name is None:
            
            # assigns first available tab name if one is not assigned
            tab_numbers = [int(x[3:]) for x in self.get_tab_names() if re.match(r"tab\d+", x)]
            first_free_num = 1
            while first_free_num in tab_numbers:
                first_free_num += 1
            
            tab_name = f"tab{first_free_num}"

        tab = ImgTab()
        self.addTab(tab, tab_name)

    def remove_tab(self, index):
        self.removeTab(index)

        #iterates over widgets in tabs
        for i in range(self.count()):
            print(self.widget(i))

        if self.count() == 0:
            welcome_tab = QtWidgets.QWidget()  # create a welcome tab to default to if no other tabs exist with contents that serve as instructions
            self.addTab(welcome_tab, "Welcome!")

    def get_current_tab(self):
        return self.widget(self.currentIndex())

    def set_tab_name(self): # unnecessary
        self.setTabText(self.currentIndex(), "test")

    def get_tab_names(self):
        tab_names = []
        for i in range(self.count()):
            tab_names.append(self.tabText(i))
        
        return tab_names
            
