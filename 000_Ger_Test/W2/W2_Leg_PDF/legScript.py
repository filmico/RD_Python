import maya.cmds as cmds

# Add a “Twist” attribute to ctrl_leg.
cmds.select('ctrl_leg') 
cmds.addAttr(shortName='Twist', longName='Twist', defaultValue=0, k=True)


# Drawing the IK
cmds.ikHandle(n= "ikh_leg", sj= "ikj_hip", ee= "ikj_ankle", sol = "ikRPsolver")
cmds.ikHandle(n= "ikh_ball", sj= "ikj_ankle", ee= "ikj_ball", sol = "ikSCsolver")
cmds.ikHandle(n= "ikh_toe", sj= "ikj_ball", ee= "ikj_toe", sol = "ikSCsolver")

# Grouping the IK
footGroups = ("grp_footPivot", "grp_heel", "grp_toe", "grp_ball", "grp_flap")
for item in footGroups:
	cmds.group(n=item, empty=True, world=True)
	

footPos = cmds.xform("loc_ctrlLeg", q=True, ws=True, t=True)	
heelPos = cmds.xform("loc_heel", q=True, ws=True, t=True)	
hipPos = cmds.xform("ikj_hip", q=True, ws=True, t=True)
anklePos = cmds.xform("ikj_ankle", q=True, ws=True, t=True)
ballPos = cmds.xform("ikj_ball", q=True, ws=True, t=True)
toePos = cmds.xform("ikj_toe", q=True, ws=True, t=True)
cmds.xform("grp_footPivot", ws=True, t=(footPos[0], 0, footPos[2]))
cmds.xform("grp_heel", ws=True, t=heelPos)
cmds.xform("grp_toe", ws=True, t=toePos)
cmds.xform("grp_ball", ws=True, t=ballPos)
cmds.xform("grp_flap", ws=True, t=ballPos)

# Now we need to put our groups and ik handles into a hierarchy.
cmds.parent('grp_heel', 'grp_footPivot')
cmds.parent('grp_toe', 'grp_heel')
cmds.parent('grp_ball', 'grp_toe')
cmds.parent('grp_flap', 'grp_toe')
cmds.parent('ikh_leg', 'grp_ball')
cmds.parent('ikh_ball', 'grp_ball')
cmds.parent('ikh_toe', 'grp_flap')
cmds.parent('grp_footPivot', 'ctrl_leg')

# No Flip Knee
cmds.spaceLocator(n='lctrPv_leg')
# pelvisPos = cmds.xform('jnt_pelvis', q=True, ws=True, t=True)
# cmds.xform('lctrPv_leg', ws=True, t=pelvisPos)
hipPos = cmds.xform('ikj_hip', q=True, ws=True, t=True)
cmds.xform('lctrPv_leg', ws=True, t=hipPos)
# Pole Vector
cmds.poleVectorConstraint ('lctrPv_leg', 'ikh_leg', weight=1)

# Twist Attribute
cmds.addAttr( shortName='Twist', longName='Twist', defaultValue=0, k=True)

# Nodos
cmds.shadingNode("plusMinusAverage", asUtility=True, n='pmaNode_LegTwist')
cmds.shadingNode("multiplyDivide", asUtility=True, n='mdNode_LegTwist')
# Conexion
cmds.connectAttr('ctrl_leg.Twist', 'mdNode_LegTwist.input1X')
cmds.connectAttr('ctrl_leg.ry', 'mdNode_LegTwist.input1Y')
cmds.connectAttr('jnt_pelvis.ry', 'mdNode_LegTwist.input1Z')
cmds.setAttr('mdNode_LegTwist.input2X', -1)
cmds.setAttr('mdNode_LegTwist.input2Y', -1)
cmds.setAttr('mdNode_LegTwist.input2Z', -1)
# cmds.connectAttr('mdNode_LegTwist.input1X', 'pmaNode_LegTwist.input1D[0]')
# cmds.connectAttr('mdNode_LegTwist.input1Y', 'pmaNode_LegTwist.input1D[1]')
# cmds.connectAttr('pmaNode_LegTwist.output1D', 'ikh_leg.twist')
cmds.connectAttr('mdNode_LegTwist.outputX', 'pmaNode_LegTwist.input1D[0]')
cmds.connectAttr('mdNode_LegTwist.outputY', 'pmaNode_LegTwist.input1D[1]')
cmds.connectAttr('pmaNode_LegTwist.output1D', 'ikh_leg.twist')


# Create the Stretchy IK Start by creating all of the nodes we will need for the stretch.
cmds.shadingNode("addDoubleLinear", asUtility=True, n='adlNode_LegStretch')
cmds.shadingNode("clamp", asUtility=True, n='clampNode_LegStretch')
cmds.shadingNode("multiplyDivide", asUtility=True, n='mdNode_LegStretch')
cmds.shadingNode("multiplyDivide", asUtility=True, n='mdNode_KneeStretch')
cmds.shadingNode("multiplyDivide", asUtility=True, n='mdNode_AnkleStretch')
# Add a “Stretch” attribute to ctrl_leg.
cmds.select('ctrl_leg') 
cmds.addAttr(shortName='Stretch', longName='Stretch', defaultValue=0, k=True)
# Create a distance tool to measure the distance between our hip and ankle joints.
hipPos = cmds.xform('ikj_hip', q=True, ws=True, t=True)
anklePos = cmds.xform('ikj_ankle', q=True, ws=True, t=True)
# Create a Distance Dimension
disDim = cmds.distanceDimension(sp=(0,0,0), ep=(0,1,0))
# Move the locators to the final destination
cmds.xform('locator1', ws=True, t=hipPos)
cmds.xform('locator2', ws=True, t=anklePos)



# Next we will need to ﬁgure out the length of the leg
cmds.rename('distanceDimension1', 'disDimNode_legStretch')
cmds.rename('locator1', 'lctrDis_hip')
cmds.rename('locator2', 'lctrDis_ankle')
cmds.parent('lctrDis_hip', 'jnt_pelvis')
cmds.parent('lctrDis_ankle', 'grp_ball')

kneeLen = cmds.getAttr('ikj_knee.tx')
# print kneeLen  
ankleLen = cmds.getAttr('ikj_ankle.tx')
# print ankleLen
legLen = (kneeLen + ankleLen)
# print legLen

# Enter our new found length values into the corresponding Nodes.
cmds.setAttr('adlNode_LegStretch.input2', legLen)
cmds.setAttr('mdNode_LegStretch.input2X', legLen)
cmds.setAttr('mdNode_KneeStretch.input2X', kneeLen)
cmds.setAttr('mdNode_AnkleStretch.input2X', ankleLen)


cmds.connectAttr('ctrl_leg.Stretch', 'adlNode_LegStretch.input1')
# cmds.setAttr ("clampNode_LegStretch.minR", 12.80004)
cmds.setAttr ("clampNode_LegStretch.minR", legLen)
cmds.setAttr ("mdNode_LegStretch.operation",  2)

# Connect the distance dimension so we always know the current length of the leg.
cmds.connectAttr('disDimNode_legStretch.distance', 'clampNode_LegStretch.inputR')
cmds.connectAttr( 'adlNode_LegStretch.output', 'clampNode_LegStretch.maxR')

# Now we feed the total value into a multiply divide so we can distribute the value to our joints.
cmds.connectAttr('clampNode_LegStretch.outputR', 'mdNode_LegStretch.input1X')
cmds.connectAttr('mdNode_LegStretch.outputX', 'mdNode_KneeStretch.input1X')
cmds.connectAttr('mdNode_LegStretch.outputX', 'mdNode_AnkleStretch.input1X')

# Finally, we output our new values into the translateX of the knee and ankle joints.
cmds.connectAttr('mdNode_KneeStretch.outputX', 'ikj_knee.tx') 
cmds.connectAttr('mdNode_AnkleStretch.outputX', 'ikj_ankle.tx')

# Make a Toe Flap
cmds.select('ctrl_leg')
cmds.addAttr( shortName='Toe_Flap', longName='Toe_Flap', defaultValue=0, k=True)
cmds.connectAttr('ctrl_leg.Toe_Flap', 'grp_flap.rx')

# Pivot for Bank and Twist
ballPos = cmds.xform('grp_ball', q=True, t=True, ws=True)
cmds.xform('ctrl_footPivot', t=ballPos)
cmds.group(n='grp_ctrl_footPivot', empty=True)
cmds.parent('grp_ctrl_footPivot', 'ctrl_footPivot')
cmds.parent('ctrl_footPivot', 'ctrl_leg')
cmds.makeIdentity( apply=True )


cmds.connectAttr('grp_ctrl_footPivot.translate', 'grp_footPivot.rotatePivot')
cmds.xform('grp_ctrl_footPivot', t=ballPos)

cmds.select('ctrl_leg')
cmds.addAttr( shortName='Foot_Pivot', longName='Foot_Pivot', defaultValue=0, k=True)
cmds.addAttr( shortName='Foot_Bank', longName='Foot_Bank', defaultValue=0, k=True)
cmds.connectAttr('ctrl_leg.Foot_Pivot', 'grp_footPivot.ry')
cmds.connectAttr('ctrl_leg.Foot_Bank', 'grp_footPivot.rz')