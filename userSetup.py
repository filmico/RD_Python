# import os
# import sys
import maya.cmds as cmds

print "In Rig Tool - C:\RDojo_Python101\Repo\userSetup.py"

# Importamos el script de startup del folder de trabajo, pero solo cuando el maya haya terminado de cargar todo
# import deferred trabaja cuando el maya se pone en modo idle
cmds.evalDeferred('import startup')