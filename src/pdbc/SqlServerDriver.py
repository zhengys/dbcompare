# -*- coding: utf-8 -*-
import sys
import time
import metadata as meta
import pdbc.AbstractDriver as dr
import logging  

class SqlServerDriver(dr.AbstractDriver):
    def __init__(self, **kwargs):
        super(SqlServerDriver,self).__init__(**kwargs)
    def connect(self):
        try:
            import pymssql as mdb
            host = self.databaseMetaData.getHostIp()
            port = self.databaseMetaData.getPort()
            user = self.databaseMetaData.getUser()
            passwd = self.databaseMetaData.getPasswd()
            db = self.databaseMetaData.getDbname()
            charset = self.databaseMetaData.getCharset()
            con = mdb.connect(host=host,port=port,user=user,password=passwd,database=db,charset=charset)
            cur = con.cursor()
        except Exception, e: 
            print Exception,":",e
            logging.info(e)
            return None
        return cur   
    #base on database type rewrite these method.  bgein
    def getAllTablePrimarySql(self):
        sql = "SELECT k.table_name,k.column_name  \
            from information_schema.KEY_COLUMN_USAGE k,INFORMATION_SCHEMA.TABLE_CONSTRAINTS  c  \
            WHERE k.CONSTRAINT_NAME=c.CONSTRAINT_NAME \
            and k.table_catalog = '"+self.dbname+"'  \
            and c.constraint_type='PRIMARY KEY' \
            order by c.table_name"
        return sql
    def getAllColumnListSql(self):
        sql = "select table_name,column_name,data_type,character_maximum_length,numeric_precision,is_nullable,ordinal_position \
            from information_schema.columns \
            WHERE table_catalog = '"+self.dbname+"'  \
            order by table_name,ordinal_position ";
        return sql
    def getAllTablesSql(self):
        sql = "SELECT table_name,IDENT_CURRENT(table_name) as auto_increment FROM INFORMATION_SCHEMA.TABLES  WHERE table_catalog = '"+self.dbname+"' order by table_name"
        return sql
    def getIsConnectedSql(self):
        sql = "SELECT count(*) as tablenum FROM INFORMATION_SCHEMA.TABLES ";
        return sql
    #base on database type rewrite these method.  end

                    
#------------------------------------------- 
if __name__ == '__main__':
    driver = SqlServerDriver(dbtype='sqlserver',dbname='FinancialAudit',host="211.151.249.252",port=54133,user="userconn_for_finance",passwd="userconn_for_finance123**",charset="utf8")  
    driver.getDatabaseMeta()