# Procedures (Functions in other Languages)

def myProc():
    print 'This is my 1st procedure'
    
# procs call    
myProc()    




# Passing Arguments
def mySecondProc(fruitType):
    print 'You ve sent an ' + fruitType
    
mySecondProc('Orange')    


# Default Arguments Parameters
def mySecondProc(fruitType='...Sorry Nothing Sent'):
    print 'You ve sent an ' + fruitType
    
mySecondProc("apple")    



# Return Values

def myThirdProc(arg1, arg2):
    return arg1 + arg2
    
sum = myThirdProc(2,5)    

print sum    
    
print myThirdProc(2,5)
