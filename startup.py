import maya.cmds as cmds

print 'Startup! - C:\Rigging Dojo - Python 101 (On Demand)\RD_Python\startup.py'

# Change the current time unit to ntsc
cmds.currentUnit(time='ntsc')

# Change the current linear unit to inches
cmds.currentUnit(linear='cm')

# Let's import the UI  (folderName.PythonFile)
import ui.ui as ui
reload(ui)  # left it like this in develop mode
