class My_Class:
    print "In My_Class"

    def _init__(self):
        print "In the __init__"

        # Delare jointinfo in the init
        jointinfo = (['joint_upperarm', [0.0, 5.0, 0.0]],
                     ['joint_lowerarm', [1.0, 5.0, 2.0]],
                     ['joint_hand', [0.0, 5.0, 4.0]])
        self.my_dictionary = {}

        # Call  on myFunction
        # self means we are calling the myFunction that is part of th My_Class
        # We could have a myFunction from a different class, but more on this later.
        self.myFunction(jointinfo)

        print self.mydictionary['arm']

    def myFunction(self, jointinfo, *args, **kwargs):
        """
        *args, and **kwars are two types of generic arguments that accept any argument (*args) or keyword argument (**kwargs)
        """
        """
        We can make the result of this function available to an external variable by using return, but we can also push data to the dictionary
        declared in the __init__
        """
        self.my_dictionary['arm'] = jointinfo


myclassresult = My_Class

print My_Class.self.my_dictionary
