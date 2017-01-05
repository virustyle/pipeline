import sys
from PySide import QtGui
from PySide import QtCore
import taskmanagerui

__author__ = "Arjun Thekkumadathil"
__email__ = "arjun.thekkumadathil@gmail.com"

class TaskManager(taskmanagerui.UserInterface):
    def __init__(self):
        super(TaskManager, self).__init__()
        self.assetTaskType.clicked.connect(self.assetShotSelection)
        self.shotTaskType.clicked.connect(self.assetShotSelection)

    def assetShotSelection(self):
        if self.assetTaskType.isChecked():
            self.taskSeqName.setEnabled(False)
            self.taskShotName.setEnabled(False)
            self.taskAssetName.setEnabled(True)
        elif self.shotTaskType.isChecked():
            self.taskAssetName.setEnabled(False)
            self.taskSeqName.setEnabled(True)
            self.taskShotName.setEnabled(True)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ac = TaskManager()
    ac.launch()
    sys.exit(app.exec_())