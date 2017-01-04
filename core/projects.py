import os
import json

__author__ = "Arjun Thekkumadathil"
__email__ = "arjun.thekkumadathil@gmail.com"

class Projects(object):
    """
    Modules helps to get the project properties of every project in the studio
    """
    def __init__(self):
        self.__projectConfigFile = os.path.join(os.getenv('PIPEDEV'), 
            'studioconfig/projects.json').replace('\\','/')

    @property
    def projectConfigFile(self):
        return self.__projectConfigFile

    def getAllActiveProject(self):
        '''
        Returns all the active project
        :return:
            Project
        '''
        allProjects = []
        configFile = open(self.__projectConfigFile,'r')
        configJson = json.load(configFile)
        for pj in configJson:
            if configJson[pj]['status'] == 'active':
                allProjects.append(Project(**configJson[pj]))
        return allProjects

    def getAllProject(self):
        '''
        Returns all projects, including disabled ones
        :return:
            Project
        '''
        allProjects = []
        configFile = open(self.__projectConfigFile,'r')
        configJson = json.load(configFile)
        for pj in configJson:
            allProjects.append(Project(**configJson[pj]))
        return allProjects

    def getProject(self, projectname):
        '''
        Returns all the active project
        :parameter:
            projectname (str): Specific project name to be fetched
        :return:
            Project
        '''
        configFile = open(self.__projectConfigFile,'r')
        configJson = json.load(configFile)[projectname]
        return Project(**configJson)


class Project:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)