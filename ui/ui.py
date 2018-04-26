import maya.cmds as cmds

def rigarm(*args):
    print 'Rig Arm Button Pressed!'


# Creates a menu in the main Maya Interface
myMenu = cmds.menu('RDojo_Menu', label='RD_Menu', tearOff=True, parent='MayaWindow')
# Add Item
cmds.menuItem(label='Rig_Arm', parent=myMenu, command=rigarm)





print "UI Loaded!"