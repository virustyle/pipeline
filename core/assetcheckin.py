import os, datetime
from PySide import QtGui, QtCore
from core import assetcore, checkinui
reload(checkinui)

class AssetCheckIn(checkinui.UserInterface):
    def __init__(self):
        super(AssetCheckIn, self).__init__()
        self.loadWorkspaceFiles()

    def loadWorkspaceFiles(self):
        core = assetcore.AssetCore()
        try:
            sanboxPath = core.createSandBox()
        except WindowsError:
            sandboxPath = core.getSandBox()

        allFiles = os.listdir(sandboxPath)
        for each in allFiles:
            print os.stat(os.path.join(sandboxPath, each))