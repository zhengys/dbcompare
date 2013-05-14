# -*- coding: utf-8 -*-
# Copyright (c) 2013 zyskm <zyskm@163.com>
#
import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui, QtWebKit

from ui_previewer import Ui_Form

class Previewer(QtGui.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Previewer, self).__init__(parent)

        self.setupUi(self)
        self.baseUrl = QtCore.QUrl()
 

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.centralWidget = Previewer(self)
        self.setCentralWidget(self.centralWidget)
        self.setStartupText()

    def setStartupText(self):
        self.centralWidget.webView.setHtml("""
<html><body>
 <h1>HTML Previewer</h1>
  <p>This example shows you how to use QtWebKit.QWebView to
   preview HTML data written in a QtGui.QPlainTextEdit.
  </p>
</body></html>""")


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
