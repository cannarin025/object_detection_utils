from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import re

from widgets.tab import Tab

class TabMenu(QtWidgets.QTabWidget):
#class TabMenu(QtWidgets.QTabBar):

    tab_list: List[Tab] = []

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

        self.add_tab_button.clicked.connect(lambda: self.add_tab(Tab))
        self.tabCloseRequested.connect(lambda index: self.remove_tab(index)) # enables tabs to be closed

        self.add_tab(Tab)
    
    def add_tab(self, new_tab: Tab, tab_name: str = None):
        if tab_name is None:
            
            # assigns first available tab name if one is not assigned
            tab_numbers = [int(x.tab_name[3:]) for x in self.tab_list if re.match(r"tab\d+", x.tab_name)]
            first_free_num = 1
            while first_free_num in tab_numbers:
                first_free_num += 1
            
            tab_name = f"tab{first_free_num}"

        tab = new_tab(tab_name)
        self.addTab(tab, tab_name)
        self.tab_list.append(tab)
        #print(self.tab_list)

    def remove_tab(self, index):
        self.removeTab(index)
        self.tab_list.pop(index)
        #print(self.tab_list)
        for i in range(self.count()):
            print(self.widget(i))
            
