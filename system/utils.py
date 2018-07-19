import maya.cmds as cmds
import json as json

# Variable de Entorno seteada en el modulo Riggint_tool.mod

# import os 
# print os.environ['RIGGING_TOOL']	


# JSON
# =====

def writeJson(fileName, data):
	with open(fileName, 'w') as outFile:
		json.dump(data, outFile)
	file.close(outFile)

def readJson(fileName):
	with open(fileName, 'r') as inFile:
		data = (open(inFile.name, 'r').read())
	return data

'''
	JSON How to Use it
	------------------

	import maya.cmds as cmds
	import os
	import system.utils as utils
	import json
	reload (system.utils)

	path = os.environ['RIGGING_TOOL']
	pathJson = path + '/layout/'

	# Lista
	# ------
	ik_Jnt_Lst = [['ik_shoulder_jnt', [0, 0, 0]], 
	            ['ik_elbow_jnt', [3, 0, -1]], 
	            ['ik_wrist_jnt', [6, 0, 0]], 
	            ['ik_wristEnd_jnt', [8, 0, 0]] ]

	# Graba
	utils.writeJson(pathJson + 'lista.json', armIKCtrl) 
	       
	# Lee
	ik_Jnt_Lst_De_Json = utils.readJson(pathJson + 'lista.json')
	print 'Lista: ' + str(ik_Jnt_Lst_De_Json)

	            
	# Diccionario
	# -----------
	armIKCtrl = {}          
	                       # offsetGrp_name, Ctrl_name, Ctrl_normal, Ctrl_radius, Ctrl_position, Ctrl_rotation
	armIKCtrl['ikh_arm'] = [ik_Jnt_Lst[0][0], ik_Jnt_Lst[2][0], 'ikh_arm', 'ikRPsolver', 2, 1] 

	# Graba
	utils.writeJson(pathJson + 'diccionario.json', armIKCtrl)

	# Lee
	armIKCtrl_De_Json = utils.readJson(pathJson + 'diccionario.json')

	# Convierte a diccionario (json.loads)
	armIKCtrl_Nuevo = {}
	armIKCtrl_Nuevo = json.loads(armIKCtrl_De_Json)

	print 'Complete Diccionary: ' + str(armIKCtrl_Nuevo)

	for key, value in armIKCtrl_Nuevo.iteritems():
		print 'Key: ' + str(key), 'Values: ' + str(value)	
		
	print armIKCtrl['ikh_arm'][2]		

'''