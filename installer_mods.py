import sys
import os
import PyQt5
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets,uic

from PyQt5.QtCore import QSize, QCoreApplication, QSettings,Qt,QThread
from PyQt5.QtWidgets import QMessageBox
from function_download import DataFunctions,ModsDownload
import sys
from pathlib import Path,PurePath
from datetime import datetime
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('design/main.ui', self)
        met = QtGui.QFontMetrics(QtGui.QFont())


        self.settings = QSettings('dataConfig', 'Tandots')
        print()

        #custom function import here
        self.GetConfig = DataFunctions.GetConfig(self.settings)
        #self.settings.clear()




        #Take all elements
        self.comboBoxServer = self.findChild(QtWidgets.QComboBox,"comboBoxServer") #box on now server
        self.pathMinecraft = self.findChild(QtWidgets.QLineEdit,"pathMinecraft") #path to mods
        self.pushButtonTakePath = self.findChild(QtWidgets.QPushButton,"pushButtonTakePath") #take path button
        self.pushButtonDownload = self.findChild(QtWidgets.QPushButton,"pushButtonDownload") #download button

        self.progressBar = self.findChild(QtWidgets.QProgressBar,"progressBar") #download_mod progressBar

        self.labelCountMods = self.findChild(QtWidgets.QLabel,"labelCountMods") #status / mods count label
        self.labelPathInfo = self.findChild(QtWidgets.QLabel,"labelPathInfo") #status path

        self.comboBoxServer.currentTextChanged.connect(self.takeServer)
        self.pathMinecraft.editingFinished.connect(self.saveNowPath)
        self.pushButtonTakePath.pressed.connect(self.takePath)
        self.pushButtonDownload.pressed.connect(self.downloadAll)

        for item in self.settings.allKeys():
            self.comboBoxServer.addItem(item.upper())

        #init event functionality

        self.nowServer = self.settings.value(self.comboBoxServer.currentText().lower())
        self.check_path()
        self.path = None
        self.show()


    def check_path(self):
        path = self.pathMinecraft.text()
        if os.path.exists(path) and "minecraft" in path:
            if os.path.exists(path+"/mods"):
                self.saveNowPath()
                self.path = path
                self.labelPathInfo.setText("Path is OK!")
            else:
                self.labelPathInfo.setText("Not path mods!")
                self.path = None
                buttonReply = QMessageBox.question(self, 'Не нашли папку Mods...', "Не найдена папка mods создать? По адресу:\n{}".format(path), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    self.labelPathInfo.setText("Path is OK!")
                    self.saveNowPath()
                    self.path = path
                    os.mkdir(path+"/mods")
                else:
                    self.labelPathInfo.setText("Not path mods!")
                    self.path = None
        else:
            self.labelPathInfo.setText("Not correct path!")
            self.path = None



    def takeServer(self,text):
        self.nowServer = self.settings.value(text.lower())
        if self.nowServer["path"]:
            self.pathMinecraft.setText(self.nowServer["path"])
        else:
            self.pathMinecraft.clear()

    def saveNowPath(self):
        print(self.nowServer,self.pathMinecraft.text())
        self.nowServer["path"] = self.pathMinecraft.text()
        self.settings.setValue(self.nowServer["name"],self.nowServer)

    def takePath(self):
        if os.path.exists(self.pathMinecraft.text()):
            self.pathMinecraft.setText(
                QtWidgets.QFileDialog.getExistingDirectory(self, 'Open mods directory', self.pathMinecraft.text()))
        else:
            self.pathMinecraft.setText(
                QtWidgets.QFileDialog.getExistingDirectory(self, 'Open mods directory', str(Path.home())))


        self.nowServer["path"] = self.pathMinecraft.text()
        self.settings.setValue(self.nowServer["name"], self.nowServer)
        self.check_path()

    def downloadAll(self):
        print(self.nowServer["git"],self.nowServer["path"])
        self.GetConfig.CloneGit(self.nowServer["path"],self.nowServer["git"])
        print("git has got")
        pass



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
