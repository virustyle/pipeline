import maya.cmds as mc


def surfacingUtilUI():
    if mc.window('surfacingutilwin', exists=True):
        mc.deleteUI('surfacingutilwin')
    window = mc.window('surfacingutilwin',title="Surfacing Utilities",widthHeight=(400, 155))
    mc.columnLayout( adjustableColumn=True )
    mc.button(label='Multi Transfer UV',command=transferUV)
    mc.button(label='Select Similar', command=selectSimilar)
    mc.setParent( '..' )
    mc.showWindow(window)

def selectSimilar(event):
    selectedGeom = mc.ls(sl=True, l=True)
    selectedShape = mc.listRelatives(selectedGeom, s=True, f=True)
    selectionGeomList=[selectedGeom[0]]
    allPolys = mc.ls(type='mesh',l=True)

    for idNum, geom in enumerate(allPolys):
        if geom == selectedShape[0]:
            pass
        else:
            comparedResult = mc.polyCompare(selectedShape[0], geom)
            if comparedResult == 0 or comparedResult ==1:
                transformObject = mc.listRelatives(geom, parent=True, f=True)
                selectionGeomList.append(transformObject[0])

    mc.select(selectionGeomList,r=True)

def transferUV(event):
    selectionList = mc.ls(sl=True)
    sourceObject = selectionList[0]

    for idNum, geom in enumerate(selectionList):
        if idNum == 0:
            pass
        else:
            mc.transferAttributes(sourceObject, geom, transferUVs=True, sampleSpace=4)

