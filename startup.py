import maya.cmds as cmds

print 'Startup! - C:\RDojo_Python101\Repo\startup.py'

# Open Port to External IDE
if not cmds.commandPort(':4434', query=True):
    cmds.commandPort(name=':4434', sourceType="python")
    print 'Port :4434 is open for IDE -> Python!'

if not cmds.commandPort(':7001', query=True):
    cmds.commandPort(name=':7001', sourceType="mel")
    print 'Port :7001 is open for IDE -> Mel!'

if not cmds.commandPort(':7002', query=True):
    cmds.commandPort(name=':7002', sourceType="python")
    print 'Port :7002 is open for IDE -> Python!'

# Change the current time unit to ntsc
cmds.currentUnit(time='ntsc')

# Change the current linear unit to inches
cmds.currentUnit(linear='cm')    

# Agregamos los path que necesitamos
# sys.path.append('C:/Rigging Dojo - Python 101 (On Demand)/RD_Python/')

# Let's import the UI  (folderName.PythonFile)
import ui.ui as ui
# reload(ui)  # left it like this in develop mode. It always load the .py instead of the .pyc
