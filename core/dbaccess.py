import os
import sqlite3

__author__ = "Arjun Thekkumadathil"
__email__ = "arjun.thekkumadathil@gmail.com"

class DBaccess(object):
    """
    Thisi gives basic access to the database of project
    """
    def __init__(self, project):
        self.__dbFile = os.path.join(os.getenv('PIPEDEV'), 
            'databases/{0}.json'.format(project)).replace('\\','/')
        self.__dbConnection = sqlite3.connect(self.__dbFile)
        self.__dbCursor = self.__dbConnection.cursor()

    @property
    def dbFile(self):
        return self.__dbFile

    @property
    def dbConnection(self):
        return self.__dbConnection

    @property
    def dbCursor(self):
        return self.__dbCursor

    def getAllTasks(self):
        cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")

    def getTask(self, taskid):
        pass

class Task(object):
    def __init__(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

class User(object):
    def __init__(self):
        pass

    def create(self):
        pass

    def update(self):
        pass