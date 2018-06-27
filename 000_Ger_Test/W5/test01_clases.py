# Global class data can be stored outside the init.
class MyClass:
    somedata = []

    def __init__(self):
        # Or in the init if you want the data to initialize on each call to the class
        otherdata = []

    def myFunction(self, data):
        # data in here can't be accessed by other functions unless returned by that function.
        myfuncdata = [data]

        return myfuncdata

    def myOtherFunction():
        thedata = myFunction()


mc = MyClass()
print mc.myFunction('things')