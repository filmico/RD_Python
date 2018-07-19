import maya.cmds as cmds                # For the Maya Commands
import system.utils as utils            # To use the Json and other utilities
import maya.OpenMaya as OpenMaya        # Used in the function calculatePvPosition
import os                               # Used to read the environment variables EG. ['RIGGING_TOOL']
import json                             # To be able to unpack the Json into a dictionary of python

path = os.environ['RIGGING_TOOL']
pathJson = path + '/layout/'

# Lee el archivo de Setup
armDefinition = utils.readJson(pathJson + 'arm_Definition.json')

# Convierte a diccionario (json.loads)
armDict = {}
armDict = json.loads(armDefinition)

# Create and orient Joints based on a list of joint names and positions
def createJoints(jntLst, orientJointAxis, secondaryAxis, zeroLast=False):   
    for item in jntLst:
        cmds.joint(n=item[0], p=item[1], rad=0.5)

    # Orient Joints
    cmds.joint(jntLst[0][0], e=True, oj=orientJointAxis, sao=secondaryAxis, ch=True)

    # Zero the joint orient of the last Jnt
    if zeroLast:
        lastJointIndex = len(jntLst) - 1
        lastJointName = jntLst[lastJointIndex][0]
        cmds.setAttr( lastJointName + '.jointOrientX', 0)
        cmds.setAttr( lastJointName + '.jointOrientY', 0)
        cmds.setAttr( lastJointName + '.jointOrientZ', 0)
        cmds.select(cl=True)

    # Deselect
    cmds.select(cl=True)

def calculatePvPosition(jnts):
    start = cmds.xform(jnts[0][0], q=True, ws=True, t=True)
    mid = cmds.xform(jnts[1][0], q=True, ws=True, t=True)
    end = cmds.xform(jnts[2][0], q=True, ws=True, t=True)
    startV = OpenMaya.MVector(start[0], start[1], start[2])
    midV = OpenMaya.MVector(mid[0], mid[1], mid[2])
    endV = OpenMaya.MVector(end[0], end[1], end[2])

    startEnd = endV - startV
    startMid = midV - startV

    dotP = startMid * startEnd
    
    proj = float(dotP) / float(startEnd.length())
    startEndN = startEnd.normal()
    projV = startEndN * proj
    arrowV = startMid - projV
    
    # Distance Separation of the PoleVector (Valor Fijo  ->  arrowV *= 2)
    arrowV *= cmds.getAttr(jnts[1][0] + '.translateY')
    
    finalV = arrowV + midV
        
    return ([finalV.x, finalV.y, finalV.z])


# This function alow to create the wrist and pole vectors controllers
# We receive a dictionary like armDict['ik_Ctl']
def createControl(ctrlDetail):
    # Create Control GRP
    cmds.group(empty=True, name=ctrlDetail[0])
    # Create Control Shape
    cmds.circle(n=ctrlDetail[1], nr=ctrlDetail[2], r=ctrlDetail[3], ch=0)
    # Parent the control to the OffsetGroup
    cmds.parent(ctrlDetail[1], ctrlDetail[0])
    cmds.select(clear=True)
    # Move and rotate the Control to match indicated position
    cmds.xform(ctrlDetail[0], t=ctrlDetail[4], ws=True)
    cmds.xform(ctrlDetail[0], ro=ctrlDetail[5], ws=True)


def createArm():

    # JOINTS
    # -------
    # Create IK Joints and orient
    createJoints(jntLst=armDict['ik_Jnts'], orientJointAxis='yxz', secondaryAxis='yup')
    # Create FK Joints and orient
    createJoints(jntLst=armDict['fk_Jnts'], orientJointAxis='yxz', secondaryAxis='yup')
    # Create Rig Joints and orient
    createJoints(jntLst=armDict['rig_Jnts'], orientJointAxis='yxz', secondaryAxis='yup')
    
    # IK
    # --
    # Create IkHandle
    cmds.ikHandle(n=armDict['ik_Ikh'][2], sj=armDict['ik_Ikh'][0], ee=armDict['ik_Ikh'][1], sol=armDict['ik_Ikh'][3], p=armDict['ik_Ikh'][4], w=armDict['ik_Ikh'][5])
    
    # Obtain the Wrist position and update the dictionary of the arm control
    armDict['ik_Ctl'][4] = cmds.xform(armDict['ik_Jnts'][2][0], q=True, t=True, ws=True)
    # Obtain the Wrist rotation and update the dictionary of the arm control
    armDict['ik_Ctl'][5] = cmds.xform(armDict['ik_Jnts'][2][0], q=True, ro=True, ws=True)
    
    # Obtain the Elbow position for the PoleVector
    # armDict['ik_PoleVect_Ctl'][4] = cmds.xform(armDict['ik_Jnts'][1][0], q=True, t=True, ws=True)
    # Obtain PoleVector position and update the dictionary of the armDict['ik_PoleVect_Ctl']
    armDict['ik_PoleVect_Ctl'][4] = calculatePvPosition(armDict['ik_Jnts'])

    # Move the Z position to place the PV to the back
    # armDict['ik_PoleVect_Ctl'][4][2] = armDict['ik_PoleVect_Ctl'][4][2] - 3

    # Create Wrist Control
    createControl(armDict['ik_Ctl'])
    # Parent the IkHandle to the Wrist Control
    cmds.parent(armDict['ik_Ikh'][2], armDict['ik_Ctl'][1])
    # Create PV Control
    createControl(armDict['ik_PoleVect_Ctl'])
    # Create PoleVector Constraint
    cmds.poleVectorConstraint(armDict['ik_PoleVect_Ctl'][1], armDict['ik_Ikh'][2], n=armDict['ik_Pv'][0])

    # FK
    # --
    # Obtain the arm Fk position and update the dictionary of the fk arm control
    armDict['fk_upperLimb_Ctl'][4] = cmds.xform(armDict['fk_Jnts'][0][0], q=True, t=True, ws=True)
    # Obtain the arm Fk rotation and update the dictionary of the fk arm control
    armDict['fk_upperLimb_Ctl'][5] = cmds.xform(armDict['fk_Jnts'][0][0], q=True, ro=True, ws=True)
    # Obtain the foreArm Fk position and update the dictionary of the fk arm control
    armDict['fk_lowerLimb_Ctl'][4] = cmds.xform(armDict['fk_Jnts'][1][0], q=True, t=True, ws=True)
    # Obtain the foreArm Fk rotation and update the dictionary of the fk arm control
    armDict['fk_lowerLimb_Ctl'][5] = cmds.xform(armDict['fk_Jnts'][1][0], q=True, ro=True, ws=True)

    # Create fk Arm Control
    createControl(armDict['fk_upperLimb_Ctl'])
    # Create fk foreArm Control
    createControl(armDict['fk_lowerLimb_Ctl'])

    # Parent the foreArm ctrl_Grp to the Arm Ctrl
    cmds.parent(armDict['fk_lowerLimb_Ctl'][0], armDict['fk_upperLimb_Ctl'][1]) 

    # Connect the Fk Controls to the Fk joints
    # Arm
    cmds.connectAttr(armDict['fk_upperLimb_Ctl'][1] + '.rotateX', armDict['fk_Jnts'][0][0] + '.rotateX')
    cmds.connectAttr(armDict['fk_upperLimb_Ctl'][1] + '.rotateY', armDict['fk_Jnts'][0][0] + '.rotateY')  
    cmds.connectAttr(armDict['fk_upperLimb_Ctl'][1] + '.rotateZ', armDict['fk_Jnts'][0][0] + '.rotateZ')  
    # foreArm
    cmds.connectAttr(armDict['fk_lowerLimb_Ctl'][1] + '.rotateX', armDict['fk_Jnts'][1][0] + '.rotateX')
    cmds.connectAttr(armDict['fk_lowerLimb_Ctl'][1] + '.rotateY', armDict['fk_Jnts'][1][0] + '.rotateY')
    cmds.connectAttr(armDict['fk_lowerLimb_Ctl'][1] + '.rotateZ', armDict['fk_Jnts'][1][0] + '.rotateZ')


# createArm()

'''
# Connect IK and FK to Rig Joints
# -------------------------------
# Create Custom Attribute on Arm Control

select -r ik_arm_Ctl ;
addAttr -ln "FKIK"  -at double  -min 0 -max 1 -dv 0 |Grp_ctrl_ikWrist|ik_arm_Ctl;
setAttr -e-keyable true |Grp_ctrl_ikWrist|ik_arm_Ctl.FKIK;
'''

print "Script rig_Arm Done! print Cambio 8"
# createArm()