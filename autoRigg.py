from select import select
import maya.cmds as cmds
editMode = True

cmds.window("GearInc AutoTool")
cmds.rowColumnLayout(numberOfColumns = 4 )
cmds.button(l = "Create Locators", w = 200, c = "createLocators()")
cmds.button(l = "Edit Mode", w = 200, c = "lockAll(editMode)")  
cmds.button(l = "Bind Skin", w = 200, c = "bindSkin()")
cmds.button(l = "Create Joints", w = 200, c = "createJoints()")
cmds.button(l = "Create FK", w = 200, c = "createCurvesFK()")
cmds.button(l = "Create IK", w = 200, c = "createCurvesIK()")
cmds.button(l = "Create Tacticile", w = 200, c = "createTacticle()")
cmds.button(l = "Delete", w = 200, c = "delete()")

cmds.separator()
cmds.separator()

cmds.rowColumnLayout(numberOfRows  = 4, w = 200)
cmds.text("Spine Count", l = "Spine Count")
spineCount = cmds.intField(minValue = 1, maxValue = 100, value = 4)

cmds.text("Height Tacticle", l = "Height Tacticle")
heightTacticle =  cmds.intField(minValue = 1, maxValue = 10, value = 1)


cmds.showWindow()


def createLocators():
    if cmds.objExists("Gear_Master"):
        print("Gear_Master is already exists") 
    else :  cmds.group(em = True, name = "Gear_Master")
    root = cmds.spaceLocator(n = "Gear_Root")
    cmds.scale(0.1, 0.1, 0.1, root)
    cmds.move(0, 1, 0, root)
    cmds.parent(root, "Gear_Master")


    createSpine()


# function create spine
def createSpine():
    for i in range(0, cmds.intField(spineCount, query = True, value = True)):
        print(i)
        spine = cmds.spaceLocator(n = "Gear_Spine" + str(i))
        cmds.scale(0.1, 0.1, 0.1, spine)
        if i == 0 : cmds.parent(spine, "Gear_Root")
        else : cmds.parent(spine, "Gear_Spine" + str(i - 1))
        cmds.move(0, 1.25 + (0.25 * i), spine)


def createJoints():
    if cmds.objExists("RIG"):
        print("Rig allready exists")
    else:
        jointGRP =  cmds.group(em = True, name = "RIG")
        cmds.move(0, 1, 0, jointGRP)
        root = cmds.ls("Gear_Root")
        #eliminate shapes
        allSpinesNoShapes = cmds.listRelatives("Gear_Spine*", shapes = False, type="locator")
        
        spine = cmds.listRelatives(*allSpinesNoShapes, p = True, f = True)
        rootPos = cmds.xform(root, q = True, t = True, ws = True)
        cmds.joint(radius =  0.1, p = rootPos, name = "RIG_SPINE")

        global j
        for i, s in enumerate(spine):
            pos = cmds.xform(s, q = True, t = True, ws = True)
            j = cmds.joint(radius = 0.08, p = pos, name = "RIG_SPINE_" + str(i))
                                   

#function create controller IK
def createCurvesFK():
        sl = cmds.ls("RIG_SPINE_*")

        ctrlFK  = cmds.circle( nr=(0, 1, 0), r=0.3,  name = "CURVE_SPINE_FK")   
        cmds.matchTransform("CURVE_SPINE_FK" ,"RIG_SPINE" , piv = True , pos = True)
        cmds.parentConstraint(ctrlFK, "RIG_SPINE", mo = True)
        group = cmds.group(em = True, name = "Controller_FK")
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

#function create mesh

def createTacticle():
    global height
    # global tnTacticle

    for i in range(0, cmds.intField(heightTacticle, query = True, value = True)):
        print(i)
    height = i
    tacticle = cmds.polyCylinder(h = height, n = "Tacticle", sy = 50, radius = 1)
    test = cmds.move(0, float(tacticle), 0, "Tacticle")
    print(test)

#fuction bind

def bindSkin():
    joints = cmds.ls("RIG_SPINE*")
    print(joints)
    mesh = cmds.ls("Tacticle")
    print(mesh)

    cmds.bindSkin(mesh, joints)

#function lockAll

def lockAll(lock):
    axis = ["x", "y", "z"]
    attr = ["t", "r", "s"]
    nodes = cmds.listRelatives("Gear_*", allParents = True)

    for axe in axis:
        #print(axe)
        for att in attr:
            #print(att)
            for node in nodes:
                cmds.setAttr(node +"." +att+axe, lock = lock)
                cmds.setAttr(node + "." +"t"+"z" , lock = lock)
                cmds.setAttr(node + "." +"r"+"z" , lock = lock)
                cmds.setAttr(node + "." +"s"+"z" , lock = lock)

    if editMode == False:
        editMode = True
    else: editMode = False    

def delete():
    nodes = cmds.ls("Gear_*")
    cmds.delete(nodes)

