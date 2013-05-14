# -*- coding: utf-8 -*-

import sys
import time
import metadata as meta
import MySqlDriver as mysql
import SqlServerDriver as sqlserver
import OracleDriver  as oracle
import logging  
class DriverManager(object):
    driverDict = {'oracle':oracle.OracleDriver,'mysql': mysql.MySqlDriver, 'sqlserver': sqlserver.SqlServerDriver}
    driver = None
    #databaseMetaData=None
    def __init__(self, **kwargs):
        super(DriverManager,self).__init__()
        #self.databaseMetaData = meta.DatabaseMetaData(**kwargs)
        #self.dbname = self.databaseMetaData.getDbname()
        dbtype = kwargs["dbtype"]
        for drivername, driverclass in self.driverDict.items():
            if cmp(drivername,dbtype)==0:
                self.driver = driverclass(**kwargs)  
    def getDriver(self):
        return self.driver
    def connect(self):
        if self.driver!=None:
            return self.driver.connect()
    def isConnected(self,cur):
        if self.driver!=None:
            return self.driver.isConnected(cur)
    #def getDatabaseMeta(self):
    #    if self.driver!=None:
    #        logging.debug( '--------------------------------')
    #        return self.driver.getDatabaseMeta()
