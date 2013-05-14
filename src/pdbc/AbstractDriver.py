# -*- coding: utf-8 -*-

import sys
import time
import metadata as meta
import logging  

class AbstractDriver(object):
    dbname=''
    databaseMetaData=None
    def __init__(self, **kwargs):
        super(AbstractDriver,self).__init__()
        self.databaseMetaData = meta.DatabaseMetaData(**kwargs)
        self.dbname = self.databaseMetaData.getDbname()

    #base on database type rewrite these method.  bgein
    def getAllTablePrimarySql(self):
        sql = "SELECT table_name,column_name from information_schema.KEY_COLUMN_USAGE  \
            WHERE table_schema = '"+self.dbname+"'  \
            and constraint_name='PRIMARY' \
            order by table_name"
        return sql
    def getAllColumnListSql(self):
        sql = "select table_name,column_name,data_type,character_maximum_length,numeric_precision,is_nullable,ordinal_position \
            from information_schema.columns \
            WHERE table_schema = '"+self.dbname+"'  \
            order by table_name,ordinal_position ";
        return sql
    def getAllTablesSql(self):
        sql = "SELECT table_name,auto_increment FROM INFORMATION_SCHEMA.TABLES  WHERE table_schema = '"+self.dbname+"' order by table_name"
        return sql
    def getIsConnectedSql(self):
        sql = "SELECT count(*) as tablenum FROM INFORMATION_SCHEMA.TABLES ";
        return sql
    #base on database type rewrite these method.  end
    
    def getAllTablePrimary(self,cur):
        tablePrimaryCurList=[]
        cur.execute(self.getAllTablePrimarySql())
        rows = cur.fetchall()
        numrows = int(cur.rowcount)
        if rows is None or numrows<=0:
            pass
        else:
            row = rows[0]
            if row is None:
                pass
            else:
                tablePrimaryCurList.append(row)
        return tablePrimaryCurList
    def getAllColumnList(self,cur):
        columnCurList=[]
        cur.execute(self.getAllColumnListSql())
        rows = cur.fetchall()
        numrows = int(cur.rowcount)
        if rows is None or numrows<=0:
            return []
        else:
            for row in rows:
                columnCurList.append(row)
        return columnCurList
    def getTablePrimary(self,tableName,tablePrimaryList):
        numrows = len(tablePrimaryList)
        if tablePrimaryList is None or numrows<=0:
            return None
        else:
            for row in tablePrimaryList:
                #tName=row["table_name"]
                tName=row[0]
                if cmp(tableName,tName)==0:
                    #return row["column_name"]
                    return row[1]
        return None
                
    def getColumnList(self,table,columnCurList):
        columnList=[]
        tableName = table.getName()
        find=False
        numrows = len(columnCurList)
        if columnCurList is None or numrows<=0:
            return []
        else:
            for row in columnCurList:
                #table_name,column_name,data_type,character_maximum_length,numeric_precision,is_nullable,ordinal_position
                #tName=row["table_name"]
                tName=row[0]
                
                if cmp(tableName,tName)==0:
                    
                    find = True
                    #columnName=row["column_name"]
                    columnName=row[1]
                    isAutoIncrement=False
                    if cmp(columnName,table.getPrimary())==0:
                        isAutoIncrement=True
                    #dataType=row["data_type"]
                    #character_maximum_length=row["character_maximum_length"]
                    #precision=row["numeric_precision"]
                    #isNullable=row["is_nullable"]
                    dataType=row[2]
                    character_maximum_length=row[3]
                    precision=row[4]
                    isNullable=row[5]
                    column = meta.ColumnMetaData(columnName,isAutoIncrement,dataType,precision,character_maximum_length,isNullable)
                    columnList.append(column)
                elif find:
                    break
        #print tName,str(len(columnList))
        return columnList
    
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
            print Exception,":-c",e
            logging.info(e)
            return None
        return cur
    def isConnected(self,cur):
        try:
            tablenum = cur.execute(self.getIsConnectedSql())
            if tablenum>0:
                return True
        except Exception, e: 
            print Exception,":-i",e
            return False
    def getAllTables(self,cur):
        cur.execute(self.getAllTablesSql())
        rows = cur.fetchall()
        return rows
    def getDatabaseMeta(self):
        con = None
        database = None
        try:
            cur = self.connect()
            if cur==None: return None
            if(self.isConnected(cur)==False):
                #connection error
                return database
            else:
                tablePrimaryCurList = self.getAllTablePrimary(cur)
                columnCurList = self.getAllColumnList(cur)
                rows = self.getAllTables(cur)
                i=0
                for row in rows:
                    #table_name,IDENT_CURRENT(table_name) as auto_increment
                    #tableName = row["table_name"]
                    tableName = row[0]
                    i+=1
                    #print tableName
                    table = meta.TableMetaData(row[0],row[1],self.getTablePrimary(tableName,tablePrimaryCurList))
                    table.setColumnList(self.getColumnList(table,columnCurList))
                    self.databaseMetaData.getTableList().append(table)
                return self.databaseMetaData
        except Exception, e: 
            print  e
            logging.info( 'getDatabaseMeta exception..........')
            #print "Error %d: %s" % (e.args[0],e.args[1])
            logging.info(e)
            return database
        finally:    
            if con:    
                con.close()   


if __name__ == '__main__':
    driver = AbstractDriver(dbtype='mysql',dbname='avatar',host="localhost",port=3306,user="root",passwd="root",charset="utf8")
    driver.connect()  
    #driver.getDatabaseMeta()