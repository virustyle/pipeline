import os
import getpass
import json
from sgstudio import sgframework
from PySide import QtGui
from PySide import QtCore


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
        self.setMinimumSize(950,620) 
        self.setWindowTitle('Asset Manager')

        # self.projects = QtGui.QComboBox()
        # self.projects.addItem("Select Projects")
        self.taskLister = MovieTreeWidget(self)
        self.taskLister.setColumnCount(6)
        self.taskLister.setHeaderLabels(['Task Name', 'Asset', 'Status', 'Type',
            'Start Date', 'Due Date'])

        self.taskVersion = MovieTreeWidget(self)
        self.taskVersion.setColumnCount(3)
        self.taskVersion.setHeaderLabels(['Version', 'Date', 'Author', 'Note'])

        self.refreshButton = QtGui.QPushButton('Refresh')
        self.submitButton = QtGui.QPushButton('Submit')

        vbox = QtGui.QVBoxLayout(self)
        # projectLayout = QtGui.QHBoxLayout()
        # tagLayout = QtGui.QHBoxLayout()
        tasklayout = QtGui.QVBoxLayout()
        buttonLayout = QtGui.QHBoxLayout()

        # projectLayout.addWidget(self.projects)
        tasklayout.addWidget(self.taskLister)
        tasklayout.addWidget(self.taskVersion)

        # tagLayout.addWidget(self.renderFinal)
        # tagLayout.addWidget(self.errorRender)
        # tagLayout.addWidget(self.missingFrames)
        # tagLayout.addWidget(self.inputNotReady)
        # tasklayout.addLayout(tagLayout)

        # tasklayout.addWidget(self.commentBox)
        buttonLayout.addWidget(self.refreshButton)
        buttonLayout.addWidget(self.submitButton)
        # vbox.addLayout(projectLayout)
        vbox.addLayout(tasklayout)
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
        self.statusJson = json.load(open(os.path.join(os.getenv('PIPEDEV'), 'config/statuses.json')))
        self.loadUserTasks()

        # self.refreshButton.clicked.connect(self.loadUserTasks)

    def loadUserTasks(self):
        projectObject = self.sgf.getProject(str(os.environ['PROJECT']))
        currentUser = getpass.getuser()
        userInfo = {'login':currentUser}
        huser = sgframework.HumanUser(**userInfo)
        allTasks = huser.getAllTasks(projectObject)

        for task in allTasks:
            # assetObject = sgframework.Asset(**task.entity)
            if task.sg_status_list not in self.statusJson['approved']:
                self.taskLister.addToTree([task.content, task.entity['name'], 
                    task.sg_status_list])