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

# Create IK Arm Joints
import maya.cmds as cmds
cmds.joint( name='ik_shoulder_jnt' ,p=[-6, 0, 1] )
cmds.joint('ik_shoulder_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.joint( name='ik_elbow_jnt' ,p=[0, 0, 0] )
cmds.joint('ik_elbow_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.joint( name='ik_wrist_jnt' ,p=[5, 0, 1] )
cmds.joint('ik_wrist_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.joint( name='ik_wristEnd_jnt' ,p=[7, 0, 1] )
cmds.joint('ik_wristEnd_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.select(clear=True)

# Create FK Arm Joints
cmds.joint( name='fk_shoulder_jnt' ,p=[-6, 0, 1] )
cmds.joint('fk_shoulder_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.joint( name='fk_elbow_jnt' ,p=[0, 0, 0] )
cmds.joint('fk_elbow_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.joint( name='fk_wrist_jnt' ,p=[5, 0, 1] )
cmds.joint('fk_wrist_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.joint( name='fk_wristEnd_jnt' ,p=[7, 0, 1] )
cmds.joint('fk_wristEnd_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.select(clear=True)

# Create Rig Arm Joints
cmds.joint( name='rig_shoulder_jnt' ,p=[-6, 0, 1] )
cmds.joint('rig_shoulder_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.joint( name='rig_elbow_jnt' ,p=[0, 0, 0] )
cmds.joint('rig_elbow_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.joint( name='rig_wrist_jnt' ,p=[5, 0, 1] )
cmds.joint('rig_wrist_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.joint( name='rig_wristEnd_jnt' ,p=[7, 0, 1] )
cmds.joint('rig_wristEnd_jnt', edit=True, zeroScaleOrient = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')

cmds.select(clear=True)

# Create IK Rig
cmds.ikHandle( name='ikh_arm', startJoint='ik_shoulder_jnt', endEffector='ik_wrist_jnt' , solver='ikRPsolver', priority=2, weight=1)
# Create Control GRP and Shape
cmds.group(empty=True, name='ik_arm_grp')
cmds.circle(name='ik_arm_ctl',  normal=(1, 0, 0), center=(0, 0, 0) )
cmds.parent( 'ik_arm_ctl', 'ik_arm_grp' )
# Obtain the Wrist Postion
pos = cmds.xform('ik_wrist_jnt', translation = True, worldSpace=True, query=True)
# Move the Group to the IK position
cmds.xform('ik_arm_grp', translation = pos, worldSpace=True)
# Parent the IkHandle below the hand ctl shape
cmds.parent( 'ikh_arm', 'ik_arm_ctl' )



# Create FK Rig

# Connect IK and FK to Rig joints