import os
import sys
from PySide import QtGui
from PySide import QtCore
from sgstudio import sgframework
from vcs import versionmanager

SERVER_PATH = "https://pipetest.shotgunstudio.com"
SCRIPT_NAME = 'info'
SCRIPT_KEY = '90aea59877cebbb6445bf7e77f5d90a9663ff0ba45d5eebae168703a6ad98cd2'

class MovieTreeWidget(QtGui.QTreeWidget):
    def __init__(self,parent):
        super(MovieTreeWidget, self).__init__(parent)

    def addToTree(self, treeList):
        '''
        List of items to be filled
            :Args:
                treeList (List): List of items to be added in same row
        '''
        root = QtGui.QTreeWidgetItem(self, treeList)

class UserInterface(QtGui.QWidget):
    def __init__(self):
        super(UserInterface, self).__init__()
        self.setGeometry(300, 300, 400, 120)
        self.setMinimumSize(550,320) 
        self.setWindowTitle('Asset Creator')

        self.projectLabel = QtGui.QLabel()
        # self.projectDrop = QtGui.QComboBox()

        self.assetNameLabel = QtGui.QLabel("Type your Asset Name")
        self.assetNameText = QtGui.QLineEdit()

        self.assetTypeLabel = QtGui.QLabel("Select asset Type")
        self.assetTypeDrop = QtGui.QComboBox()
        self.assetTypeDrop.addItem("Character")
        self.assetTypeDrop.addItem("Environment")
        self.assetTypeDrop.addItem("Prop")

        self.descriptionLabel = QtGui.QLabel("Description")
        self.descriptionText = QtGui.QTextEdit()

        self.createButton = QtGui.QPushButton("Create Asset")

        
        vbox = QtGui.QVBoxLayout(self)
        projectLayout = QtGui.QHBoxLayout()
        projectLayout.addWidget(self.projectLabel)
        # projectLayout.addWidget(self.projectDrop)

        assetNameLayout = QtGui.QHBoxLayout()
        assetNameLayout.addWidget(self.assetNameLabel)
        assetNameLayout.addWidget(self.assetNameText)

        assetTypeLayout = QtGui.QHBoxLayout()
        assetTypeLayout.addWidget(self.assetTypeLabel)
        assetTypeLayout.addWidget(self.assetTypeDrop)

        descriptionlayout = QtGui.QHBoxLayout()
        descriptionlayout.addWidget(self.descriptionLabel)
        descriptionlayout.addWidget(self.descriptionText)

        vbox.addLayout(projectLayout)
        vbox.addLayout(assetTypeLayout)
        vbox.addLayout(assetNameLayout)
        vbox.addLayout(descriptionlayout)
        vbox.addWidget(self.createButton)
 

    def launch(self):
        '''
        Core function to launch the UI for this class
        '''
        self.show()

class AssetCreator(UserInterface):
    def __init__(self):
        super(AssetCreator, self).__init__()
        self.sgf = sgframework.SgFrameWork(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)
        self.projectObject = self.sgf.getProject(str(os.environ['PROJECT']))
        self.projectLabel.setText("Project Environment:   {0}".format(str(os.environ['PROJECT'])))

        self.createButton.clicked.connect(self.create)
        
    def create(self):
        assetType = self.assetTypeDrop.currentText()
        assetName = self.assetNameText.text()
        description = self.descriptionText.toPlainText()

        a = self.projectObject.createAsset(assetName, assetType, description)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ac = AssetCreator()
    ac.launch()
    sys.exit(app.exec_())
    