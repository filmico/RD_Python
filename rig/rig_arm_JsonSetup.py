import maya.cmds as cmds
import os
import json

path = os.environ['RIGGING_TOOL']
pathJson = path + '/layout/'

# Dict to contain all the arm definition
armDict = {}

armDict['ik_Jnts'] = [['ik_shoulder_jnt', [0, 0, 0]], 
                            ['ik_elbow_jnt', [3, 0, -1]], 
                            ['ik_wrist_jnt', [6, 0, 0]], 
                            ['ik_wristEnd_jnt', [8, 0, 0]] ]

armDict['fk_Jnts'] = [['fk_shoulder_jnt', [0, 0, 0]], 
                            ['fk_elbow_jnt', [3, 0, -1]], 
                            ['fk_wrist_jnt', [6, 0, 0]], 
                            ['fk_wristEnd_jnt', [8, 0, 0]] ]

armDict['rig_Jnts'] = [['rig_shoulder_jnt', [0, 0, 0]], 
                            ['rig_elbow_jnt', [3, 0, -1]], 
                            ['rig_wrist_jnt', [6, 0, 0]], 
                            ['rig_wristEnd_jnt', [8, 0, 0]] ]        

# IK Controls
                         # offsetGrp_name, Ctrl_name, Ctrl_normal, Ctrl_radius, Ctrl_position, Ctrl_rotation
armDict['ik_Ikh']= [armDict['ik_Jnts'][0][0], armDict['ik_Jnts'][2][0], 'ikh_arm', 'ikRPsolver', 2, 1] 
armDict['ik_Ctl'] = ['ik_armOffset_grp', 'ik_arm_ctl', [0, 1, 0], 1, [0, 0, 0], [0, 0, 0]] 
armDict['ik_PoleVect_Ctl'] = ['ik_elbowOffset_grp', 'ik_elbow_ctl', [1, 0, 0], 0.5, [0, 0, 0], [0, 0, 0]]
armDict['ik_Pv'] = ['ik_pvElbow']

# FK Controls
                        # offsetGrp_name, Ctrl_name, Ctrl_normal, Ctrl_radius, Ctrl_position, Ctrl_rotation
armDict['fk_upperLimb_Ctl'] = ['fk_armOffset_grp', 'fk_arm_ctl', [0, 1, 0], 1, [0, 0, 0], [0, 0, 0]] 
armDict['fk_lowerLimb_Ctl'] = ['fk_foreArmOffset_grp', 'fk_foreArm_ctl', [0, 1, 0], 1, [0, 0, 0], [0, 0, 0]] 
                            
# Guardar el Diccionario a JSon
utils.writeJson(pathJson + 'arm_Definition.json', armDict)

# Lee el archivo de Setup y lo guarda en el diccionario
armDict_De_Json = utils.readJson(pathJson + 'arm_Definition.json')

# Convierte a diccionario (json.loads)
armDict_Nuevo = {}
armDict_Nuevo = json.loads(armDict_De_Json)

for key, value in armDict_Nuevo.iteritems():
	print 'Key: ' + str(key), 'Values: ' + str(value)	

