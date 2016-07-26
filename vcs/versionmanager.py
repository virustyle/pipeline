import exceptions

class VersionManager(object):
    '''
    '''
    def __init__(self, rootPath):
        self.rootPath = rootPath
        self.currenVersion = None

    def createVersion(self):
        pass

    def next(self):
        return self.currenVersion +1

    def previous(self):
        if self.currenVersion is not 1:
            return self.currenVersion - 1
        elif self.currenVersion is 1:
            raise exceptions.VersionError("Current version is the first version")

    def __createInformationFile(self):
        pass