import os
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
        self.setWindowTitle('Asset Manager')

        groupBox = QtGui.QGroupBox("Information")
        namefonts = QtGui.QFont()
        namefonts.setBold(True)
        namefonts.setPointSize(10)

        currentAssetLabel = QtGui.QLabel("Current Asset: ")
        currentProjectLabel = QtGui.QLabel("Current Project: ")
        currentDeptLabel = QtGui.QLabel("Current Department: ")
        self.currentProjectNameLabel = QtGui.QLabel(str(os.environ['PROJECT']))

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
        self.taskLister.setColumnCount(5)
        self.taskLister.setHeaderLabels(['Task Name', 'Asset', 'Type', 
            'Status', 'Start Date', 'Due Date', 'bid', 'Department', 
            'Time Remaining as of Today'])

        self.taskVersion = CustomTreeWidget(self)
        self.taskVersion.setSortingEnabled(True)
        self.taskVersion.setColumnCount(3)
        self.taskVersion.setHeaderLabels(['Version', 'Date', 'Author', 'Note'])

        self.progressbar = QtGui.QProgressBar()        

        self.refreshButton = QtGui.QPushButton('Refresh')
        self.checkoutButton = QtGui.QPushButton('Check Out')
        self.checkinButton = QtGui.QPushButton('Check In')
        self.settaskButton = QtGui.QPushButton('Set Task')

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

        tasklayout.addWidget(self.taskLister)
        tasklayout.addWidget(self.taskVersion)

        buttonLayout.addWidget(self.checkinButton)
        buttonLayout.addWidget(self.refreshButton)
        buttonLayout.addWidget(self.settaskButton)
        buttonLayout.addWidget(self.checkoutButton)
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