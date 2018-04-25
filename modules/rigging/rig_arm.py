# Mel commands
'''
joint -p -6 0 1 ;
joint -e -zso -oj xyz -sao yup joint1;

joint -p 0 0 0 ;
joint -e -zso -oj xyz -sao yup joint3;

joint -p 5 0 1 ;
joint -e -zso -oj xyz -sao yup joint3;

joint -p 7 0 1 ;
joint -e -zso -oj xyz -sao yup joint4;
'''

# Create IK-FK-Bind Arm Joints
import maya.cmds as cmds

# List of Arm Joints
armIK  = (['ik_shoulder_jnt', [-6, 0, 1]], ['ik_elbow_jnt', [0, 0, 0]], ['ik_wrist_jnt', [5, 0, 1]], ['ik_wristEnd_jnt', [7, 0, 1]])
armFK  = (['fk_shoulder_jnt', [-6, 0, 1]], ['fk_elbow_jnt', [0, 0, 0]], ['fk_wrist_jnt', [5, 0, 1]], ['fk_wristEnd_jnt', [7, 0, 1]])
armRig = (['rig_shoulder_jnt', [-6, 0, 1]], ['rig_elbow_jnt', [0, 0, 0]], ['rig_wrist_jnt', [5, 0, 1]], ['rig_wristEnd_jnt', [7, 0, 1]])

# IK
for i in armIK:
    cmds.joint(name=i[0], position=i[1])
    cmds.joint(i[0], edit=True, zeroScaleOrient=True, orientJoint='xyz', secondaryAxisOrient='yup')

cmds.select(clear=True)

# FK
for i in armFK:
    cmds.joint(name=i[0], position=i[1])
    cmds.joint(i[0], edit=True, zeroScaleOrient=True, orientJoint='xyz', secondaryAxisOrient='yup')

cmds.select(clear=True)

# Rig
for i in armRig:
    cmds.joint(name=i[0], position=i[1])
    cmds.joint(i[0], edit=True, zeroScaleOrient=True, orientJoint='xyz', secondaryAxisOrient='yup')

cmds.select(clear=True)


# Create IK Rig
cmds.ikHandle( name='ikh_arm', startJoint='ik_shoulder_jnt', endEffector='ik_wrist_jnt', solver='ikRPsolver', priority=2, weight=1)
# Create Control GRP and Shape
cmds.group(empty=True, name='ik_arm_grp')
cmds.circle(name='ik_arm_ctl',  normal=(1, 0, 0), center=(0, 0, 0) )
cmds.parent('ik_arm_ctl', 'ik_arm_grp')
# Obtain the Wrist Postion
pos = cmds.xform('ik_wrist_jnt', translation = True, worldSpace=True, query=True)
# Move the Group to the IK position
cmds.xform('ik_arm_grp', translation = pos, worldSpace=True)
# Parent the IkHandle below the hand ctl shape
cmds.parent('ikh_arm', 'ik_arm_ctl')

# Create PoleVector Group & Control
cmds.group(empty=True, name='ik_poleVect_grp')
cmds.circle(name='ik_poleVect_ctl',  normal=(1, 0, 0), center=(0, 0, 0) )
cmds.parent( 'ik_poleVect_ctl', 'ik_poleVect_grp' )
# Find the lenght of the Arm (by looking at the X Axis)
armLengh = cmds.xform('ik_elbow_jnt', translation = True, worldSpace=False, query=True)[0]
# Move the poleVector to the back at the Lenght+1 of the arm
cmds.xform('ik_poleVect_grp', translation = [0,0,((armLengh*-1)-1)], worldSpace=True)

# Contraint the PoleVector to the IKHandle
cmds.poleVectorConstraint( 'ik_poleVect_ctl', 'ikh_arm' )



# Create FK Rig

# Connect IK and FK to Rig joints