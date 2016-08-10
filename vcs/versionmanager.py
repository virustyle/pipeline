import os
import json
import getpass
import datetime
from core import coreutils
import exceptions

class VersionManager(object):
    '''
    '''
    def __init__(self, rootPath, workspacePath):
        self.__rootPath = rootPath
        self.__workspacePath = workspacePath

    def __createVersion(self, note):
        '''
        Creates a new version in the same root folder, creates version 1 if
        no other version exists
        :Return:
            path
        '''
        newVersion = None
        if self.latestVersion is None:
            newVersion = 1
        else:
            newVersion = self.latestVersion + 1
        versionPath = os.path.join(self.__rootPath, str(newVersion))
        os.mkdir(versionPath)
        currentUser = getpass.getuser()
        timeInfo = datetime.datetime.now()
        vinfo = VersionInfo(newVersion, currentUser, note, timeInfo)
        vinfo.create(os.path.join(versionPath, "versionInfo.json"))
        return versionPath

    def checkOutVersion(self, version):
        '''
        Checks out the specified version to the workspace / sandbox mentioned.

        '''
        versionPath = os.path.join(self.__rootPath, str(version))
        sourcePath = "{0}\\*".format(versionPath).replace('/',"\\")
        destinationPath =  self.__workspacePath.replace('/',"\\")
        cmd = "xcopy /Y {0} {1}".format(sourcePath, destinationPath)
        os.system(cmd)

    def checkInVersion(self, note, fileList=[]):
        sourcePath = "{0}\\*".format(self.__workspacePath).replace('/','\\')
        destinationPath = self.__createVersion(note)
        destinationPath = destinationPath.replace('/','\\')
        for eachFile in fileList:
            if "versionInfo.json" in eachFile:
                pass
            else:
                cmd = "xcopy /Y {0} {1}".format(eachFile, destinationPath)
                os.system(cmd)

    def getVersions(self):
        '''
        Returns a list of all versions in sorted order
        :Return:
            list
        '''
        versions = os.listdir(self.__rootPath)
        if len(versions) is 0:
            return None
        else:
            return sorted([int(i) for i in versions])

    def versionMetadata(self, version):
        versionPath = os.path.join(self.__rootPath, str(version))
        infoFile = open(os.path.join(versionPath, "versionInfo.json"))
        infoData = json.load(infoFile)
        return infoData

    @property
    def activeVersion(self):
        infoFile = open(os.path.join(self.__workspacePath, "versionInfo.json"))
        infoData = json.load(infoFile)
        return infoData['versionid']

    @property
    def latestVersion(self):
        '''
        Returns the latest version, returns None if no existing version
        :Return:
            int
        '''
        version = self.getVersions()
        if version is None:
            return None
        else:
            return version[-1]

class VersionInfo(object):
    '''
    '''
    def __init__(self, vid, author, comment, timestamp):
        self.info = coreutils.JsonObject()
        self.info.versionid = int(vid)
        self.info.author = str(author)
        self.info.comment = str(comment)
        self.info.timestamp = str(timestamp)

    def create(self, configFilePath):
        openFile = open(configFilePath,'w')
        data = self.info.to_JSON()
        openFile.write(data)
        openFile.close()