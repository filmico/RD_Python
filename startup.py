import maya.cmds as cmds

print 'Startup! - C:\RDojo_Python101\Repo\startup.py'

# Let's import the UI  (folderName.PythonFile)
import ui.ui as ui
reload(ui)  # left it like this in develop mode. It always load the .py instead of the .pyc
