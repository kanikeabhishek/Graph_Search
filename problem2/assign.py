import sys
import copy as cp
# get the parameters from the command line
fileName = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

fileData = open(fileName, "r")
data = fileData.read()

# convert data into a list (separated by a ',')
data = data.rstrip('\n').split("\n")


totalVal = {}
myDict = {}
for element in data:
    '''
    This loop is to create a dictionary to represent the input format in a better way for processing it
    The key would be the user ID
    'rank' represents whether the user prefers to work alone, in a group of two or three or he has no preference
    'preferences' represents the students the current user (student) prefers to work with
    'notWannaWork' represents the students the current user (student) does not prefer to work with
    '''
    element = element.split()
    # print element[2]
    element[2] = [items for items in element[2].split(',')]
    # print element[2]
    element[3] = [items for items in element[3].split(',')]
    myDict.update({element[0]: {'rank': int(element[1]), 'preferences': element[2], 'notWannaWork': element[3]}})
#print myDict


def getMax(totalVal):
    '''
    Given a dictionary as the input, it iterates over the <key, value> pairs and returns the maximum value
    '''
    myMax = -1
    for key in totalVal:
        if int(totalVal[key]) > myMax:
            myMax = totalVal[key]
    return myMax


def getM(value, group1, myDict):
    '''
    getM() works as follows:
    For each person who has been teamed up with the current student (value), if that person is in his list of notWannaWork then
    increment the value of `val` by `m`
    Finally return `val`
    '''
    val = 0
    for each in group1[value]['team']:
        if each in myDict[value]['notWannaWork']:
            val += m
    return val


def getK(value, group1, myDict):
    '''
    getK() works as follows:
    it returns the value of `k`
    Also, technically this function can be skipped; but it is kept as is, as a good coding practice
    '''
    return k


def getN(value, group1, myDict):
    '''
    getN() works as follows:
    For each student who the current student wants to work with (preferences) but has not been teamed up with (team), increment
    the value of `val` by `n`
    Finally return `val`
    '''
    val = 0
    temp = []
    temp = myDict[value]['preferences']
    teamList = []
    teamList = group1[value]['team']
    for each in temp:
        if each == '_':
            continue
        if each not in teamList:
            val += n
    return val


def shouldAddOne(value, group1, myDict):
    '''
    shouldAddOne() works as follows:
    If the size of the team with which the current student wants to work with is not equal to the team size that he has been allocated to,
    then add 1 (since he will spend 1 minute only)
    Return 1 or 0
    '''
    count = 0
    temp = []
    temp = group1[value]['team']
    if len(temp) != myDict[value]['rank']:
        return 1
    else:
        return 0


def get_currCost(totalVal):
    '''
    This function is used to calculate the cost, given a dictionary as an input
    '''
    value = 0
    for key in totalVal:
        value += totalVal[key]
    return value


def update_cost(finalGroup):
    '''
    As the name suggests, the update_cost() function is used to update the cost after the students are grouped.
    It calculates the cost for each student and returns the values as a dictionary
    '''
    temp = 0;
    totalVal = {}
    for each in finalGroup:
        temp = getM(each, finalGroup, myDict) + getN(each, finalGroup, myDict) + shouldAddOne(each, finalGroup, myDict)
        totalVal[each] = temp
    return totalVal


def make_groups(group1, totalVal):
    '''
    As the name suggests, the make_groups() function is used to generate groups.  It works on the student with the maximum current cost
    and tries to allocate groups as per his preference.  It also ensures that the same student is not added twice in a group.
    '''
    student = max(totalVal, key=totalVal.get)
    tmp_student = totalVal
    foundMax = False
    while not foundMax:
        if myDict[student]['preferences'][0] == '_':
            s = tmp_student.pop(student)
            student = max(tmp_student, key=totalVal.get)
        else:
            foundMax = True
    templist = []
    templist.append(student)
    # add each student in djcran's preference to his team
    for each in myDict[student]['preferences']:
        if each == '_':
            continue
        # below if condition ensures that the same person is not added twice
        if len(group1[each]['team']) > 1:
            tmp_group = cp.deepcopy(group1)
            prev_team = tmp_group[each]['team']
            prev_team.pop(prev_team.index(each))
            stud_tmp_list = cp.deepcopy(templist)
            stud_tmp_list.append(each)
            tmp_group[student]['team'] = stud_tmp_list
            tmp_group[each]['team'] = stud_tmp_list
            tmp_cost = update_cost(tmp_group)
            curr_cost = update_cost(group1)
            t_cost = tmp_cost[student] + tmp_cost[each]
            c_cost = curr_cost[student] + curr_cost[each]
            for stud in prev_team:
                t_cost += tmp_cost[stud]
                c_cost += curr_cost[stud]
            if t_cost < c_cost:
                templist.append(each)
                group1 = tmp_group
                group1[student]['team'] = templist
                group1[each]['team'] = templist
            continue
        templist.append(each)
        group1[student]['team'] = templist
        group1[each]['team'] = templist
    return group1


group1 = {}
for value in myDict:
    # To start with, we treat each student as a single group.  This is our initial state
    group1.update({value: {'rank': [], 'preferences': [], 'notWannaWork': [], 'team': []}})
    # Note that getK() is not being called here since we would be working on the basis of individuals.  getK() would be called later on,
    # when we have to determine the final cost
    finalValue = shouldAddOne(value, group1, myDict) + getM(value, group1, myDict) + getN(value, group1, myDict)
    # updating the totalVal dictionary
    totalVal.update({value: finalValue})
#print group1
#print finalValue

# setting the initial threshold as `1`
threshold = 1
finalGroup = group1
Val = totalVal

while True:
    val = getMax(Val)
    finalGroup = make_groups(finalGroup, Val)
    print finalGroup
    Val = update_cost(finalGroup)
    currCost = get_currCost(Val)
    if currCost < threshold:
        break
    # increment the threshold by 10 on each iteration
    # by means of a threshold, we plan to set an upperbound on the time for which a program can run
    threshold += 10

# using a loop to detect if students without a group (like Steflee in the given example) can be (forcibly!) added to a group
# this makes sense since we assume that k>m>n, which means it would be costly to treat a student like Steflee as a team
for each in finalGroup:
    if not finalGroup[each]['team']:
        for everyPreference in myDict[each]['preferences']:
            if everyPreference == '_':
                continue
            if len(finalGroup[everyPreference]['team']) < 3:
                finalGroup[everyPreference]['team'].append(each)
                finalGroup[each]['team'] = finalGroup[everyPreference]['team']
                break
        for eachValue in finalGroup:
            if each == eachValue:
                continue
            if eachValue == '_':
                continue
            if not finalGroup[each]['team'] and len(finalGroup[eachValue]['team']) < 3:
                finalGroup[eachValue]['team'].append(each)
                finalGroup[each]['team'] = finalGroup[eachValue]['team']
                break

s = set()
counter = 0
for each in finalGroup:
    if not finalGroup[each]['team']:
        counter += 1
        continue
    t = tuple(finalGroup[each]['team'])
    s.add(t)

for each in s:
    print(" ".join(each))
print(k * (len(s) + counter) + currCost)
