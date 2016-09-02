import os
import json

class PipeConfig(object):
    '''
    '''
    def __init__(self):
        self.pipeDev = os.getenv('PIPEDEV')

    def shotgunKeys(self):
        shotgunConf = open(os.path.join(self.pipeDev, 'config/shotgunKeys.json'))
        shotgunJson = json.load(shotgunConf)
        return shotgunJson

    def coreConfig(self):
        pipeconf = open(os.path.join(self.pipeDev, 'config/core.json'))
        pipeJson = json.load(pipeconf)
        return pipeJson