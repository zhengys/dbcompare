# -*- coding: utf-8 -*-
# Copyright (c) 2013 zyskm <zyskm@163.com>
#
import sys
import time
import pdbc.AbstractDriver as dr
import logging  

class MySqlDriver(dr.AbstractDriver):
    def __init__(self, **kwargs):
        super(MySqlDriver,self).__init__(**kwargs)
        logging.debug('MySqlDriver')
    def connect(self):
        try:
            import MySQLdb as mdb
            host = self.databaseMetaData.getHostIp()
            port = self.databaseMetaData.getPort()
            user = self.databaseMetaData.getUser()
            passwd = self.databaseMetaData.getPasswd()
            db = self.databaseMetaData.getDbname()
            charset = self.databaseMetaData.getCharset()
            con = mdb.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset=charset)
            #cur = con.cursor(mdb.cursors.DictCursor)
            cur = con.cursor()
        except Exception, e: 
            print Exception,"::",e
            logging.info('mysql connect error')
            logging.info(e)
            return None
        return cur              
#-------- 
if __name__ == '__main__':
    driver = MySqlDriver(dbtype='mysql',dbname='avatar',host="127.0.0.1",port=3306,user="root",passwd="root",charset="utf8")  
    driver.getDatabaseMeta()