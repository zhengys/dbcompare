#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class DataConnection(QGridLayout):
    dataBaseType=None
    host=None
    port=None
    databaseName=None
    user=None
    password=None
    charset=None
    #typeList = ["oracle","sqlserver","mysql","access","db2","postgresql","sqlite"]
    #portList = ["1521","1433","3306","80","50000","5432","80"]
    
    typeList = ["oracle","sqlserver","mysql"]
    portList = ["1521","1433","3306"]

    def __init__(self,parent=None):
        super(QGridLayout, self).__init__()
        
        self.hbox = QHBoxLayout(parent)
        
        
        dataBaseTypeLabel = QLabel("DataBse Type:")
        self.dataBaseComboBox = QComboBox()
        
        self.dataBaseComboBox.addItem("Oracle")
        self.dataBaseComboBox.addItem("Microsoft SQL Server")
        self.dataBaseComboBox.addItem("MySQL")
        #self.dataBaseComboBox.addItem("Microsoft Access")
        #self.dataBaseComboBox.addItem("DB2")
        #self.dataBaseComboBox.addItem("PostgreSQL")
        #self.dataBaseComboBox.addItem("SQLite")
        
        self.connect(self.dataBaseComboBox, SIGNAL('activated(QString)'),self.onActivated)

        
        hostLabel = QLabel("Host:")
        self.hostLine = QLineEdit()
        self.hostLine.setMaxLength(50)
        
        portLabel = QLabel("Port:")
        self.portLine = QLineEdit()
        self.portLine.setMaxLength(10)
        qRegExp = QRegExp("[0-9]+$")
        self.portLine.setValidator(QRegExpValidator(qRegExp,self.portLine))

        dataBaseNameLabel = QLabel("DataBase Name:")
        self.dataBaseNameLine = QLineEdit()
        self.dataBaseNameLine.setMaxLength(50)
        
        userLabel = QLabel("user:")
        self.userLine = QLineEdit()
        self.userLine.setMaxLength(50)
        
        passwordLabel = QLabel("password:")
        self.passwordLine = QLineEdit()
        self.passwordLine.setEchoMode(QtGui.QLineEdit.Password) 
        self.passwordLine.setMaxLength(50)

        self.addWidget(dataBaseTypeLabel, 0, 0)
        self.addWidget(self.dataBaseComboBox, 0, 1)
        self.addWidget(hostLabel, 1, 0, Qt.AlignTop)
        self.addWidget(self.hostLine, 1, 1)
        self.addWidget(portLabel, 2, 0, Qt.AlignTop)
        self.addWidget(self.portLine,2, 1)
        self.addWidget(dataBaseNameLabel, 3, 0, Qt.AlignTop)
        self.addWidget(self.dataBaseNameLine, 3, 1)
        self.addWidget(userLabel, 4, 0, Qt.AlignTop)
        self.addWidget(self.userLine, 4, 1)
        self.addWidget(passwordLabel, 5, 0, Qt.AlignTop)
        self.addWidget(self.passwordLine, 5, 1)
        
        self.dataBaseComboBox.setCurrentIndex(2)
        self.portLine.setText(self.portList[self.dataBaseComboBox.currentIndex()])
        
    def onActivated(self, text):
        self.portLine.setText(self.portList[self.dataBaseComboBox.currentIndex()])

    def getDataBaseType(self):
        self.dataBaseType=self.typeList[self.dataBaseComboBox.currentIndex()]
        return self.dataBaseType
    def getHost(self):
        self.host=str(self.hostLine.text())
        return self.host
    def getPort(self):
        self.port=int(str(self.portLine.text()))
        return self.port
    def getDatabaseName(self):
        self.databaseName=str(self.dataBaseNameLine.text())
        return self.databaseName
    def getUser(self):
        self.user=str(self.userLine.text())
        return self.user
    def getPassword(self):
        self.password=str(self.passwordLine.text())
        return self.password
    def isInputed(self):
        self.host=str(self.hostLine.text())
        self.port=int(str(self.portLine.text()))
        self.databaseName=str(self.dataBaseNameLine.text())
        self.user=str(self.userLine.text())
        if len(self.host)<=0 or len(self.databaseName)<=0 or len(self.user)<=0:
            return False
        return True
