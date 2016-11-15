import os
import maya.cmds as mc
import random
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore

class UserInterface(QtWidgets.QWidget):
    def __init__(self):
        super(UserInterface, self).__init__()
        self.setGeometry(300, 300, 400, 120)
        self.setMinimumSize(400,150) 
        self.setWindowTitle('$RaNdOm SeLEcTor')

        self.totalNum = 0
        self.allSelection = None

        self.initialSelectionButton = QtWidgets.QPushButton('Initialize Selection')
        self.totalNumObjectLabel = QtWidgets.QLabel('Total numbe of objects selected: 0')
        self.numObjectLabel = QtWidgets.QLabel('Number of Objects to Select')
        self.numObjectSelection = QtWidgets.QLineEdit()
        self.randomSelectionButton = QtWidgets.QPushButton('Randomize Selection')

        vbox = QtWidgets.QVBoxLayout(self)

        vbox.addWidget(self.initialSelectionButton)
        vbox.addWidget(self.totalNumObjectLabel)
        vbox.addWidget(self.numObjectLabel)
        vbox.addWidget(self.numObjectSelection)
        vbox.addWidget(self.randomSelectionButton)

        self.initialSelectionButton.clicked.connect(self.initSelection)
        self.randomSelectionButton.clicked.connect(self.randomSelect)



    def launch(self):
        '''
        Core function to launch the UI for this class
        '''
        self.show()

    def initSelection(self):
        self.allSelection = mc.ls(sl=True)
        self.totalNum = len(self.allSelection)
        self.totalNumObjectLabel.setText('Total numbe of objects selected: {0}'.format(self.totalNum))

    def randomSelect(self):
        try:
            numOfSelection = int(self.numObjectSelection.text())
            randNum = random.sample(range(self.totalNum), numOfSelection)
            randomObjSelection = []
            
            for obj in randNum:
                randomObjSelection.append(self.allSelection[obj])

            mc.select(randomObjSelection, r=True)

        except ValueError:
            print("Number of copy specified is not an Integer")
        