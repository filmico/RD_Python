#### Python Types ####

a = 'Hello'
print type(a)

b = 10
print type(b)

c = 10.26
print type(c)

d = True
print type(d)

# Casting types

print a + b        # This throws an error
print a + str(b)   # This works as b was casted as String

#### OPERATIONS ####
print 10 + 25.33
print a + ' world!'

#### CONDITIONS ####
fruit = ['apple', 'orange']
if	fruit[0] == 'apple':
	print 'I think I want apple pie'
elif fruit[0] == 'orange':
	print 'I think I want orange juice'
else:
	print 'No dessert for me, thanks.'
	
#### LOOPS ####
fruits = ['apple', 'orange']

for f in fruits:
	if	f == 'apple':
		print 'I think I want apple pie'
	elif f == 'orange':
		print 'I think I want orange juice'
	else:
		print 'No dessert for me, thanks.'	
		
	
#### Terms Comparison ####
'''
== equal to
!= not equal to
> greater than
< less than
>= greater than or equal
<= less than or equal
'''

#### DICTIONARIES ####

# Empty Dictionary
myDict = {}

# Add items to the dictionary under the key 'fruit'
myDict['fruit'] = [["apple", [1.0, 1.0, 1.0]], ["orange", [2.0, 2.0, 2.0,]] ]
# Add more items
myDict['veg'] = [["kale", [1.0, 1.0, 1.0]], ["carrots", [2.0, 2.0, 2.0]]]

for key, value in myDict.iteritems():
	print (key, value)
	



