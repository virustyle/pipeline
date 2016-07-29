import os
import json
import getpass
import datetime
from core import coreutils
import exceptions

class VersionManager(object):
    '''
    '''
    def __init__(self, rootPath):
        self.__rootPath = rootPath

    def createVersion(self, note):
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

    def checkoutVersion(self, workspacePath):
        pass

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

    @property
    def latestVersion(self):
        '''
        Returns the latest version, returns None if no existing version
        :Return:
            int
        '''
        version = self.getVersions()
        print version
        if version is None:
            return None
        else:
            return version[-1]

    def next(self):
        '''
        Returns next number if exists.
        :Return:
            path
        '''
        return None

    def previous(self):
        '''
        Returns next number if exists.
        :Return:
            path
        '''
        return None

    def __createInformationFile(self):
        pass

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
        print self.info.versionid
        print self.info.author
        print self.info.comment
        print self.info.timestamp
        data = self.info.to_JSON()
        openFile.write(data)
        openFile.close()