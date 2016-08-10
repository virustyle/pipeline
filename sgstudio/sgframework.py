from __future__ import division
from shotgun_api3 import Shotgun
import datetime
import getpass
import exceptions
import os

sg = None

class SgFrameWork(object):
    def __init__(self, serverPath, scriptName, scriptKey, certificate=None):
        global sg
        sg = Shotgun(serverPath, scriptName, scriptKey, ca_certs=certificate)

    def getProject(self, projectCode):
        '''
        Returns a project entity 
            :Args:
                projectCode (string): Name of project
            :Returns:
                Project
        '''
        projectInfo = sg.find_one('Project', [['code', 'is', projectCode]],
            [proj for proj in sg.schema_field_read('Project')])
        return Project(**projectInfo)

    def getAllProjects(self, status):
        '''
        Returns a List of project entities
            :Args:
                status (string): Status of project like "Active", "Bidding"
            :Returns:
                List
        '''
        allProjects = []
        projects = sg.find('Project', [['sg_status', 'is', status]],
            [proj for proj in sg.schema_field_read('Project')])
        for project in projects:
            allProjects.append(Project(**project))
        return allProjects

    def getAllUsers(self):
        artistList = []
        artistGroup = {'type': 'PermissionRuleSet',
                       'id': 8, 'name': 'Artist'}

        allArtist = sg.find('HumanUser',[["permission_rule_set","is", artistGroup]],
            [user for user in sg.schema_field_read('HumanUser')])



        for artist in allArtist:
            artistList.append(HumanUser(**artist))

        return artistList

class BaseEntity(object):
    def __init__(self, entityType, id):
        self._entityType = entityType
        self._id = id

    def setField(self, fieldInfo):
        '''
        Sets the value for certain fields for the entity
        fieldInfo expects dictionary 
            :Args:
                fieldInfo (dict): dictionary of field name and value
            :Example:
                shot.setField({'sg_cut_in':101, 'sg_cut_out':225})
        '''
        sg.update(self._entityType, self._id, fieldInfo)

    def getField(self, fieldName):
        '''
        Returns the value for the requested field for the entity
        expects a string 
            :Args:
                fieldName (string): name of field to fetch the information 
                                    from
            :Returns:
                String
        '''
        fieldValue = sg.find_one(self._entityType, [['id', 'is', self._id]],
            [fieldName])
        return fieldValue[fieldName]


class Project(BaseEntity):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super(Project, self).__init__(self.type, self.id)

    def getShot(self, shotName):
        '''
        Returns a specific sequence entity based on sequence name
            :Args:
                shotName (string): name of shot to be fetched
            :Returns:
                Shot
        '''
        shot = sg.find_one('Shot', [['code', 'is', shotName],
            ['project','is',{'id':self.id, 'type':self.type}]],
            [shot for shot in sg.schema_field_read('Shot')])

        return Shot(**shot)

    def getAllTasks(self, statusName, stepValue=None):
        '''
        Returns a list of Task entity
            :Returns:
                List
        '''
        allTasks = []
        tasks = sg.find('Task', 
            [['project', 'is', {'id':self.id, 'type':self.type}],
            ['sg_status_list', 'is', statusName]],
            [task for task in sg.schema_field_read('Task')])

        if stepValue is not None:
            stepEntity = sg.find_one('Step',[['short_name','is',stepValue]],
                [st for st in sg.schema_field_read('Step')])

            tasks = sg.find('Task', 
            [['project', 'is', {'id':self.id, 'type':self.type}],
            ['sg_status_list', 'is', statusName],
            ['step', 'is', stepEntity]],
            [task for task in sg.schema_field_read('Task')])

        for task in tasks:
            allTasks.append(Task(**task))

        return allTasks
        
    def getAllSequences(self):
        '''
        Returns a list of sequences for current project
            :Returns:
                List
        '''
        allSequences = []
        sequences = sg.find('Sequence', 
            [['project', 'is', {'type':self.type, 'id':self.id}]],
            [seq for seq in sg.schema_field_read('Sequence')])

        for sequence in sequences:
            allSequences.append(Sequence(**sequence))

        return allSequences

    def getSequence(self, sequenceName):
        '''
        Returns a specific sequence entity based on sequence name
            :Args:
                sequenceName (string): name of sequence to be fetched
            :Returns:
                Sequence
        '''
        sequence = sg.find_one('Sequence', [['code', 'is', sequenceName],
            ['project', 'is', {'type':self.type, 'id':self.id}]],
            [seq for seq in sg.schema_field_read('Sequence')])
        return Sequence(**sequence)

    def createPlaylist(self, playlistName):
        '''
        Creates a playlist and returns playlist entity, playlist will
        be always created with the following naming convention

        playlistname-date
        lighting-05012016
        directorreview-05012016

        You cannot create playlist with same name on same day the second part
        of playlist is basically the date.

            :Args:
                playlistName (string): name of playlistName 
            :Returns:
                Playlist
        '''
        dt = datetime.datetime.now()
        currentDay = str(dt.day).zfill(2)
        currentMonth = str(dt.month).zfill(2)
        currentYear = dt.year
        projectEntity = {'type':self.type, 'id':self.id}
        playlistName = "{dept}-{day}{month}{year}".format(day=currentDay,
            month=currentMonth, year=currentYear, dept=playlistName)
        plst = sg.find("Playlist",[["code", "is",playlistName],
            ['project','is',projectEntity]])
        if len(plst) == 0:
            plst = sg.create('Playlist',{'code':playlistName,
                'project':projectEntity})
            return Playlist(**plst)
        else:
            raise exceptions.EntityExist("Playlist aready exist in same name")

    def getAllPlaylist(self):
        '''
        Returns a list of Playlist entity within the current project
            :Returns:
                List
        '''
        allPlaylist = []
        projectEntity = {'type':self.type, 'id':self.id}
        playlists = sg.find("Playlist",[["project", "is", projectEntity]],
            [plst for plst in sg.schema_field_read('Playlist')])

        for playlist in playlists:
            allPlaylist.append(Playlist(**playlist))

        return allPlaylist

    def getPlaylist(self, playlistName):
        '''
        Returns playlist with specific name provided
            :Returns:
                Playlist
        '''
        projectEntity = {'type':self.type, 'id':self.id}
        playlist = sg.find_one("Playlist", [["project", "is", projectEntity],
            ["code", "is", playlistName]],
            [plst for plst in sg.schema_field_read('Playlist')])

        return Playlist(**playlist)

    def getAsset(self, assetName):
        '''
        Returns a specific asset entity based on asset name
            :Args:
                assetName (string): name of asset to be fetched
            :Returns:
                Asset
        '''
        asset = sg.find_one('Asset', [['code', 'is', assetName],
            ['project', 'is', {'type':self.type, 'id':self.id}]],
            [ast for ast in sg.schema_field_read('Asset')])
        return Asset(**asset)

    def getAllAssets(self, assetType = None):
        '''
        Returns a list of sequences for current project
            :Returns:
                List
        '''
        allAssets = []
        if assetType is None:
            assets = sg.find('Asset',[['project', 'is', 
                {'type':self.type, 'id':self.id}]],
                [ast for ast in sg.schema_field_read('Asset')])
        else:
            pass

        for asset in assets:
            allAssets.append(Asset(**asset))

        return allAssets

class Sequence(BaseEntity):
    def __init__(self, **kwargs):
        self.code=None
        self.__dict__.update(kwargs)
        if self.code is None:
            sqInfo =sg.find_one("Sequence",[["id", "is", self.id]],
                [sq for sq in sg.schema_field_read('Sequence')])
            self.__dict__.update(**sqInfo)
        super(Sequence, self).__init__(self.type, self.id)

    def getAllShots(self):
        '''
        Returns a list of Shot entity
            :Returns:
                List
        '''
        allShots = []
        shots = sg.find('Shot', 
            [['sg_sequence', 'is', {'type':self.type, 'id':self.id}]],
            [shot for shot in sg.schema_field_read('Shot')])

        for shot in shots:
            allShots.append(Shot(**shot))

        return allShots

    def getShot(self, shotName):
        '''
        Returns a specific sequence entity based on sequence name
            :Args:
                shotName (string): name of shot to be fetched
            :Returns:
                Shot
        '''
        shot = sg.find_one('Shot', [['code', 'is', shotName],
            ['sg_sequence', 'is', {'type':self.type, 'id':self.id}]],
            [shot for shot in sg.schema_field_read('Shot')])

        return Shot(**shot)

    def getTasks(self, stepValue=None):
        '''
        Returns a specific task entity based on shot
            :Args:
                stepValue (string): step value is nothing but department name
            :Returns:
                Task
        '''
        allTasks = []
        tasks = None
        if stepValue is not None:
            stepEntity = sg.find_one('Step',[['short_name','is',stepValue]],
                [st for st in sg.schema_field_read('Step')])

            tasks = sg.find('Task', 
                [['entity', 'is', {'id':self.id, 'type':self.type}],
                ['step','is',{'type':stepEntity['type'], 'id':stepEntity['id']}]],
                [task for task in sg.schema_field_read('Task')])
        else:
            tasks = sg.find('Task', 
            [['entity', 'is', {'id':self.id, 'type':self.type}]],
            [task for task in sg.schema_field_read('Task')])

        for tk in tasks:
            allTasks.append(Task(**tk))

        return allTasks

class Shot(BaseEntity):
    def __init__(self, **kwargs):
        self.project = None
        self.__dict__.update(kwargs)
        if self.project == None:
            shInfo =sg.find_one("Shot",[["id", "is", self.id]],
                [sh for sh in sg.schema_field_read('Shot')])
            self.__dict__.update(**shInfo)
        super(Shot, self).__init__(self.type, self.id)

    def getAllTasks(self):
        '''
        Returns a list of Task entity
            :Returns:
                List
        '''
        allTasks = []
        tasks = sg.find('Task', 
            [['entity', 'is', {'id':self.id, 'type':self.type}]],
            [task for task in sg.schema_field_read('Task')])

        for task in tasks:
            allTasks.append(Task(**task))

        return allTasks

    def getTask(self, stepValue):
        '''
        Returns a specific task entity based on shot
            :Args:
                stepValue (string): step value is nothing but department name
            :Returns:
                Task
        '''
        stepEntity = sg.find_one('Step',[['short_name','is',stepValue]],
            [st for st in sg.schema_field_read('Step')])

        task = sg.find_one('Task', 
            [['entity', 'is', {'id':self.id, 'type':self.type}],
            ['step','is',{'type':stepEntity['type'], 'id':stepEntity['id']}]],
            [task for task in sg.schema_field_read('Task')])

        taskEntity = Task(**task)

        return taskEntity

class Task(BaseEntity):
    def __init__(self, **kwargs):
        self.content=None
        self.__dict__.update(kwargs)
        if self.content is None:
            taskInfo =sg.find_one("Task",[["id", "is", self.id]],
                [tk for tk in sg.schema_field_read('Task')])
            self.__dict__.update(**taskInfo)
        super(Task, self).__init__(self.type, self.id)

    def getAllVersions(self):
        '''
        Returns a list of version entity associated with the task
            :Returns:
                List
        '''
        allVersions = []        
        versions = sg.find('Version', [['entity', 'is', self.entity],
            ['sg_task', 'is', {'type':self.type, 'id':self.id}]],
            [ver for ver in sg.schema_field_read('Version')])

        for version in versions:
            allVersions.append(Version(**version))

        return allVersions

    def getVersion(self, versionNumber):
        '''
        Returns a specific Version entity based on task
            :Args:
                versionNumber (int): number of version to be fetched
            :Returns:
                Version
        '''
        version = sg.find_one('Version', [['entity', 'is', self.entity],
            ['sg_task', 'is', {'type':self.type, 'id':self.id}],
            ['code', 'is', versionNumber]],
            [ver for ver in sg.schema_field_read('Version')])
        versionEntity = Version(**version)
        return versionEntity

    def createVersion(self, filePath, versionName=None, username=None):
        '''
        Returns a specific Version entity based on task
            :Args:
                filePath (string|path): path to the movie that should be
                                         associated to the version entity
                image (Boolean): If enabled the file gets attached to 
                                 sg_path_to_frames attribute on a version
                username (string): username for the user who is currently 
                                   working by default picks up the current 
                                   OS logged in user
            :Returns:
                Version
        '''
        if username is None:
            username = getpass.getuser()

        userInfo = {'login':username}
        huser = HumanUser(**userInfo)

        fileName = os.path.basename(filePath).split('.')[0]

        data = {'sg_task':{'type':self.type,'id':self.id},
        'sg_path_to_movie':filePath,
        'user':{'type':huser.type,'id':huser.id},
        'project':self.project,
        'entity':self.entity,
        'code':fileName,
        'sg_status_list':'opn'
        }

        if os.path.isDir(filePath):
            data = {'sg_task':{'type':self.type,'id':self.id},
            'sg_reviewfolder':filePath,
            'user':{'type':huser.type,'id':huser.id},
            'project':self.project,
            'entity':self.entity,
            'code':versionName
            }
        
        ver = sg.create('Version', data)

        return Version(**ver)

    def addTimeLog(self, timeDuration, user=None):
        '''
        Add a time log entry to specific task by user
            :Args:
                timeDuration (int): minutes in integer like 20, 60, 90, 230
                user (string): username for the user who is currently working
                               by default picks up the current OS logged in
                               user
            :Returns:
                Version
        '''
        if user is None:
            user = getpass.getuser()

        userInfo = {'login':user}
        huser = HumanUser(**userInfo)
        project = self.project
        timeLog = sg.create('TimeLog',{'entity':{'id':self.id,
                                                 'type':self.type},
                                       'user':{'type':huser.type,
                                               'id':huser.id},
                                       'project':project,
                                       'duration':timeDuration})
        return TimeLog(**timeLog)

    def getAssignees(self):
        '''
        Returns a user who is assigned to the specific task
            :Returns:
                HumanUser
        '''
        allUsers = []
        users = self.getField('task_assignees')
        for user in users:
            allUsers.append(HumanUser(**user))

        return allUsers

    def createNote(self, message, taskTag=None, username=None, messageSubject=None):
        if username is None:
            username = getpass.getuser()

        userInfo = {'login':username}
        huser = HumanUser(**userInfo)

        if taskTag is not None:
            currentTag = self.tag_list
            currentTag.append(taskTag)
            self.setField({'tag_list':currentTag})

        data = {'note_links':[self.entity],
        'tasks':[{'id':self.id, 'type':self.type}],
        'user':{'type':huser.type,'id':huser.id},
        'content':message,
        'subject':messageSubject,
        'project':self.project
        }
        noteData = sg.create('Note', data)
        return noteData

    def getNotes(self):
        '''
        Returns all notes attached to the current version
            :Returns:
                Note
        '''
        # Below item commented out as its a slower method to fetch data
        # from shotgun server 

        # allNotes = []

        # for note in self.open_notes:
        #     noteData = sg.find_one('Note',[['id', 'is', note['id']]],
        #         [nt for nt in sg.schema_field_read('Note')])
        #     allNotes.append(Note(**noteData))

        allNotes = []
        notes = sg.find('Note',[['tasks', 'is', {'id':self.id, 
            'type':self.type}],
            ['note_links', 'is', self.entity],['project','is',self.project]],
            [note for note in sg.schema_field_read('Note')])

        for note in notes:
            allNotes.append(Note(**note))

        return allNotes

class Version(BaseEntity):
    def __init__(self, **kwargs):
        self.user = None
        self.__dict__.update(kwargs)
        if self.user is None:
            versionInfo =sg.find_one("Version",[["id", "is", self.id]],
                [attr for attr in sg.schema_field_read('Version')])
            self.__dict__.update(**versionInfo)
        super(Version, self).__init__(self.type, self.id)

    def getNotes(self):
        '''
        Returns all notes attached to the current version
            :Returns:
                List
        '''
        allNotes = []
        notes = sg.find('Note',[['tasks', 'is', self.sg_task],
            ['note_links', 'is', {'type':self.type, 'id':self.id}]],
            [note for note in sg.schema_field_read('Note')])

        for note in notes:
            allNotes.append(Note(**note))

        return allNotes

    def createNote(self, message, taskTag=None, username=None):
        if username is None:
            username = getpass.getuser()

        userInfo = {'login':username}
        huser = HumanUser(**userInfo)

        if taskTag is not None:
            currentTag = self.tag_list
            currentTag.append(taskTag)
            self.setField({'tag_list':currentTag})

        data = {'note_links':[{'id':self.id, 'type':self.type}],
        'tasks':[self.sg_task],
        'user':{'type':huser.type,'id':huser.id},
        'content':message,
        'project':self.project
        }
        noteData = sg.create('Note', data)
        return noteData

    def submitToPlaylist(self, playlistEntity):
        '''
        Submits current version to the passed on playlist entity
            :Returns:
                Playlist
        '''
        currentData = playlistEntity.versions
        for ver in currentData:
            if self.id == ver['id']:
                raise exceptions.EntityExist("Version aready exist in the \
                    playlist")

        currentData.append({'type':self.type, 'id':self.id})
        data = {'versions':currentData}
        plst = sg.update('Playlist', playlistEntity.id, data)
        return Playlist(**plst)

class Note(BaseEntity):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super(Note, self).__init__(self.type, self.id)
        self.retriveData = {"Attachment": ["filmstrip_image","local_storage",
                            "this_file","image"]}

    def getAttachment(self):
        '''
        Returns attachment from a note like snapshots attached with the note
            :Returns:
                Dict
        '''
        attachment = sg.note_thread_read(self.id, self.retriveData)
        return attachment

    def createAttachment(self):
        pass

class HumanUser(BaseEntity):
    def __init__(self, **kwargs):
        self.id = None
        self.sg_sparkid = None
        self.__dict__.update(kwargs)

        if self.id == None:
            userInfo =sg.find_one("HumanUser",[["login", "is", self.login]],
                [user for user in sg.schema_field_read('HumanUser')])
            self.__dict__.update(**userInfo)

        if self.sg_sparkid == None:
            userInfo =sg.find_one("HumanUser",[["id", "is", self.id]],
                [user for user in sg.schema_field_read('HumanUser')])
            self.__dict__.update(**userInfo)
            
        super(HumanUser, self).__init__(self.type, self.id)

    def getAllTasks(self, projectEntity=None, status=None):
        '''
        Returns all task for current user and can be filtered base on
        project or status
            :Args:
                projectEntity (Project): If the project name provided this 
                                         will provide the result based on
                                         project

                status (string): If provided will return the results based
                                 on the status.
            :Returns:
                Task
        '''
        allTasks=[]
        if projectEntity is not None:
            tasks = sg.find("Task",[["task_assignees", "is",
            {'type': 'HumanUser', 'id': self.id, 'name': self.name}],
            ['project', 'is',{'id':projectEntity.id,
            'type':projectEntity.type}]],
            [task for task in sg.schema_field_read('Task')])

        elif projectEntity is not None and status is not None:
            tasks = sg.find("Task",[["task_assignees", "is",
            {'type': 'HumanUser', 'id': self.id, 'name': self.name}],
            ['project', 'is',{'id':projectEntity.id,
            'type':projectEntity.type}],
            ['sg_status_list','is',status]],
            [task for task in sg.schema_field_read('Task')])

        elif status is not None:
            tasks = sg.find("Task",[["task_assignees", "is",
            {'type': 'HumanUser', 'id': self.id, 'name': self.name}],
            ['sg_status_list','is',status]],
            [task for task in sg.schema_field_read('Task')])

        else:
            tasks = sg.find("Task",[["task_assignees", "is",
            {'type': 'HumanUser', 'id': self.id, 'name': self.name}]],
            [task for task in sg.schema_field_read('Task')])

        for task in tasks:
            allTasks.append(Task(**task))

        return allTasks

    def getTimeLog(self, projectEntity=None, taskEntity=None):
        '''
        Returns a list of dictionaries for user time log based on arguments
        if none of of the arguments are given this will fetch entire data
        since tracking for the user.
            :Args:
                projectEntity (Project): Project enitity which can provide an 
                                         id attribute

                taskEntity (Task): Task entity which can provide an id attribute
            :Returns:
                List
        '''
        allTimeLogs = []

        if projectEntity is not None:
            if taskEntity is not None:
                print "Task"
            else:
                print "Project"
        else:
            allTLogs =  sg.find('TimeLog',[['user', 'is', {'id':self.id,'type':self.type}]],
                [tm for tm in sg.schema_field_read('TimeLog')])

        for timelog in allTLogs:
            allTimeLogs.append(TimeLog(**timelog))

        return allTimeLogs

    def totalTimeAlloted(self, projectEntity, startDate=None, endDate=None):
        '''
        Returns the total time alloted for the specific user between the given
        dates
            :Args:
                projectEntity (Project): Project enitity which can provide an id
                                         and type attributes

                startDate (string): date in (YYYY-MM-DD) format
                endDate (string): date in (YYYY-MM-DD) format
            :Returns:
                float / int
        '''
        allTasks=[]
        totalTime = 0

        sdate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
        edate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()

        tasks = sg.find("Task",[["task_assignees", "is",
            {'type': 'HumanUser', 'id': self.id, 'name': self.name}],
            ['project', 'is',{'id':projectEntity.id,'type':projectEntity.type}]],
            [task for task in sg.schema_field_read('Task')])

        for task in tasks:
            stDate = datetime.datetime.strptime(task['start_date'], "%Y-%m-%d").date()
            edDate = datetime.datetime.strptime(task['due_date'], "%Y-%m-%d").date()
            if stDate >= sdate:
                if edDate <= edate:
                    totalTime += task['duration']

        timeInHour = totalTime / 60

        return timeInHour

    def totalTimeLogged(self, projectEntity, startDate=None, endDate=None):
        '''
        Returns the total time logged by the specific user between the given
        dates
            :Args:
                projectEntity (Project): Project enitity which can provide an id
                                         and type attributes

                startDate (string): date in (YYYY-MM-DD) format
                endDate (string): date in (YYYY-MM-DD) format
            :Returns:
                float / int
        '''
        allTasks=[]
        totalTime = 0

        sdate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
        edate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()

        tasks = sg.find("Task",[["task_assignees", "is",
            {'type': 'HumanUser', 'id': self.id, 'name': self.name}],
            ['project', 'is',{'id':projectEntity.id,'type':projectEntity.type}]],
            [task for task in sg.schema_field_read('Task')])

        for task in tasks:
            stDate = datetime.datetime.strptime(task['start_date'], "%Y-%m-%d").date()
            edDate = datetime.datetime.strptime(task['due_date'], "%Y-%m-%d").date()
            if stDate >= sdate:
                if edDate <= edate:
                    totalTime += task['time_logs_sum']

        timeInHour = totalTime / 60

        return timeInHour

class Playlist(BaseEntity):
    def __init__(self, **kwargs):
        self.id = None
        self.versions = None
        self.__dict__.update(kwargs)
        if self.id == None or self.versions == None:
            userInfo =sg.find_one("Playlist",[["code", "is", self.code]],
                [attr for attr in sg.schema_field_read('Playlist')])
            self.__dict__.update(**userInfo)
        super(Playlist, self).__init__(self.type, self.id)

    def getSubmissions(self):
        '''
        Returns a list of versions submited to the current playlist
            :Returns:
                List
        '''
        versionList = []
        for ver in self.versions:
            versionList.append(Version(**ver))
        return versionList

class TimeLog(BaseEntity):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super(TimeLog, self).__init__(self.type, self.id)

class Asset(BaseEntity):
    def __init__(self, **kwargs):
        self.project = None
        self.__dict__.update(kwargs)
        if self.project == None:
            assetInfo =sg.find_one("Asset",[["id", "is", self.id]],
                [sh for sh in sg.schema_field_read('Asset')])
            self.__dict__.update(**assetInfo)
        super(Asset, self).__init__(self.type, self.id)

    def getAllTasks(self):
        '''
        Returns a list of Task entity
            :Returns:
                List
        '''
        allTasks = []
        tasks = sg.find('Task', 
            [['entity', 'is', {'id':self.id, 'type':self.type}]],
            [task for task in sg.schema_field_read('Task')])

        for task in tasks:
            allTasks.append(Task(**task))

        return allTasks

    def getTask(self, stepValue):
        '''
        Returns a specific task entity based on shot
            :Args:
                stepValue (string): step value is nothing but department name
            :Returns:
                Task
        '''
        stepEntity = sg.find_one('Step',[['short_name','is',stepValue]],
            [st for st in sg.schema_field_read('Step')])

        task = sg.find_one('Task', 
            [['entity', 'is', {'id':self.id, 'type':self.type}],
            ['step','is',{'type':stepEntity['type'], 'id':stepEntity['id']}]],
            [task for task in sg.schema_field_read('Task')])

        taskEntity = Task(**task)

        return taskEntity

class Department(BaseEntity):
    def __init__(self, **kwargs):
        self.id = None
        self.__dict__.update(kwargs)
        if self.id == None:
            deptInfo =sg.find_one("Department",[["name", "is", self.name]],
                [dept for dept in sg.schema_field_read('Department')])
            self.__dict__.update(**deptInfo)
        super(Department, self).__init__(self.type, self.id)