# -*- coding: utf-8 -*-
# Copyright (c) 2013 zyskm <zyskm@163.com>
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import sys
import os
class previewer(QHBoxLayout):
    def __init__(self,parent=None):
        super(QHBoxLayout, self).__init__()
        
        self.hbox = QHBoxLayout(parent)
        
        self.web = QWebView()
        self.web.load(QUrl(self.getResourcePath()+"help.html"))
        self.hbox.addWidget(self.web)
    def setHtml(self,html):
        self.web.setHtml(html)
    def getHtml(self):
        return self.web.page().currentFrame().documentElement().toOuterXml()
    def getResourcePath(self):
        return 'resource'+os.sep
    def reloadHelp(self):
        self.web.load(QUrl(self.getResourcePath()+"help.html"))
def sayhi():
    print '-------------------------------'