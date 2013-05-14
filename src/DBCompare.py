# -*- coding: utf-8 -*-
# Copyright (c) 2013 zyskm <zyskm@163.com>
#
"""
dbcompare kde init
"""

from PyQt4 import QtCore, QtGui
from KdeDc import Browser
from KdeDc.DataConnection import DataConnection
import ServiceDc.comparer as cper
import os
import logging  

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding('utf-8')
class MainWindow(QtGui.QMainWindow):
    leftConnection=None
    rightConnection=None
    threadRunning=False
    def __init__(self):
        super(MainWindow, self).__init__()
        #窗口布局
        self.initUI()
        
    def initUI(self):      
        centralWidget = self.centralWidget()
        

        topleft = QtGui.QFrame(centralWidget)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
        self.leftConnection=DataConnection()
        topleft.setLayout(self.leftConnection)
        
        topright = QtGui.QFrame(centralWidget)
        topright.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rightConnection=DataConnection()
        topright.setLayout(self.rightConnection)
        
        self.middle = QtGui.QFrame(centralWidget)
        self.middle.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pbar = QtGui.QProgressBar(self.middle)
        self.pbar.setGeometry(0, 0, 500,25)
        #self.middle.setStyleSheet("QFrame{border: 0px;}") 
        
        
        self.bottom = QtGui.QFrame(centralWidget)
        self.bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        self.browser = Browser.previewer(self.bottom)
        
        self.splitterTop = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitterTop.addWidget(topleft)
        self.splitterTop.addWidget(topright)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.splitterTop)
        self.middle.hide()
        splitter.addWidget(self.middle)
        splitter.addWidget(self.bottom)
        #self.bottom.hide()
        
        hbox = QtGui.QHBoxLayout(centralWidget)
        hbox.addWidget(splitter)
        
        self.centralWidget=QtGui.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(hbox)
        self.centralWidget.setLayout(hbox)
        
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        self.createActions()
        self.createMenus()
        self.createToolbar()
        #状态栏
        message = "Ready"
        self.statusBar().showMessage(message)
        #窗口标题、大小、位置
        self.setWindowIcon(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'dbcompare.png'))
        self.setWindowTitle("DBCompare")
        self.setMinimumSize(600,480)
        self.resize(800,600)
        self.center()
        self.show()
        self.processbarCenter()
    def getResourcePath(self):
        return os.getcwd()+os.sep+'resource'+os.sep
    def timerEvent(self, event):
        if self.step >= 90:
            if self.threadRunning==True:
                self.step = 80
        self.step = self.step + 1
        self.pbar.setValue(self.step)
    
    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)
    def processbarCenter(self):
        screen = self.middle.geometry()
        size =  self.pbar.geometry()
        self.pbar.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    #右键菜单
    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        menu.addAction(self.cutAct)
        menu.addAction(self.copyAct)
        menu.addAction(self.pasteAct)
        menu.exec_(event.globalPos())

    def newFile(self):
        self.infoLabel.setText("Invoked <b>File|New</b>")

    def open(self):
        filename=QtGui.QFileDialog.getOpenFileName(self,'Open file','./',self.tr('Image Files(*.htm *.html)'))
        file =open(filename)
        html=file.read()
        self.browser.setHtml(html)
            
    def save(self):
        filename =os.getcwd()+os.sep+'DbCompare.html'
        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text): 
            QtGui.QMessageBox.warning(self, self.tr("Dock Widgets"), 
            self.tr("Cannot write file %1:\n%2.").arg(filename)
            .arg(file.errorString()))
            return
        out = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)#设置光标
        out << self.browser.getHtml()
        QtGui.QApplication.restoreOverrideCursor()
        self.statusBar().showMessage(self.tr("Saved '%1'").arg(filename), 2000)
        
    def saveAs(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,self.tr("Choose a file name"), ".",self.tr("HTML (*.html *.htm)"))
        if filename.isEmpty():            
            return          
        file = QtCore.QFile(filename)        
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr("Dock Widgets"),
            self.tr("Cannot write file %1:\n%2.").arg(filename)
            .arg(file.errorString())) 
            return
        out = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        out << self.browser.getHtml()
        QtGui.QApplication.restoreOverrideCursor() 
        self.statusBar().showMessage(self.tr("Saved '%1'").arg(filename), 2000)

    def print_(self):
        document  = QtGui.QTextDocument(self.browser.getHtml())
        printer = QtGui.QPrinter()          
        dlg = QtGui.QPrintDialog(printer, self)        
        if dlg.exec_() != QtGui.QDialog.Accepted:            
            return          
        document.print_(printer)          
        self.statusBar().showMessage(self.tr("Print"), 2000)
    @QtCore.pyqtSlot(str)
    def callbackCompareCC(self,html):
        self.threadRunning=False
        self.pbar.setValue(100)
        self.bottom.show()
        self.middle.hide()
        QtGui.QMessageBox.information(self,"QMessageBox.information()", html)
        self.toolbar.setEnabled(True) 
    @QtCore.pyqtSlot(str) 
    def callbackCompare(self,html):
        self.threadRunning=False
        self.pbar.setValue(100)
        self.bottom.show()
        self.middle.hide()
        self.browser.setHtml(html)
        self.toolbar.setEnabled(True)    
    def compare(self,type=None):
        self.toolbar.setEnabled(False)
        self.timer = QtCore.QBasicTimer()
        self.step = 0
        self.threadRunning=True
        self.thread = cper.Comparer(self.leftConnection,self.rightConnection,self.callbackCompare,self.callbackCompareCC,type)
        self.thread.start()

        self.middle.show()
        self.bottom.hide()
        self.middle.setGeometry(self.bottom.geometry())
        self.processbarCenter()
        self.onStart()
    def connect(self):
        if self.leftConnection.isInputed()==False:
            QtGui.QMessageBox.information(self,"QMessageBox.information()", 'please input left connection information...')
            return
        if self.rightConnection.isInputed()==False:
            QtGui.QMessageBox.information(self,"QMessageBox.information()", 'please input Right connection information...')
            return
        self.compare('connect')
    def run(self):
        if self.leftConnection.isInputed()==False:
            QtGui.QMessageBox.information(self,"QMessageBox.information()", 'please input left connection information...')
            return
        if self.rightConnection.isInputed()==False:
            QtGui.QMessageBox.information(self,"QMessageBox.information()", 'please input Right connection information...')
            return
        self.compare()
        
    def preferences(self):
        self.informationMessage()
    def switchView(self):
        if self.splitterTop.isHidden():  
            self.splitterTop.show()  
            self.switchViewAct.setIcon(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'fit.png'))
        else:
            self.splitterTop.hide()  
            self.switchViewAct.setIcon(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'all_context.png'))
    def about(self):
        self.browser.reloadHelp()
        self.bottom.show()
        self.middle.hide()
    def aboutQt(self):
        QtGui.QMessageBox.about(self, self.tr("About DbCompare"),            
                                self.tr("Database structure compare tool "                    
                                        "create by zhengys "                    
                                        "email:zhengys@gmail.com"))
        
    def informationMessage(self):    
        reply = QtGui.QMessageBox.information(self,"QMessageBox.information()", "left database connect success!\n left database connect success!")
    #---sub thread rollback   
    
    def createActions(self):
        #begin file
        self.newAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'New.ico'),"&New", self,
                shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'folder-open.png'),"&Open...", self,
                shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an existing html file", triggered=self.open)

        self.saveAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'save.png'),"&Save", self,
                shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the document(DbCompare.html) to disk", triggered=self.save)

        self.printAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'print.png'),"&Print...", self,
                shortcut=QtGui.QKeySequence.Print,
                statusTip="Print the document", triggered=self.print_)
        
        self.saveAsAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'saveas_edit.png'),"&SaveAs", self,
                shortcut=QtGui.QKeySequence.SaveAs,
                statusTip="Save document after prompting the user for a file name.", triggered=self.saveAs)

        self.exitAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'Disconnect.png'),"E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)
        #end file
        #begin run
        self.connectAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'imp_extfeat.png'),"Co&nnect", self, shortcut="Ctrl+O",
                statusTip="check database connect", triggered=self.connect)
        self.runAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'DBRun.png'),"&Compare", self, shortcut="Ctrl+R",
                statusTip="run database structure compare", triggered=self.run)
        #end run
        #begin preferences
        self.preferencesAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'Properties.ico'),"&Preferences", self,
                shortcut=QtGui.QKeySequence.Preferences,
                statusTip="Open the preferences dialog", triggered=self.preferences)
        #end preferences
        
        self.switchViewAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'fit.png'),"&maximize", self,
                statusTip="maximize result window", triggered=self.switchView)
        
        self.aboutAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'help.png'),"&help", self,
                statusTip="zhengys@gmail.com",
                triggered=self.about)
        
        self.aboutQtAct = QtGui.QAction(QtGui.QIcon(self.getResourcePath()+'icons'+os.sep+'info_obj.png'),"About &Qt", self,
                statusTip="Show dbcompare About box",
                triggered=self.aboutQt)
        #self.aboutQtAct.triggered.connect(QtGui.qApp.aboutQt)

       

    def createMenus(self):
        #文件
        self.fileMenu = self.menuBar().addMenu("&File")
        #self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        #运行
        self.runMenu = self.menuBar().addMenu("&Run")
        self.runMenu.addAction(self.connectAct)
        self.runMenu.addAction(self.runAct)
        #设置
        #self.preferencesMenu = self.menuBar().addMenu("&Preferences")
        #self.preferencesMenu.addAction(self.preferencesAct)
        #帮助
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
    def createToolbar(self):
        self.toolbar =self.addToolBar('Exit')
        self.toolbar.addAction(self.openAct)#打开文件
        self.toolbar.addAction(self.saveAct)#保存文件
        self.toolbar.addAction(self.saveAsAct)#保存文件
        self.toolbar.addAction(self.connectAct)#测试连接
        self.toolbar.addAction(self.runAct)#运行
        #self.toolbar.addAction(self.preferencesAct)#设置
        self.toolbar.addAction(self.switchViewAct)#视图
        self.toolbar.addAction(self.aboutAct)
                


        
    
if __name__ == '__main__':
    import sys
    logging.basicConfig(filename = os.path.join(os.getcwd(), 'dbcompare.log'), level = logging.INFO, format = '%(asctime)s - %(levelname)s: %(message)s')  
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    try:
        sys.exit(app.exec_())
    finally:
        window.cleanUp()
