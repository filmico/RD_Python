# import os
# import sys
import maya.cmds as cmds

print "In Rig Tool - C:\RDojo_Python101\Repo\userSetup.py"

# Open Port to External IDE
if not cmds.commandPort(':4434', query=True):
    cmds.commandPort(n=':4434')
    print 'Port :4434 is open!'

# Change the current time unit to ntsc
cmds.currentUnit(time='ntsc')

# Change the current linear unit to inches
cmds.currentUnit(linear='cm')    

# Agregamos los path que necesitamos
# sys.path.append('C:/Rigging Dojo - Python 101 (On Demand)/RD_Python/')

# Importamos el script de startup del folder de trabajo, pero solo cuando el maya haya terminado de cargar todo
# import deferred trabaja cuando el maya se pone en modo idle
cmds.evalDeferred('import startup')