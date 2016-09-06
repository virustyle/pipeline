import os, getpass
from PySide import QtGui
from PySide import QtCore

class CustomTreeWidget(QtGui.QTreeWidget):
    def __init__(self,parent):
        super(CustomTreeWidget, self).__init__(parent)

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
        self.setMinimumSize(900,520) 
        self.setWindowTitle('Check In Files')

        groupBox = QtGui.QGroupBox("Information")
        namefonts = QtGui.QFont()
        namefonts.setBold(True)
        namefonts.setPointSize(10)

        currentAssetLabel = QtGui.QLabel("Current Asset: ")
        currentProjectLabel = QtGui.QLabel("Current Project: ")
        currentDeptLabel = QtGui.QLabel("Current Department: ")
        currentUserLabel = QtGui.QLabel("Current User: ")
        self.currentProjectNameLabel = QtGui.QLabel(str(os.environ['PROJECT']))
        self.currentUserNameLabel = QtGui.QLabel(str(getpass.getuser()))

        try:
            self.currentAssetNameLabel = QtGui.QLabel(str(os.environ['ASSETNAME']))                                  
            self.currentDeptNameLabel = QtGui.QLabel(str(os.environ['TASKSTEP']))
        except KeyError:
            self.currentAssetNameLabel = QtGui.QLabel(None)                        
            self.currentDeptNameLabel = QtGui.QLabel(None)

        self.currentAssetNameLabel.setFont(namefonts)
        self.currentProjectNameLabel.setFont(namefonts)
        self.currentDeptNameLabel.setFont(namefonts)


        self.taskLister = CustomTreeWidget(self)
        self.taskLister.setSortingEnabled(True)
        self.taskLister.setColumnCount(3)
        self.taskLister.setHeaderLabels(['File Name', 'Modified Date', 'User', 
            'Full Path'])

        self.commentBox = QtGui.QTextEdit()

        self.progressbar = QtGui.QProgressBar()        

        self.checkinButton = QtGui.QPushButton('Check In')
        self.resetButton = QtGui.QPushButton('Reset')

        vbox = QtGui.QVBoxLayout(self)
        infoLabelLayout = QtGui.QHBoxLayout()
        tasklayout = QtGui.QVBoxLayout()
        buttonLayout = QtGui.QHBoxLayout()

        infoLabelLayout.addWidget(currentProjectLabel)
        infoLabelLayout.addWidget(self.currentProjectNameLabel)
        infoLabelLayout.addWidget(currentAssetLabel)
        infoLabelLayout.addWidget(self.currentAssetNameLabel)
        infoLabelLayout.addWidget(currentDeptLabel)
        infoLabelLayout.addWidget(self.currentDeptNameLabel)
        infoLabelLayout.addWidget(currentUserLabel)
        infoLabelLayout.addWidget(self.currentUserNameLabel)

        tasklayout.addWidget(self.taskLister)
        tasklayout.addWidget(self.commentBox)

        buttonLayout.addWidget(self.checkinButton)
        buttonLayout.addWidget(self.resetButton)
        groupBox.setLayout(infoLabelLayout)
        vbox.addWidget(groupBox)
        vbox.addLayout(tasklayout)
        vbox.addWidget(self.progressbar)
        vbox.addLayout(buttonLayout)

    def launch(self):
        '''
        Core function to launch the UI for this class
        '''
        self.show()