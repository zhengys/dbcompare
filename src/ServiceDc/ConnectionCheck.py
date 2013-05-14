# -*- coding: utf-8 -*-

import sys

import threading
import pdbc.DriverManager as dr
from PyQt4 import QtCore, QtGui

class ConnectionCheck(QtCore.QThread):
    check=QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self) #没有parent参数
        self.moveToThread(self)

    def run(self):
        print ''
        html='55555555555555555555'
        self.check.emit(self.connectInfo(True,True))
    def __del__(self):
        self.wait()

    def connectInfo(self,left,right): 
        info = ""
        if left==None and right==None:
            info = 'all database connect Failed!'
        elif left!=None and right!=None:
            info = 'all database connect Success!'
        elif left!=None and right==None:
            info = 'left database connect Success!'
            info += '\n'
            info = 'right database connect Failed!'
        elif left==None and right!=None:
            info = 'left database connect Failed!'
            info += '\n'
            info = 'right database connect Success!'
        return info