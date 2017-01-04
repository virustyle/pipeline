import sys
from PySide import QtGui
from PySide import QtCore
import taskmanagerui

__author__ = "Arjun Thekkumadathil"
__email__ = "arjun.thekkumadathil@gmail.com"

class TaskManager(taskmanagerui.UserInterface):
    def __init__(self):
        super(TaskManager, self).__init__()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ac = TaskManager()
    ac.launch()
    sys.exit(app.exec_())