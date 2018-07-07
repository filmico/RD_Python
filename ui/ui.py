import maya.cmds as cmds

def rigarm(*args):
    print 'Rig Arm Button Pressed!'
    import rig.rig_arm as rig_arm
    reload(rig_arm)
    rig_arm.createArm()


# Creates a menu in the main Maya Interface
myMenu = cmds.menu('RDojo_Menu', label='RD_Menu', tearOff=True, parent='MayaWindow')
# Add Item
cmds.menuItem(label='Rig_Arm', parent=myMenu, command=rigarm)

# The following will be visible on the Maya Console but not in the Output window
print "UI Loaded!"