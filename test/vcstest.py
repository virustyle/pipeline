import os
import shutil
from vcs import versionmanager


ROOTPATH = "C:/vcstest"

def createTestEnvironment():
	if os.path.exists(ROOTPATH):
		shutil.rmtree(ROOTPATH)
	else:
		os.mkdir(ROOTPATH)

def removeTestEnvironment():
	pass

def main():
	createTestEnvironment()
	vc = versionmanager(ROOTPATH)
	vc.createversion()


if __name__ == '__main__':
	main()