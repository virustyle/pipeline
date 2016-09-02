import os
import getpass
import json
import datetime
from sgstudio import sgframework
from PySide import QtGui
from PySide import QtCore
from core import sandbox
from core import pipeconfig
reload(pipeconfig)

pconf = pipeconfig.PipeConfig()
conf = pconf.shotgunKeys()['coretools']

SERVER_PATH = conf['url']
SCRIPT_NAME = conf['name']
SCRIPT_KEY = conf['skey']

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

class AssetManager(UserInterface):
    def __init__(self):
        super(AssetManager, self).__init__()
        self.sgf = sgframework.SgFrameWork(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)
        self.statusJson = json.load(open(os.path.join(os.getenv('PIPEDEV'), 
            'config/statuses.json')))
        self.loadUserTasks()

        self.refreshButton.clicked.connect(self.loadUserTasks)
        self.settaskButton.clicked.connect(self.setTaskSettings)

    def setTaskSettings(self):
        currentSelection = self.taskLister.selectedItems()[0]
        os.environ["ASSETNAME"] = currentSelection.text(1)
        os.environ["TASKSTEP"] = currentSelection.text(7)
        os.environ["ASSETTYPE"] = currentSelection.text(2)
        self.currentAssetNameLabel.setText(str(currentSelection.text(1)))
        self.currentDeptNameLabel.setText(str(currentSelection.text(7)))
        sbox = sandbox.SandBox()
        currentAssetSandBox = sbox.getSandBox()
        if currentAssetSandBox is None:
            sbox.create()

    def remainingTime(self, dueDate):
        currentDate = datetime.date.today()
        dateSplit = dueDate.split("-")
        dueDateObj = datetime.date(int(dateSplit[0]), int(dateSplit[1]), 
            int(dateSplit[2]))
        remainingDays = dueDateObj - currentDate
        return str(remainingDays).split(',')[0]

    def loadUserTasks(self):
        self.taskLister.clear()
        projectObject = self.sgf.getProject(str(os.environ['PROJECT']))
        currentUser = getpass.getuser()
        userInfo = {'login':currentUser}
        huser = sgframework.HumanUser(**userInfo)
        allTasks = huser.getAllTasks(projectObject)
        self.progressbar.setRange(0,len(allTasks))
        for index, task in enumerate(allTasks):
            self.progressbar.setValue(index+1)
            assetObject = sgframework.Asset(**task.entity)
            if task.sg_status_list not in self.statusJson['approved']:
                self.taskLister.addToTree([task.content, task.entity['name'],
                assetObject.sg_asset_type, task.sg_status_list, 
                task.start_date, task.due_date,
                "{0} Days".format(task.duration/600), task.step['name'],
                    self.remainingTime(task.due_date)])