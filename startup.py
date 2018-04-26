import maya.cmds as cmds
# os is a python module that allows access to operating system commnands
import os

print 'Startup! - C:\Rigging Dojo - Python 101 (On Demand)\RD_Python\startup.py'

# Change the current time unit to ntsc
cmds.currentUnit(time='ntsc')

# Change the current linear unit to inches
cmds.currentUnit(linear='cm')

# Create a new environment variable that will provide easy access
# Later and just calling os.environ["RDOJO] we will get the path
os.environ["RDOJO"] = "C:/Rigging Dojo - Python 101 (On Demand)/RD_Python"

# Let's import the UI  (folderName.PythonFile)
import ui.ui as ui
reload(ui)  # left it like this in develop mode. It always load the .py instead of the .pyc
