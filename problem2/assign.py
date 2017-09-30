import sys

fileName = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

fileData = open(fileName, "r")
data = fileData.read()

#convert data into a list (separated by ,)
data = data.split("\n")

#global totalVal
totalVal={}
#create a dictionary
myDict = {}
for element in data:
    element=element.split()
    element[2]=[items for items in element[2].split(',')]
    element[3] = [items for items in element[3].split(',')]
    myDict.update({element[0]:{'rank':int(element[1]), 'preferences':element[2], 'notWannaWork':element[3]}})

def getMax(totalVal):
    myMax=-1
    for key in totalVal:
        if int(totalVal[key])>myMax:
            myMax=totalVal[key]
    return myMax

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
    #imp#print("In getM: ", value, val)
    return val

def getK(value, group1, myDict):
    '''
    return (number of teams)*k
    '''
    #imp#print("In getK: ", value, k)
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
    #imp#print("Printing temp: ", temp)
    teamList=[]
    teamList = group1[value]['team']
    #imp#print("Printing teamList: ", teamList)
    for each in temp:
        #imp#print("Check for: ", each)
        if each == '_':
            continue
        if each not in teamList:
            val+=n
    #imp#print("In getN: ", value, val)
    return val

def shouldAddOne(value, group1, myDict):
    '''
    If the size of the team which he wants to work in is not equal to the team size that he has been allocated to,
    then add 1 (since he will spend 1 minute only)
    Return 1 or 0
    '''
    count=0
    temp=[]
    temp=group1[value]['team']
    if len(temp) != myDict[value]['rank']:
        #print("In shouldAddOne for: ", value, ": ", 1)
        return 1
    else:
        #print("In shouldAddOne, for: ", value, ": ", 0)
        return 0

def get_currCost(totalVal):
    value=0
    for key in totalVal:
        value+=totalVal[key]
    return value

def get_cost(finalGroup):
    temp=0;
    totalVal={}
    for each in finalGroup:
        print("Get_cost:")
        print(each, " has cost: ")
        print(getM(each, finalGroup, myDict))
        print(getN(each, finalGroup, myDict))
        print(shouldAddOne(each, finalGroup, myDict))
        print("Done with the prints!")
        temp=getM(each, finalGroup, myDict) + getN(each, finalGroup, myDict) + shouldAddOne(each, finalGroup, myDict)
        print("----------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", each, temp)
        #totalVal.update({value:{temp})
        totalVal[each]=temp
    return totalVal
    
def make_groups(group1, totalVal):
    student = max(totalVal, key=totalVal.get)
    templist=[]
    templist.append(student)
    print(student)
    #add each student in djcran's preference to his team
    for each in myDict[student]['preferences']:
        #below if condition to check that the same person doesn't get added twice
        if each=='_':
            continue
        if len(group1[each]['team'])>1:
            continue
        templist.append(each)
        group1[student]['team'] = templist
        group1[each]['team'] = templist
    return group1

#group1 would be a dict containing data like djcran and his choices, preferences, notWannaWorks and his team
#djcran: {rank:0, preferences: chen464,zehzhang, notWannaWork: kapadia, team: chen464,kapadia,zehzhang}, etc.
group1={}
for value in myDict:
    #treating each individual as a group
    group1.update({value:{'rank':[], 'preferences':[], 'notWannaWork':[], 'team':[]}})
    finalValue = shouldAddOne(value, group1, myDict) + getM(value, group1, myDict) + getN(value, group1, myDict) #+ getK(value, group1, myDict)
    totalVal.update({value: finalValue})
    print("--------------------- ", "Done with ", value, "as ", finalValue, " --------------------------------------------------")

# Dict totalVal contains all the students along with their ranks as a <key, value> pair
print("totalVal after a single run: ", totalVal)

threshold = 4
totalCost = 999999; #just hard coded to make it enter
print("Printing make_groups() call: ", make_groups(group1, totalVal))

finalGroup=group1
Val=totalVal
i=2000

print("+++++++++++++++++++++++++++++++++++++ Main loop output from below! +++++++++++++++++++++++++++++++++++++")
while i>0:
    val = getMax(Val)
    print("Max value is: ", val, " so will start grouping for it!")
    finalGroup = make_groups(finalGroup, Val)
    Val = get_cost(finalGroup)
    print("totalVal: ", Val)
    currCost = get_currCost(Val)
    if currCost<threshold:
        print("Exiting... with the final cost and threshold as: ", currCost, threshold)
        print("Final group is: ", finalGroup)
        break
    threshold+=10
    i=i-1

#using a loop to detect if people without a group can be (forcibly!) added to a group
for each in finalGroup:
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", each)	
    if not finalGroup[each]['team']:
        print("***************************", each)
        for everyPreference in myDict[each]['preferences']:
            if everyPreference=='_':
                continue
            if len(finalGroup[everyPreference]['team'])<3:
                finalGroup[everyPreference]['team'].append(each)
                print("After appending (1): ", finalGroup[everyPreference]['team'])
                finalGroup[each]['team']=finalGroup[everyPreference]['team']
                break
        for eachValue in finalGroup:
            if eachValue=='_':
                continue
            if not finalGroup[each]['team'] and len(finalGroup[eachValue]['team'])<3:
                finalGroup[eachValue]['team'].append(each)
                #finalGroup[each]['team'].append(eachValue)
                print("After appending (1): ", finalGroup[everyPreference]['team'])
                finalGroup[each]['team']=finalGroup[eachValue]['team']
                break

print("... Done now! ...")
print("Final finalGroup is: ", finalGroup)

s=set()
for each in finalGroup:
    t=tuple(finalGroup[each]['team'])
    s.add(t)
print(len(s))

for each in s:
    print(" ".join(each))
print(k*len(s)+currCost)
