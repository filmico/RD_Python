import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

ik_Jnt_Lst = [['ik_shoulder_jnt', [0, 0, 0]], 
            ['ik_elbow_jnt', [3, 0, -1]], 
            ['ik_wrist_jnt', [6, 0, 0]], 
            ['ik_wristEnd_jnt', [8, 0, 0]] ]

fk_Jnt_Lst = [['fk_shoulder_jnt', [0, 0, 0]], 
            ['fk_elbow_jnt', [3, 0, -1]], 
            ['fk_wrist_jnt', [6, 0, 0]], 
            ['fk_wristEnd_jnt', [8, 0, 0]] ]

rig_Jnt_Lst = [['rig_shoulder_jnt', [0, 0, 0]], 
               ['rig_elbow_jnt', [3, 0, -1]], 
               ['rig_wrist_jnt', [6, 0, 0]], 
               ['rig_wristEnd_jnt', [8, 0, 0]] ]

# Dict of armIK Controls
armIKCtrl = {}           
                       # offsetGrp_name, Ctrl_name, Ctrl_normal, Ctrl_radius, Ctrl_position, Ctrl_rotation
armIKCtrl['ikh_arm'] = [ik_Jnt_Lst[0][0], ik_Jnt_Lst[2][0], 'ikh_arm', 'ikRPsolver', 2, 1] 

                        # offsetGrp_name, Ctrl_name, Ctrl_normal, Ctrl_radius, Ctrl_position, Ctrl_rotation
armIKCtrl['ctrl_arm'] = ['ik_armOffset_grp', 'ik_arm_ctl', [0, 1, 0], 1, [0, 0, 0], [0, 0, 0]] 
armIKCtrl['ctrl_elbow'] = ['ik_elbowOffset_grp', 'ik_elbow_ctl', [1, 0, 0], 0.5, [0, 0, 0], [0, 0, 0]]
armIKCtrl['pv_elbow'] = ['ik_pvElbow']

# Dict of armFK Controls
armFKCtrl = {}          # offsetGrp_name, Ctrl_name, Ctrl_normal, Ctrl_radius, Ctrl_position, Ctrl_rotation
armFKCtrl['ctrl_arm'] = ['fk_armOffset_grp', 'fk_arm_ctl', [0, 1, 0], 1, [0, 0, 0], [0, 0, 0]] 
armFKCtrl['ctrl_foreArm'] = ['fk_foreArmOffset_grp', 'fk_foreArm_ctl', [0, 1, 0], 1, [0, 0, 0], [0, 0, 0]] 


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
# We receive a dictionary like armIKCtrl['ctrl_arm']
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
    createJoints(jntLst=ik_Jnt_Lst, orientJointAxis='yxz', secondaryAxis='yup')
    # Create FK Joints and orient
    createJoints(jntLst=fk_Jnt_Lst, orientJointAxis='yxz', secondaryAxis='yup')
    # Create Rig Joints and orient
    createJoints(jntLst=rig_Jnt_Lst, orientJointAxis='yxz', secondaryAxis='yup')
    
    # IK
    # --
    # Create IkHandle
    cmds.ikHandle(n=armIKCtrl['ikh_arm'][2], sj=armIKCtrl['ikh_arm'][0], ee=armIKCtrl['ikh_arm'][1], sol=armIKCtrl['ikh_arm'][3], p=armIKCtrl['ikh_arm'][4], w=armIKCtrl['ikh_arm'][5])
    
    # Obtain the Wrist position and update the dictionary of the arm control
    armIKCtrl['ctrl_arm'][4] = cmds.xform(ik_Jnt_Lst[2][0], q=True, t=True, ws=True)
    # Obtain the Wrist rotation and update the dictionary of the arm control
    armIKCtrl['ctrl_arm'][5] = cmds.xform(ik_Jnt_Lst[2][0], q=True, ro=True, ws=True)
    
    # Obtain the Elbow position for the PoleVector
    # armIKCtrl['ctrl_elbow'][4] = cmds.xform(ik_Jnt_Lst[1][0], q=True, t=True, ws=True)
    # Obtain PoleVector position and update the dictionary of the armIKCtrl['ctrl_elbow']
    armIKCtrl['ctrl_elbow'][4] = calculatePvPosition(ik_Jnt_Lst)

    # Move the Z position to place the PV to the back
    # armIKCtrl['ctrl_elbow'][4][2] = armIKCtrl['ctrl_elbow'][4][2] - 3

    # Create Wrist Control
    createControl(armIKCtrl['ctrl_arm'])
    # Parent the IkHandle to the Wrist Control
    cmds.parent(armIKCtrl['ikh_arm'][2], armIKCtrl['ctrl_arm'][1])
    # Create PV Control
    createControl(armIKCtrl['ctrl_elbow'])
    # Create PoleVector Constraint
    cmds.poleVectorConstraint(armIKCtrl['ctrl_elbow'][1], armIKCtrl['ikh_arm'][2], n=armIKCtrl['pv_elbow'][0])

    # FK
    # --
    # Obtain the arm Fk position and update the dictionary of the fk arm control
    armFKCtrl['ctrl_arm'][4] = cmds.xform(fk_Jnt_Lst[0][0], q=True, t=True, ws=True)
    # Obtain the arm Fk rotation and update the dictionary of the fk arm control
    armFKCtrl['ctrl_arm'][5] = cmds.xform(fk_Jnt_Lst[0][0], q=True, ro=True, ws=True)
    # Obtain the foreArm Fk position and update the dictionary of the fk arm control
    armFKCtrl['ctrl_foreArm'][4] = cmds.xform(fk_Jnt_Lst[1][0], q=True, t=True, ws=True)
    # Obtain the foreArm Fk rotation and update the dictionary of the fk arm control
    armFKCtrl['ctrl_foreArm'][5] = cmds.xform(fk_Jnt_Lst[1][0], q=True, ro=True, ws=True)

    # Create fk Arm Control
    createControl(armFKCtrl['ctrl_arm'])
    # Create fk foreArm Control
    createControl(armFKCtrl['ctrl_foreArm'])

    # Parent the foreArm ctrl_Grp to the Arm Ctrl
    cmds.parent(armFKCtrl['ctrl_foreArm'][0], armFKCtrl['ctrl_arm'][1]) 

    # Connect the Fk Controls to the Fk joints
    # Arm
    cmds.connectAttr(armFKCtrl['ctrl_arm'][1] + '.rotateX', fk_Jnt_Lst[0][0] + '.rotateX')
    cmds.connectAttr(armFKCtrl['ctrl_arm'][1] + '.rotateY', fk_Jnt_Lst[0][0] + '.rotateY')  
    cmds.connectAttr(armFKCtrl['ctrl_arm'][1] + '.rotateZ', fk_Jnt_Lst[0][0] + '.rotateZ')  
    # foreArm
    cmds.connectAttr(armFKCtrl['ctrl_foreArm'][1] + '.rotateX', fk_Jnt_Lst[1][0] + '.rotateX')
    cmds.connectAttr(armFKCtrl['ctrl_foreArm'][1] + '.rotateY', fk_Jnt_Lst[1][0] + '.rotateY')
    cmds.connectAttr(armFKCtrl['ctrl_foreArm'][1] + '.rotateZ', fk_Jnt_Lst[1][0] + '.rotateZ')


# createArm()

'''
# Connect IK and FK to Rig Joints
# -------------------------------
# Create Custom Attribute on Arm Control

select -r ik_arm_Ctl ;
addAttr -ln "FKIK"  -at double  -min 0 -max 1 -dv 0 |Grp_ctrl_ikWrist|ik_arm_Ctl;
setAttr -e-keyable true |Grp_ctrl_ikWrist|ik_arm_Ctl.FKIK;
'''

print "Script rig_Arm Done!"