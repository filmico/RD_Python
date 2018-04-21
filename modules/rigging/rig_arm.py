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