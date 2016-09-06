import os, getpass, json, datetime
from sgstudio import sgframework
from PySide import QtGui, QtCore
from core import sandbox, pipeconfig
from core import assetManagerui
reload(assetManagerui)
reload(pipeconfig)

pconf = pipeconfig.PipeConfig()
conf = pconf.shotgunKeys()['coretools']

SERVER_PATH = conf['url']
SCRIPT_NAME = conf['name']
SCRIPT_KEY = conf['skey']


class AssetManager(assetManagerui.UserInterface):
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