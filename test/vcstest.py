import os
import shutil
from vcs import versionmanager


ROOTPATH = "C:/vcstest"

def createTestEnvironment():
    if os.path.exists(ROOTPATH):
        shutil.rmtree(ROOTPATH)
        os.mkdir(ROOTPATH)
    else:
        os.mkdir(ROOTPATH)

def removeTestEnvironment():
    pass

def main():
    # createTestEnvironment()
    vc = versionmanager.VersionManager(ROOTPATH)
    # print vc.getVersions()
    # print vc.latestVersion
    print vc.createVersion("hello")


if __name__ == '__main__':
    main()