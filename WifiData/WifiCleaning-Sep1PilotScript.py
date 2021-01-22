import pandas as pd

# README: this code tracks user count of ap regions
def extract_time(time):
    # Extracts the information about time in data
    date = time.split('T')[0]
    t = time.split('T')[1]
    t = t.split('.')[0]
    hour = t.split(':')[0]
    minute = t.split(':')[1]
    totalMin = int(hour) * 60 + int(minute)
    return [t, totalMin, date]

#Purpose of this function unclear
def reduce(dic):
    build = ['bryancenter-roof-ap1562d-rw-8','bryancenter-roof-ap1562d-rw-10',
             '7791-bryancenter-roof-11','bryancenter-roof-ap1562d-rw-5','bryancenter-roof-ap1562d-rw-4',
             'bryancenter-roof-ap1562d-rw-7','bryancenter-roof-ap1562d-rw-6','bryancenter-tkoff-ap3502i-hc-1',
             'bryancenter-roof-ap1562d-rw-1','bryancenter-roof-ap1562d-rw-3','bryancenter-roof-ap1562d-rw-2',
             'bryancenter-0037-ap3502i-rc-1','bryancenter-245-ap3502i-hc-1','bryanctr-mcdonalds-ap3502i-rc-1',
             'bryancenter-305-ap3502i-rc-4','bryanctr-pg4-ap3502e-ow-1','bryancenter-303-ap3502i-rc-1',
             'bryancenter-251-ap3502i-hc-1','bryancenter-300-ap3502i-hc-1','bryancenter-aubon-ap3502i-rc-1',
             'bryancenter-248-ap3502i-hc-1','bryancenter-305-ap3502i-rc-2','bryancenter-104t-ap3502i-hc-1',
             'bryancenter-243-ap3502i-hc-1','bryancenter-216-ap3502i-hc-1','bryancenter-241-ap3502i-hc-1',
             'bryancenter-306-ap3502i-rc-1','bryancenter-246-ap3502i-hc-1','bryancenter-208-ap3502i-hc-1',
             'bryancenter-somewhr-ap3502i-rc-1','bryancenter-339-ap3502i-rc-1','bryancenter-304-ap3502i-rc-1']
    for i in build:
        if dic[i]<0:
            dic[i] = 0
        if dic[i]>50:
            dic[i] = int(0.85*dic[i])
            continue
        if dic[i]>30:
            dic[i] = int(0.97*dic[i])
            continue
    return dic

#Imports events from the whole day on 9/1/2020
#May need to correct file location later
dfData = pd.read_csv("WifiData/2020-09-01.csv")

#include connections of association type only
dfData = dfData[dfData['ssid'].str.contains('unknown')]

#delete duplicates
dfData=dfData.drop_duplicates(['time','ap_name','building_id','building_name',
    'ssid','affil','radiomac','netid_hashed','macaddr_hashed'])
dfData.shape

#Arranges events by time
dfData.sort_values(by=["time"], inplace=True, ascending=True)

#Check that data covers the whole day
dfData['time'].min
dfData['time'].max

#Imports dataframe with access point location
dfAps = pd.read_csv("WifiData/bryan_center_aps_2019-12-10-Edited.csv")

#Creates a dictionary for the counts of users at each access point
dicCount = {ap: 0 for ap in dfAps['name']}

#Why is this accesspoing singled out?
dicCount["7791-bryancenter-roof-11"] = 0
dicCount["bryancenter-002g-ap3602i-rc-1"] = 0

dicUser = {}

# dictionary of user to ap - need to examine more
minTime = 0

#sets date - only done once per csv file
date = extract_time(dfData['time'][0])[2] 

#creates a dataframe of returning users - need to confirm
dfRet = pd.DataFrame.from_dict(dicCount, orient='index')
dfRet.rename(columns={0: 'Count'}, inplace=True)

listTime = [date + ' {:02d}:{:02d}'.format(*divmod(0, 60)) for k in dicCount]

dfRet['Time'] = listTime
dfRet['minTime'] = [0 for k in dicCount]

#need to examine more
for ind in dfData.index:
    user = dfData['macaddr_hashed'][ind]
    ap = dfData['ap_name'][ind]
    if ap not in dicCount:
        dicCount[ap] = 0
    #     new user scenario
    if user not in dicUser:
        dicUser[user] = ap
        dicCount[ap] += 1
    #     user moving in building
    else:
        apOld = dicUser[user]
        dicUser[user] = ap
        dicCount[apOld] -= 1
        dicCount[ap] += 1
    # executes every 5 min to print ap count values
    logMinTime = extract_time(dfData['time'][ind])[1]
    if logMinTime > 5 + minTime:
        # reduce(dicCount)
        dfDicCount = pd.DataFrame.from_dict(dicCount, orient='index')
        dfDicCount.rename(columns={0: 'Count'}, inplace=True)
        dfDicCount.sort_values(by = ["Count"], inplace = True, ascending = False)
        minTime += 5
        listTime = [date + ' {:02d}:{:02d}'.format(*divmod(minTime, 60)) for k in dicCount]
        dfDicCount['Time'] = listTime
        dfDicCount['minTime'] = [minTime for k in dicCount]
        dfRet = dfRet.append(dfDicCount)

print(dicCount["bryancenter-roof-ap1562d-rw-8"])
