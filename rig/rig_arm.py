import maya.cmds as cmds

# Create IK-FK-Rig Arm

# List of Arm Joints
armIK = (['ik_shoulder_jnt', [-6, 0, 1]], ['ik_elbow_jnt', [0, 0, 0]], ['ik_wrist_jnt', [5, 0, 1]], ['ik_wristEnd_jnt', [7, 0, 1]])
armFK = (['fk_shoulder_jnt', [-6, 0, 1]], ['fk_elbow_jnt', [0, 0, 0]], ['fk_wrist_jnt', [5, 0, 1]], ['fk_wristEnd_jnt', [7, 0, 1]])
armRig = (['rig_shoulder_jnt', [-6, 0, 1]], ['rig_elbow_jnt', [0, 0, 0]], ['rig_wrist_jnt', [5, 0, 1]], ['rig_wristEnd_jnt', [7, 0, 1]])


# Dict of armIK Controls
armIKCtrl = {}
armIKCtrl['grpOffsetDetails_arm'] = ['ik_arm_grp']  # Name of the grp
armIKCtrl['ctrlShapeDetails_arm'] = ['ik_arm_ctl', [1, 0, 0], [0, 0, 0]]  # name, normal, center


# Create Joints from the list received
def createJoints(jntsInfo):
    # Cycle an create the joints
    for i in jntsInfo:
        cmds.joint(name=i[0], position=i[1])
        cmds.joint(i[0], edit=True, zeroScaleOrient=True, orientJoint='xyz', secondaryAxisOrient='yup')
    # Deselect the last joint
    cmds.select(clear=True)

def createControl(ctrlName, ctrlNormal, ctrlCenter, ctrlOffsetGroupName):

    # Create Control GRP
    cmds.group(empty=True, name=ctrlOffsetGroupName)
    # Create Shape to be placed under the offset group
    cmds.circle(name=ctrlName, normal=ctrlNormal, center=ctrlCenter)
    # Delete Construction History
    cmds.delete(constructionHistory=True)
    # Parent the control to the OffsetGroup
    cmds.parent(ctrlName, ctrlOffsetGroupName)
    cmds.select(clear=True)


def posConstraint(objList, world=True):

    # Obtain Parent position
    parentPos = cmds.xform(objList[1], translation=True, worldSpace=world, query=True)

    # Move Child to the Parent's pos
    cmds.xform(objList[0], translation=parentPos, worldSpace=world)
    cmds.select(clear=True)


def createArm():

    # Create IK Joints
    createJoints(armIK)
    # Create FK Joints
    createJoints(armFK)
    # Create Rig Joints
    createJoints(armRig)

    # Create armIK Control
    createControl(armIKCtrl['ctrlShapeDetails_arm'][0],   # control Shape
                  armIKCtrl['ctrlShapeDetails_arm'][1],   # control Normal
                  armIKCtrl['ctrlShapeDetails_arm'][2],   # control Center
                  armIKCtrl['grpOffsetDetails_arm'][0]    # control Offset Group
                  )

    # Move armIK Control to Wrist Position
    posConstraint([armIKCtrl['grpOffsetDetails_arm'][0], armIK[2][0]], world=True)


    # Create IK Rig
    cmds.ikHandle( name='ikh_arm', startJoint='ik_shoulder_jnt', endEffector='ik_wrist_jnt', solver='ikRPsolver', priority=2, weight=1)

    # # Create Control GRP
    # cmds.group(empty=True, name='ik_arm_grp')
    #
    # # Create Shape to be placed under the offset group
    # cmds.circle(name='ik_arm_ctl',  normal=(1, 0, 0), center=(0, 0, 0) )
    # cmds.parent('ik_arm_ctl', 'ik_arm_grp')

    # Obtain the Wrist Postion
    # pos = cmds.xform('ik_wrist_jnt', translation = True, worldSpace=True, query=True)

    # Move the Group to the IK position
    # cmds.xform('ik_arm_grp', translation = pos, worldSpace=True)

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

    # Connect IK and FK to Rig joints (Blender Custom Attribute, etc)