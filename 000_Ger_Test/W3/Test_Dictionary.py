# https://www.tutorialspoint.com/python/python_dictionary.htm

# List of Joints
jList = [
         ['ik_shoulder_jnt', [-6, 0, 1]],
         ['ik_elbow_jnt', [0, 0, 0]]
        ]


for i in jList:
    print 'JNT: ' + str(i[0]) + ' Postion: ' + str(i[1])

print '---------------------------------------------'

# Dictionary of Joints
armIK_Rig = {}
armIK_Rig['ik_shoulder_jnt'] = [-6, 0, 1]
armIK_Rig['ik_elbow_jnt'] = [0, 0, 0]

for key, value in armIK_Rig.iteritems():
    print 'JNT: ' + str(key) + ' Postion: ' + str(value)
    #print key, value

print '---------------------------------------------'
print arm_Rig


print '\n'
print 'End of Script!'
