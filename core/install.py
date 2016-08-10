import os
import sys
import shutil
import json
import coreutils

PIPECONF = open(os.path.join(os.getenv('PIPEDEV'), 'config/core.json'))
PIPEJSON = json.load(PIPECONF)

class Install(object):
    '''
    :parameter:
        showBasePath: Root path of server to setup the show
        showName: Show name is used as the root directory name for the show
    '''
    def __init__(self, showName):
        self.showName = showName
        self.projectDestination = None
        pipeConf = open(os.path.join(os.getenv('PIPEDEV'), 'config/core.json'))
        self.pipeJson = json.load(pipeConf)

    def copyStructure(self):
        '''
        Copies the template directory structure with a show root name, If the 
        show already exists prompts the user, If continued will removes the
        existing show and create a new one.
        '''
        showTemplate = os.path.join(os.getenv('PIPEDEV'), 'config/showTemplate')
        self.projectDestination = os.path.join(PIPEJSON['SERVER_ROOT'], self.showName)
        shutil.copytree(showTemplate, self.projectDestination)
        
class ShowConfig(object):
    '''
    :parameter:
        longName: Long Name for a project
        shortName: Short Name for a project
        resolution: Final full resolution for the showName
        aspectRatio: Aspect ratio for the show
        proxy: Proxy resolution for the show
        cache: Type of cahce used in the show, "alembic", "native", "cortex"
               where "native" is maya's native geometry cache.
    '''
    def __init__(self, longName, shortName, resolution=[1980,1080], 
        aspectRatio=1.77, proxy=None, cache='alembic'):
        self.project = coreutils.JsonObject()
        self.project.resolution = resolution
        self.project.aspectRatio = aspectRatio
        self.project.proxy = proxy
        self.project.longName = longName
        self.project.shortName = shortName
        self.project.cache = cache

    def create(self):
        projectBasePath = os.path.join(PIPEJSON['SERVER_ROOT'], self.project.shortName)
        projectConfigPath = str(os.path.join(projectBasePath, 'config/project.json'))
        print projectConfigPath
        openFile = open(projectConfigPath.replace('\\',"/"),'w')
        data = self.project.to_JSON()
        openFile.write(data)
        openFile.close()
        return [openFile, data]
        

def main():
    showName = raw_input("Show Name (same as show long name): ")

    # installObj = Install(showName)
    # installObj.copyStructure()

    config = ShowConfig('myproject','mpf')
    config.create()


if __name__ == '__main__':
    main()