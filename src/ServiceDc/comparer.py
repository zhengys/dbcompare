# -*- coding: utf-8 -*-
# Copyright (c) 2013 zyskm <zyskm@163.com>
#
import sys

import threading
import pdbc.DriverManager as dr
import ServiceDc.DbCompare as cp
from PyQt4 import QtCore, QtGui
import logging  

class EventObject(QtCore.QObject):
    event = QtCore.pyqtSignal(str)
    callback=None
    def __init__(self,callback):       
        super(EventObject, self).__init__() 
        self.callback=callback
        self.event.connect(callback) 
    def emitter(self,info):  
        self.event.emit(info) 
        
def getDriver(conn):
    dbtype = conn.getDataBaseType()
    dbname = conn.getDatabaseName()
    host = conn.getHost()
    port = conn.getPort()
    user = conn.getUser()
    passwd = conn.getPassword()
    
    #dbtype = "mysql"
    #dbname = "avatar"
    #host = "localhost"
    #port = 3306
    #user = "root"
    #passwd = "root"
    charset = "utf8"
    logging.debug('666666666666666666...')
    driver = dr.DriverManager(dbtype=dbtype,dbname=dbname,host=host,port=port,user=user,passwd=passwd,charset=charset).getDriver()
    logging.debug('77777777777777777777777...') 
    return driver
class Comparer(QtCore.QThread):
    leftConn = None
    rightConn = None
    check=QtCore.pyqtSignal(str)
    def __init__(self, leftConn,rightConn,caller,msger,type=None):
        super(Comparer,self).__init__()
        QtCore.QThread.__init__(self)
        self.leftConn=leftConn
        self.rightConn=rightConn
        self.caller=caller
        self.msger=msger
        self.type=type
    def isConnected(self,conn):
        driver = getDriver(conn)
        cur = driver.connect()
        if cur==None:return False
        return driver.isConnected(cur)
    def getDatabaseMeta(self,conn):
        try:
            driver = getDriver(conn)
            meta = driver.getDatabaseMeta()
            return meta
        except Exception, e: 
            print Exception,":",e
            logging.debug(e)
            return None
    def getCompareInfo(self):
        left=self.getDatabaseMeta(self.leftConn)
        right = self.getDatabaseMeta(self.rightConn)
        if left==None or right==None:
            html = 'connect Failed!'
        else:
            html = cp.compare(left,right)
        return html
    def getConnectInfo(self):
        left = getDriver(self.leftConn).connect()
        right = getDriver(self.rightConn).connect()
        html=self.connectInfo(left,right)
        return html
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
    def run(self):
        if self.type==None:
            html = self.getCompareInfo()
        else:
            html = self.getConnectInfo()
        if len(html)>100:
            e = EventObject(self.caller)
        else:
            e = EventObject(self.msger)
            
        logging.debug(html)
        e.emitter(html)
        
        
