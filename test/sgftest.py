import sys
import time
sys.path.append("E:\\pipeline")
from sgstudio import sgframework
print sgframework.__file__


reload(sgframework)

SERVER_PATH = "https://pipetest.shotgunstudio.com"
SCRIPT_NAME = 'info'
SCRIPT_KEY = '90aea59877cebbb6445bf7e77f5d90a9663ff0ba45d5eebae168703a6ad98cd2'


a = sgframework.SgFrameWork(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

# artists = a.getAllUsers()
# for i in artists:
# 	print i.login
# verdict = {'type':'Version','id':6013}
# verObject = sgframework.Version(**verdict)
# verObject.createNote("this is a new message")
# verObject.setField({'sg_status_list':'ispapr'})

# def timeTestProject():
# 	t1 = time.time()
# 	allprojects = a.getAllProjects('Active')
# 	t2 = time.time()
# 	print str(t2-t1)
# 	t1 = time.time()
# project = a.getProject('gattuaurbattu')
# asset = project.getAsset('char-gatturnd')
# task = asset.getTask('chmdl')
# task.createNote("this is my subject", "this is by message")
# print project.getAllTasks('rndr1')

# sh = project.getShot('ep101-sh110')
# print sh.sg_cut_in
# print sh.sg_cut_out
# assets = project.getAllAssets()
# print assets
# myasset = {'code':'char-batturnd','id':947}
# ast = sgframework.Asset(**myasset)
# print ast.getAllTasks()
# 	t2 = time.time()
# 	print str(t2-t1)

# for i in range(15):
# 	timeTestProject()
# sqinfo = {'id':21,'type':'Sequence'}
# sq = sgframework.Sequence(**sqinfo)
# print sq.code
# allprojects = a.getAllProjects('Active')
project = a.getProject('myproject')
# ast = project.createAsset('mytest', 'Character', 'blajfksdf')
asset = project.getAsset("jack")
print asset.task_template
# project = a.getProject('gattuaurbattu')
# print project.getAllAssets()
# # print project.id
# # pl = project.createPlaylist("animation")
# pl = project.getPlaylist("animation-02032016")
# print pl
# pl = project.getAllPlaylist()
# for i in pl:
#     print i.getSubmissions
# print project

# allSequence =  project.getAllSequences()
# for i in allSequence:
#   print i.code

# sq = project.getSequence('ep100')
# tasks = sq.getAllTasks()
# for i in tasks:
# 	print i.content

# tsk = sq.getTasks('kbg')
# for i in tsk:
# 	print i.content


# allShots = sq.getAllShots()
# for i in allShots:
#   print i.code
#   print i.id
#   print i.open_notes

# print sq.getField('sg_status_list')
# print sq.getField('sg_shots')
# print sq.getField('shots')

# shot = sq.getShot("ep100-sh021")
# print shot.tasks
# for i in allShots:
#   print i.getField('code')
# shot = sq.getShot('002')
# print shot.code
# print shot.project
# print shot.sg_status_list

# print shot.getField('sg_status_list')

# print shot.getAllTasks()
# task =  shot.getTask('anim')
# print task.sg_status_list

# for i in range(10):
# 	ta = time.time()
# 	notesList =task.getNotes()
# 	tb = time.time()
# 	print tb-ta
# task.createNote('some kind of note again2', "my ctag")
# mytaskdict = {'type': 'Task', 'id': 2281, 'name': 'Animation'}

# print task.sg_latestversion
# ver = task.createVersion(filePath='//tai-isilon/3D-Projects/Fruit-Ninja/workspace/animation/ep103/review/fnj_ep103sh069_an01_v00.avi')
# print task.sg_status_list
# task.setField({'sg_status_list':'ip'})

# task =  shot.getTask('chfs')
# print task.sg_status_list
# print task.sg_status_list
# print dir(task)
# print task.getAssignees()
# print task.getField('start_date')
# allVers = task.getAllVersions()

# for i in allVers:
# 	print i.code
# 	print i.created_at
# version = task.getVersion('fnj_ep999sh006_an01_v12')
# abc = version.submitToPlaylist(pl)
# print abc
# notes = version.getNotes()[0]

# attachments = notes.getAttachment()
# print attachments
# userInfo = {'login':"boban.m"}
# huser = sgframework.HumanUser(**userInfo)
# houralloted = huser.totalTimeAlloted(project,"2016-02-29", "2016-03-04")
# hoursLogged = huser.totalTimeLogged(project,"2016-02-29", "2016-03-04")

# print houralloted
# print hoursLogged


# tasks = huser.getAllTasks()
# print tasks
# t = tasks[-1]
# print tasks
# for i in t.__dict__.keys():
#     print i, t.__dict__[i]

# sh = t.entity
# shObj = sgframework.Shot(**sh)
# print shObj.name
# print shObj.description
# print shObj.getField('description')
# for i in tasks:
#     userData = i.getAssignees()[0]
#     print userData.id
#     print userData.name
#     print userData.getField('login')
#     for j in dir(userData):
#         print j

# playlistName = {"code":"animation-25012016"}
# pl = sgframework.Playlist(**playlistName)
# print pl.versions

# vr= pl[0].getSubmissions()[0]
# print vr.sg_path_to_movie
# for g in dir(vr):
#     print g