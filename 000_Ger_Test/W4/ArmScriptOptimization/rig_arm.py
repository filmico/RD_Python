import maya.cmds as cmds

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
armIKCtrl['ctrl_arm'] = ['ik_armOffset_grp', 'ik_arm_ctl', [1, 0, 0], 1, [0, 0, 0], [0, 0, 0]] 
armIKCtrl['pv_arm'] = ['ik_armPv', [1, 0, 0], [0, 0, 0]]  # 

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

def createControl(ctrlDetail):
	# We receive the dictionary armIKCtrl['ctrl_arm']
	cmds.circle(n=armIKCtrl['ctrl_arm'][1], nr=armIKCtrl['ctrl_arm'][2], r=ctrlRadius, ch=0)






def createIkSystem(ikhName, startJnt, endJnt, ctrlOffsetName, ctrlName, ctrlNormal, ctrlRadius,
	               pvName, pvCtlOffsetName, pvCtlName, pvCtlNormal, pvCtlRadius, pvJointRef, pvZDirecton):

	# Create a dictionary to add the name of the created items
	components = {}

	# Create IkHandle
	ikHandle = cmds.ikHandle( n=ikhName, sj=startJnt, ee=endJnt, sol='ikRPsolver', p=2, w=1)		
	components["ikHandle"] = ikHandle[0]
	
	# Obtain Position and Rotation of the endJnt to create Controller
	posEndJnt = cmds.xform(endJnt, q=True, t=True, ws=True)
	rotEndJnt = cmds.xform(endJnt, q=True, ro=True, ws=True)
	
	# Create arm Control
	ikControl = cmds.circle(n=ctrlName, nr=ctrlNormal, r=ctrlRadius, ch=0)
	cmds.select(cl=True)
	components["ikCtrl"] = ikControl

	# Create Group
	cmds.group(n=ctrlOffsetName, em=True)
	components["ikOffsetG"] = ctrlOffsetName
	
	# Parent the control to the group
	cmds.parent(components["ikCtrl"], components["ikOffsetG"])

	# Move and rotate the Control to match the Wrist pos and rot
	cmds.xform(components["ikOffsetG"], t=posEndJnt, ws=True)
	cmds.xform(components["ikOffsetG"], ro=rotEndJnt, ws=True)

	# Parent Ikh to hand Ctrl
	cmds.parent(components["ikHandle"], components["ikCtrl"])

	# Create PoleVector Ctrl Shape
	pvCtl = cmds.circle(n=pvCtlName, nr=pvCtlNormal, r=pvCtlRadius, ch=0)

	components["ik_pvCtl"] = pvCtl

	# Create PoleVector offset Group
	pvCtlOffset_Grp = createGroup(name=pvCtlOffsetName)
	components["ik_pvOffsetGrp"] = pvCtlOffset_Grp

	# Parent the control to the group
	cmds.parent(components["ik_pvCtl"], components["ik_pvOffsetGrp"])

	# Deselect
	cmds.select(cl=True)

	# Find Position for the PoleVector
	pvPosRef = cmds.xform(pvJointRef, q=True, t=True, ws=True)

	# Move the elbow control to the back of the elbow (Z must increment in 2)
	cmds.xform(components["ik_pvOffsetGrp"], t=(pvPosRef[0], pvPosRef[1], pvPosRef[2] + pvZDirecton), ws=True)	

	# Create PoleVector Constraint
	cmds.poleVectorConstraint( components["ik_pvCtl"], components["ikHandle"], n=pvName)

	return components


# Create arm Joints and orient (3 arms - IK - FK - RIG)
createJoints(jntLst=ik_Jnt_Lst, orientJointAxis='yxz', secondaryAxis='yup')
createJoints(jntLst=fk_Jnt_Lst, orientJointAxis='yxz', secondaryAxis='yup')
createJoints(jntLst=rig_Jnt_Lst, orientJointAxis='yxz', secondaryAxis='yup')

# Create IK rig
ikArmComponents = createIkSystem(ikhName='ikh_arm', 
	                             startJnt=ik_Jnt_Lst[0][0], 
	                             endJnt=ik_Jnt_Lst[2][0],
	                             ctrlOffsetName='Grp_ik_arm_ctl',
	                             ctrlName='ik_arm_ctl',
	                             ctrlNormal=[0, 1, 0],
	                             ctrlRadius=1,
	                             pvName='ik_elbow_PV',
	                             pvCtlOffsetName='Grp_ik_elbow_Ctl',                            
	                             pvCtlName='ik_elbow_Ctl',
	                             pvCtlNormal=[1, 0, 0],
	                             pvCtlRadius=0.5,
	                             pvJointRef=ik_Jnt_Lst[1][0],
	                             pvZDirecton=-2
	                             )

for key, value in ikArmComponents.iteritems():
	print key, value



'''
Lo que sigue no se convirtio al modo del script de arriba pero son los pasos que faltan

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

select -r ik_arm_Ctl ;
addAttr -ln "FKIK"  -at double  -min 0 -max 1 -dv 0 |Grp_ctrl_ikWrist|ik_arm_Ctl;
setAttr -e-keyable true |Grp_ctrl_ikWrist|ik_arm_Ctl.FKIK;
'''






print "Script Done!"
