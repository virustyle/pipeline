import sys
import os
import getpass
from PySide import QtGui
from PySide import QtCore
from core import projects
from core import privilages

__author__ = "Arjun Thekkumadathil"
__email__ = "arjun.thekkumadathil@gmail.com"

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
        self.setGeometry(300, 300, 1000, 700)
        self.setMinimumSize(900,600) 
        self.setWindowTitle('Task Manager')

        #CONFIG INFO
        projectInfo = projects.Projects()
        self.projectObj = projectInfo.getProject(str(os.environ['PROJECTNAME']))
        privilageInfo = privilages.Privilages()
        self.privilageObj = privilageInfo.getPrivilage()

        # Tab widget
        self.tab_widget = QtGui.QTabWidget(self) 
        self.shottab = QtGui.QWidget() 
        self.assettab = QtGui.QWidget()
        self.playlisttab = QtGui.QWidget()
        self.tab_widget.addTab(self.shottab, "Task Lister")
        self.taskListerUI()
        if self.productionCheck() or self.adminCheck():
            self.tab_widget.addTab(self.assettab, "Task Create") 
            self.taskCreateUI()
        self.tabbox = QtGui.QVBoxLayout()
        self.tabbox.addWidget(self.tab_widget)
        self.setLayout(self.tabbox)

        

    def taskListerUI(self):
        # basic horizonatal and vertical layouts
        vbox = QtGui.QVBoxLayout(self.shottab)
        infoLayout = QtGui.QHBoxLayout()
        searchLayout = QtGui.QHBoxLayout()
        taskListLayout = QtGui.QVBoxLayout()
        buttonLayout = QtGui.QHBoxLayout()

        # information group box
        groupBox = QtGui.QGroupBox("Information")
        namefonts = QtGui.QFont()
        namefonts.setBold(True)
        namefonts.setPointSize(10)

        # Information Labels
        currentProjectLabel = QtGui.QLabel("Current Project: {0}".format(self.projectObj.name))
        infoLayout.addWidget(currentProjectLabel)

        currentUserLabel = QtGui.QLabel("Current User: {0}".format(getpass.getuser()))
        infoLayout.addWidget(currentUserLabel)

        currentDivisionLabel = QtGui.QLabel("Division: {0}".format(self.projectObj.division))
        infoLayout.addWidget(currentDivisionLabel)

        currentStatusLabel = QtGui.QLabel("Status: {0}".format(self.projectObj.status))
        infoLayout.addWidget(currentStatusLabel)

        # search box information
        self.searchTypeCombo = QtGui.QComboBox()
        self.searchTypeCombo.addItem('User Name')
        self.searchTypeCombo.addItem('Task Name')
        self.searchTypeCombo.addItem('Status')
        searchLayout.addWidget(self.searchTypeCombo)

        self.searchBarLineEdit = QtGui.QLineEdit()
        searchLayout.addWidget(self.searchBarLineEdit)

        self.filterButton = QtGui.QPushButton("Filter")
        searchLayout.addWidget(self.filterButton)

        # task information
        self.taskListTreeWidget = CustomTreeWidget(self)
        self.taskListTreeWidget.setColumnCount(8)
        self.taskListTreeWidget.setHeaderLabels(['ID', 'Task Name','Status', 'Assigned', 
            'Start Date','End Date', 'Actual Start Date', 'Actual End Date', 'Remarks'])
        taskListLayout.addWidget(self.taskListTreeWidget)

        # Version information
        self.versionListTreeWidget = CustomTreeWidget(self)
        self.versionListTreeWidget.setColumnCount(5)
        self.versionListTreeWidget.setHeaderLabels(['Version Number', 'Comment','Author',
            'Movie Path', 'Review Notes'])
        taskListLayout.addWidget(self.versionListTreeWidget)

        # buttons
        self.checkoutVersion = QtGui.QPushButton("Checkout Version")
        buttonLayout.addWidget(self.checkoutVersion)
        self.makeVersion = QtGui.QPushButton("Make Version")
        buttonLayout.addWidget(self.makeVersion)
        self.submitReview = QtGui.QPushButton("Submit for Review")
        buttonLayout.addWidget(self.submitReview)
        self.addRemark = QtGui.QPushButton("Add Remark")
        buttonLayout.addWidget(self.addRemark)
        self.publishTask = QtGui.QPushButton("Publish Task")
        buttonLayout.addWidget(self.publishTask)

        groupBox.setLayout(infoLayout)

        # adding multiple layouts to the main layout
        vbox.addWidget(groupBox)
        vbox.addLayout(searchLayout)
        vbox.addLayout(taskListLayout)
        vbox.addLayout(buttonLayout)

    def taskCreateUI(self):
        #LAYOUTS
        vboxC = QtGui.QVBoxLayout(self.assettab)
        infoLayoutC = QtGui.QHBoxLayout()
        taskTypeLayout = QtGui.QHBoxLayout()
        taskNameLayout = QtGui.QHBoxLayout()
        taskDefaultNameLayout = QtGui.QHBoxLayout()
        taskDateLayout = QtGui.QHBoxLayout()
        descriptionLayout = QtGui.QHBoxLayout()
        buttonLayout = QtGui.QHBoxLayout()

        groupBoxC = QtGui.QGroupBox("Information")
        namefontsC = QtGui.QFont()
        namefontsC.setBold(True)
        namefontsC.setPointSize(10)

        currentProjectLabelC = QtGui.QLabel("Current Project: {0}".format(self.projectObj.name))
        infoLayoutC.addWidget(currentProjectLabelC)

        currentUserLabelC = QtGui.QLabel("Current User: {0}".format(getpass.getuser()))
        infoLayoutC.addWidget(currentUserLabelC)

        currentDivisionLabelC = QtGui.QLabel("Division: {0}".format(self.projectObj.division))
        infoLayoutC.addWidget(currentDivisionLabelC)

        currentStatusLabelC = QtGui.QLabel("Status: {0}".format(self.projectObj.status))
        infoLayoutC.addWidget(currentStatusLabelC)

        taskTypeLabel = QtGui.QLabel('Select you task type:')
        taskTypeLayout.addWidget(taskTypeLabel)
        self.assetTaskType = QtGui.QRadioButton("Asset")
        taskTypeLayout.addWidget(self.assetTaskType)
        self.shotTaskType = QtGui.QRadioButton("Shot")
        taskTypeLayout.addWidget(self.shotTaskType)

        seqLabel = QtGui.QLabel('Sequences')
        self.taskSeqName = QtGui.QComboBox()
        taskNameLayout.addWidget(seqLabel)
        taskNameLayout.addWidget(self.taskSeqName)

        assetLabel = QtGui.QLabel('Asset')
        self.taskAssetName = QtGui.QComboBox()
        taskNameLayout.addWidget(assetLabel)
        taskNameLayout.addWidget(self.taskAssetName)

        shotLabel = QtGui.QLabel('Shots')
        self.taskShotName = QtGui.QComboBox()
        taskNameLayout.addWidget(shotLabel)
        taskNameLayout.addWidget(self.taskShotName)

        deptLabel = QtGui.QLabel('Departments')
        self.taskDepartmentName = QtGui.QComboBox()
        taskNameLayout.addWidget(deptLabel)
        taskNameLayout.addWidget(self.taskDepartmentName)

        statusLabel = QtGui.QLabel('Status')
        self.statusName = QtGui.QComboBox()
        taskNameLayout.addWidget(statusLabel)
        taskNameLayout.addWidget(self.statusName)

        defaultLabel = QtGui.QLabel('Default Name')
        self.defaultName = QtGui.QLineEdit('Default')
        taskDefaultNameLayout.addWidget(defaultLabel)
        taskDefaultNameLayout.addWidget(self.defaultName)

        startDateLabel = QtGui.QLabel('Start Date')
        self.startDate = QtGui.QCalendarWidget()
        endDateLabel = QtGui.QLabel('End Date')
        self.endDate = QtGui.QCalendarWidget()
        taskDateLayout.addWidget(startDateLabel)
        taskDateLayout.addWidget(self.startDate)
        taskDateLayout.addWidget(endDateLabel)
        taskDateLayout.addWidget(self.endDate)

        descriptionLabel =QtGui.QLabel('Description')
        self.descriptionText =QtGui.QTextEdit()
        descriptionLayout.addWidget(descriptionLabel)
        descriptionLayout.addWidget(self.descriptionText)

        self.validateButton = QtGui.QPushButton('Validate Task')
        self.createButton = QtGui.QPushButton('Create Task')
        buttonLayout.addWidget(self.validateButton)
        buttonLayout.addWidget(self.createButton)

        groupBoxC.setLayout(infoLayoutC)
        vboxC.addWidget(groupBoxC)
        vboxC.addLayout(taskTypeLayout)
        vboxC.addLayout(taskNameLayout)
        vboxC.addLayout(taskDefaultNameLayout)
        vboxC.addLayout(taskDateLayout)
        vboxC.addLayout(descriptionLayout)
        vboxC.addLayout(buttonLayout)

    def leadCheck(self):
        currentUser = getpass.getuser()
        if currentUser in self.privilageObj.leads:
            return True
        else:
            return False

    def adminCheck(self):
        currentUser = getpass.getuser()
        if currentUser in self.privilageObj.admin:
            return True
        else:
            return False

    def productionCheck(self):
        currentUser = getpass.getuser()
        if currentUser in self.privilageObj.production:
            return True
        else:
            return False

































        # QTreeWidget to list all items
        # ASSET TAB
        

    def createMenu(self):
        pass

    def launch(self):
        '''
        Core function to launch the UI for this class
        '''
        self.show()