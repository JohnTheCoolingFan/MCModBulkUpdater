import sys
import PyQt5
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QSize, QCoreApplication, QSettings,Qt,QThread
from function_download import DataFunctions,ModsDownload
import sys
from datetime import datetime
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('design/main.ui', self)
        met = QtGui.QFontMetrics(QtGui.QFont())


        settings = QSettings('dataConfig', 'Tandots')
        settings.clear()
        print(settings.allKeys())

        #custom function import here
        self.GetConfig = DataFunctions.GetConfig()
        self.GetConfig.Setting(settings)


        settings.setValue('list_value', [1, 2, 3])

        list_value = settings.value('list_value', type=int)
        print(list_value)

        #Take all elements
        self.comboBoxServer = self.findChild(QtWidgets.QComboBox,"comboBoxServer") #box on now server
        self.pathMinecraft = self.findChild(QtWidgets.QLineEdit,"pathMinecraft") #path to mods
        self.pushButtonTakePath = self.findChild(QtWidgets.QPushButton,"pushButtonTakePath") #take path button
        self.pushButtonDownload = self.findChild(QtWidgets.QPushButton,"pushButtonDownload") #download button

        self.progressBar = self.findChild(QtWidgets.QProgressBar,"progressBar") #download_mod progressBar

        self.labelCountMods = self.findChild(QtWidgets.QLabel,"labelCountMods") #status / mods count label

        #init event functionality


        self.show()






app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
