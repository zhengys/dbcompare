# -*- coding: utf-8 -*-
# Copyright (c) 2013 zyskm <zyskm@163.com>
#
"""
database metadata schema
"""
import random
class DatabaseMetaData:
    '''Comprehensive information about the database as a whole.'''
    _id=''
    _dbtype=''
    _dbname=''
    _host=""
    _port=0
    _user=""
    _passwd=""
    _charset=""
    _url=''
    _tableList=[]
    def __init__(self, **kwargs):
        self._id=random.randint(10, 100)
        self._dbtype=kwargs["dbtype"]
        self._dbname=kwargs["dbname"]
        self._host=kwargs["host"]
        self._port=kwargs["port"]
        self._user=kwargs["user"]
        self._passwd=kwargs["passwd"]
        self._charset=kwargs["charset"]
        self._tableList=[]
    def getId(self):
        return str(self._id)
    def getDbtype(self):
        return self._dbtype
    def getDbname(self):
        return self._dbname
    def getHost(self):
        return self._host
    def getHostIp(self):
        if cmp("localhost",self._host.lower())==0:
            return '127.0.0.1'
        return self._host
    def getPort(self):
        return self._port
    def getUser(self):
        return self._user
    def getPasswd(self):
        return self._passwd
    def getCharset(self):
        return self._charset
    def getURL(self):
        return self._url
    def getTableList(self):
        return self._tableList

class TableMetaData:
    _name=''
    _type=''
    _auto_increment=0
    _primary=''
    _columnList=[]
    def __init__(self,name,auto_increment,primary):
        self._name=name
        self._auto_increment=auto_increment
        self._primary=primary
    def getName(self):
        return self._name
    def getType(self):
        return self._type
    def getColumnList(self):
        return self._columnList
    def setColumnList(self,columnList):
        self._columnList=columnList
    def setPrimary(self,primary):
        self._primary=primary
    def getPrimary(self):
        return self._primary

    
class ColumnMetaData:
    _name=''
    #code auto_increment  dateType   length  nullable 
    _isAutoIncrement=True
    _dataType=''
    _precision=0
    _character_maximum_length=0
    _length=0
    _isNullable=True
    def __init__(self,name,_isAutoIncrement,_dataType,_precision,_character_maximum_length,_isNullable):
        self._name=name
        self._isAutoIncrement=_isAutoIncrement
        self._dataType=_dataType
        self._precision=_precision
        self._character_maximum_length=_character_maximum_length
        self._isNullable=_isNullable
        
        if _character_maximum_length is not None and _character_maximum_length>0:
            self._length=_character_maximum_length
        if _precision is not None and _precision>0:
            self._length=_precision
    def getName(self):
        return self._name
    def getDataType(self):
        return self._dataType
    def getLength(self):
        return self._length
    def isAutoIncrement(self):
        return self._isAutoIncrement
    def isNullable(self):
        return self._isNullable
    
    def getLengthStr(self):
        return str(self._length)
    def isAutoIncrementStr(self):
        return str(self._isAutoIncrement)
    def isNullableStr(self):
        return str(self._isNullable)
