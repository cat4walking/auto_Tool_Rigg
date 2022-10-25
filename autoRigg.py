from select import select
import maya.cmds as cmds

cmds.window("GearInc AutoTool")
cmds.rowColumnLayout(numberOfColumns = 1 )
cmds.button(l = "Create Locators", w = 200, c = "createLocators()")
cmds.button(l = "Create Joints", w = 200, c = "createJoints()")
cmds.button(l = "Create Tacticile", w = 200, c = "createTacticle()")
cmds.button(l = "Create FK", w = 200, c = "createCurvesFK()")
cmds.button(l = "Create IK", w = 200, c = "createCurvesIK()")
cmds.button(l = "Bind Skin", w = 200, c = "bindSkin()")
cmds.button(l = "Delete", w = 200, c = "delete()")

cmds.separator()
cmds.separator()

cmds.rowColumnLayout(numberOfRows  = 4, w = 200)

cmds.text("Spine Count", l = "Spine Count")
spineCount = cmds.intField(minValue = 1, maxValue = 100, value = 4)

cmds.text("Height Count", l = "Height Count")
count = cmds.intField(minValue = 1, maxValue = 100, value = 2)

cmds.text("Thickness", l = "Thickness")
thickNess = cmds.intField(minValue = 1, maxValue = 10, value = 1)



cmds.showWindow()

#function create locators
def createLocators():
    if cmds.objExists("Gear_Master"):
        print("Gear_Master is already exists") 
    else :  cmds.group(em = True, name = "Gear_Master")
    root = cmds.spaceLocator(n = "GEAR_SPINE")
    cmds.scale(0.1, 0.1, 0.1, root)
    cmds.move(0, 0, 0, root)
    cmds.parent(root, "Gear_Master")

    createSpine()

# function create spine
def createSpine():
    global height
    for i in range(0, cmds.intField(count, query = True, value = True)):
        print(i)
    height = i+1

    for i in range(0, cmds.intField(spineCount, query = True, value = True)):
        spine = cmds.spaceLocator(n = "Gear_Spine" + str(i))
        cmds.scale(0.1, 0.1, 0.1, spine)
        cmds.move(0, height + i, spine)
        if i == 0 : cmds.parent(spine, "GEAR_SPINE")
        else : cmds.parent(spine, "Gear_Spine" + str(i - 1))
        cmds.move(0, height + (i * height), spine)

#function create joints
def createJoints():
    if cmds.objExists("RIG"):
        print("Rig allready exists")
    else:
        jointGRP =  cmds.group(em = True, name = "RIG")
        cmds.move(0, 1, 0, jointGRP)
        root = cmds.ls("GEAR_SPINE")
        #eliminate shapes
        allSpinesNoShapes = cmds.listRelatives("Gear_Spine*", shapes = False, type="locator")
        
        spine = cmds.listRelatives(*allSpinesNoShapes, p = True, f = True)
        rootPos = cmds.xform(root, q = True, t = True, ws = True)
        cmds.joint(radius =  0.1, p = rootPos, name = "RIG_SPINE")

        global j
        for i, s in enumerate(spine):
            pos = cmds.xform(s, q = True, t = True, ws = True)
            j = cmds.joint(radius = 0.1, p = pos, name = "RIG_SPINE_" + str(i))
                                   

#function create controller FK
def createCurvesFK():
        sl = cmds.ls("RIG_SPINE_*")

        ctrlFK  = cmds.circle( nr=(0, 1, 0), r=2,  name = "CURVE_SPINE_FK")   
        cmds.matchTransform("CURVE_SPINE_FK" ,"RIG_SPINE" , piv = True , pos = True)
        cmds.parentConstraint(ctrlFK, "RIG_SPINE", mo = True)
        cmds.group(em = True, name = "Controller_FK")
        cmds.parent(ctrlFK, "Controller_FK")
        for i, s in enumerate(sl):
            ctrlName = s.replace("_jnt", "_ctrl")
            ctrl = cmds.circle( nr=(0, 1, 0), r=2,  name = "CURVE_SPINE_FK_" + str(i))
            cmds.matchTransform("CURVE_SPINE_FK_" + str(i),"RIG_SPINE_" + str(i), piv = True , pos = True)
            CreteaCtrl = cmds.parentConstraint(ctrl, s, mo = True)
            if i == 0 : cmds.parent(ctrl, "CURVE_SPINE_FK")
            else : cmds.parent(ctrl, "CURVE_SPINE_FK_"  + str(i - 1))     


#function create controller IK
def createCurvesIK():  
    cmds.ikHandle (sj="RIG_SPINE", ee= j)

#function count element in list
def countElement():
    all = cmds.listRelatives("Gear_Spine*", shapes = False, type="locator")
    global allCount 
    allCount = 0
    for element in all:
        allCount += 1      
    return allCount

#function create mesh
def createTacticle():
    countElement()
    totalHeight = height * allCount

    for i in range(0, cmds.intField(thickNess, query = True, value = True)):
        print(i)
    r = i + 1
    # global tnTacticle
    cmds.polyCylinder(h = totalHeight, n = "Tacticle", sy = 50, radius = r)
    cmds.move(0, allCount, 0, "Tacticle")

#fuction bind
def bindSkin():
    joints = cmds.ls("RIG_SPINE*")
    print(joints)
    mesh = cmds.ls("Tacticle")
    print(mesh)

    cmds.bindSkin(mesh, joints)


def delete():
    nodes = cmds.ls("Gear_*")
    cmds.delete(nodes)

