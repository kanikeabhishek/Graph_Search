import sys

fileName = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

fileData = open(fileName, "r")
data = fileData.read()

#convert data into a list (separated by ,)
data = data.split("\n")

#create a dictionary
myDict = {}
for element in data:
    element=element.split()
    myDict.update({element[0]:{'rank':element[1], 'preferences':element[2], 'notWannaWork':element[3]}})

'''
#Can ignore!
for value in myDict:
    value=value.split()
    #print(value[0], ":", value[1])
    print(value)
'''

'''
#Accessing the individuals elements like a <key, value> pair
for value in myDict:
    print(value, myDict[value]['preferences'])
    if "chen464" in myDict[value]['preferences']:
        print("Found")
    else:
        print("Not found")
'''

def getM(value, group1, myDict):
    '''
    For each person who has been teamed up with him (value), if that person is in his list of notWannaWork then 
    increment the value of `val` by `m`
    Finally return `val`
    '''
    val=0
    for each in group1[value]['team']:
        if each in myDict[value]['notWannaWork']:
            val+=m
    print("In getM: ", value, val)
    return val

def getK(value, group1, myDict):
    '''
    return (number of teams)*k
    '''
    print("In getK: ", value, k)
    return k

def getN(value, group1, myDict):
    '''
    For each person who we wants to work with (preferences) but has not been teamed up with (team), increment 
    the value of `val` by `n`
    Finally return `val`
    '''
    val=0
    temp=[]
    temp = myDict[value]['preferences']
    temp = temp.split(",")
    for each in temp:
        print("Check for: ", each)
        if each not in group1[value]['team']:
            val+=n
    print("In getN: ", value, val)
    return val

def shouldAddOne(value, group1, myDict):
    '''
    If the size of the team which he wants to work in is not equal to the team size that he has been allocated to,
    then add 1 (since he will spend 1 minute only)
    Return 1 or 0
    '''
    if len(group1[value]['team']) != myDict[value]['rank']:
        print("In shouldAddOne, for: ", value, ": ", 1)
        return 1
    else:
        print("In shouldAddOne, for: ", value, ": ", 0)
        return 0

#group1 would be a dict containing data like djcran and his choices, preferences, notWannaWorks and his team
#djcran: {rank:0, preferences: chen464,zehzhang, notWannaWork: kapadia, team: chen464,kapadia,zehzhang}, etc.
group1={}
totalVal={}

for value in myDict:
    #treating each individual as a group
    group1.update({value:{'rank':"", 'preferences':"", 'notWannaWork':"", 'team':""}})
    finalValue = shouldAddOne(value, group1, myDict) + getM(value, group1, myDict) + getN(value, group1, myDict) + getK(value, group1, myDict)
    totalVal.update({value: finalValue})
    print("--------------------- ", "Done with ", value, "as ", finalValue, " --------------------------------------------------")

#print(group1)
print(totalVal)
