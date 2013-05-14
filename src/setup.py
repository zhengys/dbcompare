# -*- coding: utf-8 -*-

from distutils.core import setup
from sip import *
import py2exe
from PyQt4 import QtCore, QtGui
from KdeDc import Browser
from KdeDc.DataConnection import DataConnection
import ServiceDc.comparer as cper
import os
import logging  
import sys
#import Image


import glob
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding('utf-8')

includes = ["encodings", "encodings.*","sip", "PyQt4.QtCore", "PyQt4.QtGui", "PyQt4.QtNetwork", "PyQt4.QtNetwork",\
"MySQLdb","pymssql","_mssql","uuid","cx_Oracle"]     
  
options = {"py2exe":  
	{"compressed": 1,
	"optimize": 2,  
	"includes":includes,
	#"dll_excludes":["qgif4.dll","qico4.dll","qjpeg4.dll","qmng4.dll","qsvg4.dll","qtga4.dll","qtiff4.dll"],
	"bundle_files":3
	}  
	}  
setup(      
	version = "1.0.0",
    description = "database structure compare",
    name = "dbcompare",
	author = "zhengys",    
	author_email = "zhengys@gmail.com",

    options = options,       
    zipfile=None,
    windows=[{"script": "DBCompare.py", 
			"icon_resources": [(1, "resource/icons/dbcompare.ico")],
			}],

	data_files=[("resource",glob.glob("resource/*.*")),
	#(".",glob.glob("*.conf")),
	("resource/icons",glob.glob("resource/icons/*.*")),
	#('plugins/imageformats', glob.glob("D:\Python27\Lib\site-packages\PyQt4\plugins\imageformats/*.dll"))
	]

    )  

