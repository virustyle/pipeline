import os
import json

__author__ = "Arjun Thekkumadathil"
__email__ = "arjun.thekkumadathil@gmail.com"

class Privilages(object):
    """
    Modules helps to get the privilage database / dictionary.
    """
    def __init__(self):
        self.privilageConfigFile = os.path.join(os.getenv('PIPEDEV'), 
            'studioconfig/privilages.json').replace('\\','/')

    def getPrivilage(self):
        '''
        Returns a privilages object based on users.
        :return:
            Privilage
        '''
        configFile = open(self.privilageConfigFile,'r')
        configJson = json.load(configFile)
        return Privilage(**configJson)
        
class Privilage:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)