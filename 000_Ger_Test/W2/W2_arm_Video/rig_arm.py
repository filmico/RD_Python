import maya.cmds as cmds
# Mel Syntax
'''
joint -p 0 0 0 ;
joint -p 3 0 -1 ;
joint -e -zso -oj xyz -sao yup joint1;
joint -p 6 0 0 ;
joint -e -zso -oj xyz -sao yup joint2;
joint -p 8 0 0 ;
joint -e -zso -oj xyz -sao yup joint3;
'''

# Create IK Joints
cmds.joint(n='ik_shoulder_jnt', p=(0, 0, 0), rad=0.5)
cmds.joint(n='ik_elbow_jnt', p=(3, 0, -1), rad=0.5)
cmds.joint(n='ik_wrist_jnt', p=(6, 0, 0), rad=0.5)
cmds.joint(n='ik_wristEnd_jnt', p=(8, 0, 0), rad=0.5)
# Orient Joints
cmds.joint('ik_shoulder_jnt' ,oj='yxz', sao='yup', ch=True, e=True)
cmds.select(cl=True)

# Create FK Joints
cmds.joint(n='fk_shoulder_jnt', p=(0, 0, 0), rad=0.5)
cmds.joint(n='fk_elbow_jnt', p=(3, 0, -1), rad=0.5)
cmds.joint(n='fk_wrist_jnt', p=(6, 0, 0), rad=0.5)
cmds.joint(n='fk_wristEnd_jnt', p=(8, 0, 0), rad=0.5)
cmds.joint('fk_shoulder_jnt' ,oj='yxz', sao='yup', ch=True, e=True)
cmds.select(cl=True)

# Create Rig Joints
cmds.joint(n='rig_shoulder_jnt', p=(0, 0, 0), rad=0.5)
cmds.joint(n='rig_elbow_jnt', p=(3, 0, -1), rad=0.5)
cmds.joint(n='rig_wrist_jnt', p=(6, 0, 0), rad=0.5)
cmds.joint(n='rig_wristEnd_jnt', p=(8, 0, 0), rad=0.5)
cmds.joint('rig_shoulder_jnt' ,oj='yxz', sao='yup', ch=True, e=True)
cmds.select(cl=True)

# Create IK rig
# -------------
# IK Handle
ikHandl = cmds.ikHandle( n='ikh_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol='ikRPsolver', p=2, w=1)
# Obtain Position and Rotation of the Wrist
posWrist = cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)
rotWrist = cmds.xform('ik_wrist_jnt', q=True, ro=True, ws=True)
 
# Create IK Control
# -----------------
arm_Ctrl = cmds.circle(n='ik_arm_Ctl', nr=(0, 1, 0), r=1, ch=0)
cmds.select(cl=True)
# Create Group
arm_group = cmds.group(em=True, n='Grp_ctrl_ikWrist')
# Parent the control to the group
cmds.parent(arm_Ctrl, arm_group)
# Move and rotate the Control to match the Wrist pos and rot
cmds.xform(arm_group, t=posWrist, ws=True)
cmds.xform(arm_group, ro=rotWrist, ws=True)

# Parent Ikh to hand Ctrl
cmds.parent(ikHandl[0], arm_Ctrl)

# Create PoleVector
# -----------------
elbow_Ctrl = cmds.circle(n='ik_elbow_Ctl', nr=(1, 0, 0), r=0.5, ch=0)
# Group it 
elbow_group = cmds.group(em=True, n='Grp_ctrl_ikElbow')
# Parent the control to the group
cmds.parent(elbow_Ctrl, elbow_group)
# Obtain Position of the elbow
posElbow = cmds.xform('ik_elbow_jnt', q=True, t=True, ws=True)
# Move the elbow control to the back of the elbow (Z must increment in 2)
cmds.xform(elbow_group, t=(posElbow[0], posElbow[1], posElbow[2] - 2) , ws=True)
# Create PoleVector Constraint
cmds.poleVectorConstraint( elbow_Ctrl, ikHandl[0], n='ik_elbow_PV')

# Create FK rig
# -------------
# Create Circles for Arm and ForeArms
fk_arm_Ctrl = cmds.circle(n='fk_arm_Ctl', nr=(0, 1, 0), r=0.75, ch=0)
fk_forArm_Ctrl = cmds.circle(n='fk_foreArm_Ctl', nr=(0, 1, 0), r=0.75, ch=0)
cmds.select(cl=True)
# Create Groups
fk_arm_group = cmds.group(em=True, n='Grp_ctrl_fkArm')
fk_foreArm_group = cmds.group(em=True, n='Grp_ctrl_fkForeArm')
# Parent Controls to each group
cmds.parent(fk_arm_Ctrl, fk_arm_group)
cmds.parent(fk_forArm_Ctrl, fk_foreArm_group)
# Obtain Arm Coordinates
fk_arm_pos = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)
# Obtain Elbow Coordinates
fk_foreArm_pos = cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)
# Move the Arm and Elbow Ctrl Groups to the respective Arm and Elbow Pos
cmds.xform(fk_arm_group, t=fk_arm_pos, ws=True)
cmds.xform(fk_foreArm_group, t=fk_foreArm_pos, ws=True)
# Obtain The Rotation of the FK Shoulder and arm
fk_shoulder_rot = cmds.xform('fk_shoulder_jnt', q=True, ro=True, ws=True)
fk_foreArm_rot = cmds.xform('fk_elbow_jnt', q=True, ro=True, ws=True)
# Rotate to group to replicate the rotation of the joints
cmds.xform(fk_arm_group, ro=fk_shoulder_rot, ws=True)
cmds.xform(fk_foreArm_group, ro=fk_foreArm_rot, ws=True)
# Parent Elbow_Grp Ctrl to Shoulder Control
cmds.parent(fk_foreArm_group, fk_arm_Ctrl)
# Parent Constraint of FK controls to Fk Joints
cmds.orientConstraint(fk_forArm_Ctrl, 'fk_elbow_jnt')
cmds.orientConstraint(fk_arm_Ctrl, 'fk_shoulder_jnt')


# Connect IK and FK to Rig Joints
# -------------------------------
# Create Custom Attribute on Arm Control
'''
select -r ik_arm_Ctl ;
addAttr -ln "FKIK"  -at double  -min 0 -max 1 -dv 0 |Grp_ctrl_ikWrist|ik_arm_Ctl;
setAttr -e-keyable true |Grp_ctrl_ikWrist|ik_arm_Ctl.FKIK;
'''


print "Script Done!"