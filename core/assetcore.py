import os
import getpass
import json

class AssetCore(object):
	def __init__(self):
		self.projectName = os.environ['PROJECT']
		self.assetName = os.environ['ASSETNAME']
		self.taskStep = os.environ['TASKSTEP']
		self.assetType = os.environ['ASSETTYPE']
		self.corejson = json.load(open(os.path.join(os.environ['PIPEDEV'],
			'config/core.json'),'r'))

	def __buildSandBoxPath(self):
		projectPath = os.path.join(self.corejson['SERVER_ROOT'], 
			self.projectName)
		wrkspcBase = "workspace/asset/{0}/{1}/{2}".format(self.assetType, 
			self.assetName, self.taskStep)
		userWorkspace = os.path.join(wrkspcBase, getpass.getuser())
		sandboxPath = os.path.join(projectPath, userWorkspace)
		return sandboxPath.lower()

	def __buildMasterPath(self):
		projectPath = os.path.join(self.corejson['SERVER_ROOT'], 
			self.projectName)
		wrkspcBase = "master/asset/{0}/{1}/{2}".format(self.assetType, 
			self.assetName, self.taskStep)
		userWorkspace = os.path.join(wrkspcBase, getpass.getuser())
		masterPath = os.path.join(projectPath, userWorkspace)
		return masterPath.lower()

	def createSandBox(self):
		'''
		:parameter:
			type: There are only two types of SandBox / workspace settings, one
				  is "asset" and other is "shot"
		'''
		sandboxPath = self.__buildSandBoxPath()
		os.makedirs(sandboxPath)
		return sandboxPath

	def getSandBox(self):
		sandboxPath = self.__buildSandBoxPath()
		if os.path.exists(sandboxPath):
			return sandboxPath
		else:
			return None

	def createMaster(self):
		'''
		:parameter:
			type: There are only two types of SandBox / workspace settings, one
				  is "asset" and other is "shot"
		'''
		masterPath = self.__buildMasterPath()
		os.makedirs(masterPath)
		return masterPath

	def getMaster(self):
		masterPath = self.__buildMasterPath()
		if os.path.exists(masterPath):
			return masterPath
		else:
			return None

	def remove(self):
		pass