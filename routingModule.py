import csv
import os


distancesRouteDict = {}
distancesRouteList = []
minDistance = 0
startPoint = '0001_1'
counterLine = 0
routes = 0

with open(os.path.join(os.path.dirname(__file__), 'routeSheet_12012018')) as routeSheetFile:
    routeSheetFile = csv.reader(routeSheetFile)
    for row in routeSheetFile:
        counterLine += 1

while routes < counterLine:
    print(routes, counterLine)
    with open(os.path.join(os.path.dirname(__file__), 'routeSheet_12012018')) as routeSheetFile:
        routeSheetFile = csv.reader(routeSheetFile)
        for row_i in routeSheetFile:
            id_Concatenate = startPoint + row_i[1]
            with open(os.path.join(os.path.dirname(__file__), 'totalDistances_AB_BA_12012018.csv')) as compareDistances:
                compareDistances = csv.reader(compareDistances)
                for row_j in compareDistances:
                    #print(row_j[1], 'and', id_Concatenate)
                    if (id_Concatenate == row_j[1]) and (row_j[4] not in distancesRouteList):
                        #print('THE DICT VALUE TO ADD IS:', row_j)
                        distancesRouteDict[row_j[4]] = float(row_j[6]) #It could be read: Client_id (row_j[4]) is far X meters (row_j[6]) from start point It's storaged in Dictionary (distancesRouteDict)
        if distancesRouteDict == {}:
            pass
        else:
            minDistance = min(distancesRouteDict, key=lambda k: distancesRouteDict[k]) #Formula found on internet for getting the min value in a dict
        distancesRouteList.append(minDistance)
    with open(os.path.join(os.path.dirname(__file__), 'totalDistances_AB_BA_12012018.csv')) as lookingUpClientInfo:
        lookingUpClientInfo = csv.reader(lookingUpClientInfo)
        for row_k in lookingUpClientInfo:
            if row_k[1] == startPoint + minDistance:
                with open(os.path.join(os.path.dirname(__file__), 'route_12012018.csv'), 'a') as routeFile:
                    routeFile = csv.writer(routeFile, delimiter=',')
                    routeFile.writerow([startPoint+row_k[4], row_k[5], row_k[6]])
    startPoint = minDistance  
    distancesRouteDict = {}
    routes += 1
                    