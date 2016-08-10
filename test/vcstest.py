import os
import shutil
from vcs import versionmanager


ROOTPATH = "C:/vcstest"
WORKSPACEPATH = "C:/vcsWPtest"

def createTestEnvironment():
    if os.path.exists(ROOTPATH):
        shutil.rmtree(ROOTPATH)
        os.mkdir(ROOTPATH)
    else:
        os.mkdir(ROOTPATH)

def createTestWorspaceEnvironment():
    if os.path.exists(WORKSPACEPATH):
        shutil.rmtree(WORKSPACEPATH)
        os.mkdir(WORKSPACEPATH)
    else:
        os.mkdir(WORKSPACEPATH)

def removeTestEnvironment():
    pass

def main():
    # createTestEnvironment()
    # createTestWorspaceEnvironment()
    vc = versionmanager.VersionManager(ROOTPATH, WORKSPACEPATH)
    # print vc.getVersions()
    # print vc.latestVersion
    # print vc.__createVersion("hello")
    # vc.checkOutVersion(12)
    # print vc.versionMetadata(12)
    # vc.checkInVersion("abc", ["C:\\vcsWPtest\\BAGA_LookDev.ma","C:\\vcsWPtest\\versionInfo.json"])


if __name__ == '__main__':
    main()