# -*- coding: utf-8 -*-
import sys
import time
import pdbc.AbstractDriver as dr
import logging  

class OracleDriver(dr.AbstractDriver):
    def __init__(self, **kwargs):
        super(OracleDriver,self).__init__(**kwargs)
    def connect(self):
        try:
            import cx_Oracle as mdb
            import os
            os.environ['NLS_LANG'] = 'TRADITIONAL CHINESE_TAIWAN.ZHT16MSWIN950'
            
            host = self.databaseMetaData.getHostIp()
            port = self.databaseMetaData.getPort()
            user = self.databaseMetaData.getUser()
            passwd = self.databaseMetaData.getPasswd()
            db = self.databaseMetaData.getDbname()
            charset = self.databaseMetaData.getCharset()
            
            dsn_tns = mdb.makedsn(host, port,db)
            #print dsn_tns
            con = mdb.connect(user,passwd,dsn_tns)
            cur = con.cursor()
        except Exception, e: 
            print Exception,":-o",e
            logging.info(e)
            return None
        return cur   
    #base on database type rewrite these method.  bgein
    def getAllTablePrimarySql(self):
        sql = "SELECT k.table_name,k.column_name  \
            from user_cons_columns k,user_constraints  c  \
            WHERE k.CONSTRAINT_NAME=c.CONSTRAINT_NAME \
            and c.constraint_type='P'  \
            order by c.table_name"
        return sql
    def getAllColumnListSql(self):
        sql = "select table_name,column_name,data_type,data_length,data_precision,nullable,column_id as ordinal_position \
            from user_tab_columns \
            order by table_name,ordinal_position ";
        return sql
    def getAllTablesSql(self):
        sql = "SELECT table_name,1 as auto_increment FROM USER_TABLES  order by table_name"
        return sql
    def getIsConnectedSql(self):
        sql = "SELECT count(*) as tablenum FROM USER_TABLES ";
        return sql
    #base on database type rewrite these method.  end

                    
#------------------------------------------- 
if __name__ == '__main__':
    driver = OracleDriver(dbtype='sqlserver',dbname='FinancialAudit',host="211.151.249.252",port=54133,user="userconn_for_finance",passwd="userconn_for_finance123**",charset="utf8")  
    driver.getDatabaseMeta()