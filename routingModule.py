import csv
import os


distancesRouteDict = {}
minDistance = 0
startPoint = '0001_1'
counterLine = 0

with open(os.path.join(os.path.dirname(__file__), 'routeSheet_12012018')) as routeSheetFile:
    routeSheetFile = csv.reader(routeSheetFile)
    for row in routeSheetFile:
        counterLine+=1

with open(os.path.join(os.path.dirname(__file__), 'routeSheet_12012018')) as routeSheetFile:
    routeSheetFile = csv.reader(routeSheetFile)
    for i, row_i in enumerate(routeSheetFile):
        id_Concatenate = startPoint + row_i[1]
        with open(os.path.join(os.path.dirname(__file__), 'totalDistances_AB_BA_12012018.csv')) as compareDistances:
            compareDistances = csv.reader(compareDistances)
            for row_j in compareDistances:
                print(row_j[1], 'and', id_Concatenate)
                if id_Concatenate == row_j[1]:
                    distancesRouteDict[row_j[4]] = row_j[6]
            print(distancesRouteDict)
            minDistance = min(distancesRouteDict, key=lambda k: distancesRouteDict[k]) #Formula found on internet for getting the min value in a dict
            startPoint = minDistance
            with open(os.path.join(os.path.dirname(__file__), 'totalDistances_AB_BA_12012018.csv')) as lookingUpClientInfo:
                lookingUpClientInfo = csv.reader(lookingUpClientInfo)
                for row_k in lookingUpClientInfo:
                    if row_k[4] == minDistance:
                        with open(os.path.join(os.path.dirname(__file__), 'route_12012018.csv'), 'a') as routeFile:
                            routeFile = csv.writer(routeFile, delimiter=',')
                            routeFile.writerow([i, row_k[4], row_k[5]])
        #distancesRouteDict = []
                    