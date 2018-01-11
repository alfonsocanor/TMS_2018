import googlemaps
import geocoder
from geopy.distance import vincenty
from urllib.request import urlopen
import json
import os
import csv
import math
import time

''' gmaps = googlemaps.Client(key='AIzaSyBMwXuzxKO2EY2eoNX163Iojydhmi39i1U') #From googlaMaps API
#print(dir(gmaps))
gi = gmaps.distance_matrix('pasaje santa rosa 5040 buenos aires', 'Gascón 1099 buenos aires')
#print(gi)
getInfo = gmaps.geocode('pasaje santa rosa 5040 buenos aires') #Getting latitude and longitude from an address
getInfo2 = gmaps.geocode('Av Cordoba 3301 CABA') #Getting latitude and longitude from an address
LAT1 = getInfo[0]['geometry']['location']['lat']
LONG1 = getInfo[0]['geometry']['location']['lng']
LAT2 = getInfo2[0]['geometry']['location']['lat']
LONG2 = getInfo2[0]['geometry']['location']['lng']
#print(LAT1, LONG1, 'AND', LAT2, LONG2)
A = str('(') + str(LAT1) + str(',') + str(LONG1) + str(')')
B = str('(') + str(LAT2) + str(',') + str(LONG2) + str(')') '''

def routing():
    rowCounter = -1 #It must not count the header of the csv
    with open(os.path.join(os.path.dirname(__file__), 'routeSheet')) as routeSheet:
        routeSheet = csv.reader(routeSheet)
        for row in routeSheet:
            rowCounter += 1
    return rowCounter
    iRouting = 0 #Iterator Routing value
    iterationFormula = (rowCounter - 1) * rowCounter / 2
    #while iRouting <= iterationFormula:
    #    if iRouting == 0:

lineCounterVariable = -1
with open(os.path.join(os.path.dirname(__file__), 'latLngInfo09012018.csv')) as lineCounter:
    lineCounter = csv.reader(lineCounter)
    for row in lineCounter:
        lineCounterVariable += 1
print(lineCounterVariable)

counterForDelay = 0
clientsDone = 0
conditional = 0
listDistances = []
with open(os.path.join(os.path.dirname(__file__), 'latLngInfo09012018.csv')) as X:
    X = csv.reader(X)
    for i, linei in enumerate(X):
        with open(os.path.join(os.path.dirname(__file__), 'errorServerClientsBackUp.csv')) as errorServerConditional:
            errorServerConditional = csv.reader(errorServerConditional)
            for l in errorServerConditional:
                #print('This is l[0]:', type(l[0]))
                #print('This is i:', type(str(i)))
                if l[0] == str(i):
                    conditional = 1
        print('conditional', conditional)
        if conditional == 0:
            print('es i', i, linei)
            with open(os.path.join(os.path.dirname(__file__), 'latLngInfo09012018.csv')) as Y:
                Y = csv.reader(Y)
                for j, linej in enumerate(Y):
                    print('es j:', j, linej)
                    if counterForDelay == 40: #Trying to avoid to be getting out of the server
                        time.sleep(30)
                        counterForDelay = 0
                    try:
                        with open(os.path.join(os.path.dirname(__file__), 'distanceInfo09012018')) as headersFile:
                            pass
                    except FileNotFoundError:
                        with open(os.path.join(os.path.dirname(__file__), 'distanceInfo09012018'), 'a') as headersFile:
                            headersFile = csv.writer(headersFile, delimiter = ',')
                            headersFile.writerow(['conditional', 'id_AddressNumber_A', 'name_A', 'id_AddressNumber_B', 'name_B', 'distanceAB'])
                    if i < j and i != 0 and j != 0:
                        lookingForDistance = urlopen('http://router.project-osrm.org/trip/v1/driving/'+linei[5]+','+linei[4]+';'+linej[5]+','+linej[4]+'?source=first&destination=last')
                        infoFromOSRM = json.load(lookingForDistance)
                        distanceAB = infoFromOSRM['trips'][0]['legs'][0]['distance']
                        with open(os.path.join(os.path.dirname(__file__), 'distanceInfo10012018_AB'), 'a') as distanceInfo_AB: #It saves distance clients from A to B 
                            distanceInfo_AB = csv.writer(distanceInfo_AB, delimiter = ',')
                            distanceInfo_AB.writerow([str(linei[0]+'_'+linei[2]+linej[0]+'_'+linej[2]), str(linei[0]+'_'+linei[2]), linei[1], str(linej[0]+'_'+linej[2]), linej[1], str(distanceAB)])
                            print(str(linei[0]+'_'+linei[2]+linej[0]+'_'+linej[2]), str(linei[0]+'_'+linei[2]), linei[1], str(linej[0]+'_'+linej[2]), linej[1], str(distanceAB))
                        with open(os.path.join(os.path.dirname(__file__), 'distanceInfo10012018_BA'), 'a') as distanceInfo_BA: #It moves the order of the clients as B to A and we asume that the distance between them are the same than from A to B
                            distanceInfo_BA = csv.writer(distanceInfo_BA, delimiter = ',')
                            distanceInfo_BA.writerow([str(linej[0]+'_'+linej[2]+linei[0]+'_'+linei[2]), str(linej[0]+'_'+linej[2]), linej[1], str(linei[0]+'_'+linei[2]), linei[1], str(distanceAB)])
                            print(str(linej[0]+'_'+linej[2]+linei[0]+'_'+linei[2]), str(linej[0]+'_'+linej[2]), linej[1], str(linei[0]+'_'+linei[2]), linei[1], str(distanceAB))
                        clientsDone += 1
                        if clientsDone == (lineCounterVariable - i):
                            with open(os.path.join(os.path.dirname(__file__), 'errorServerClientsBackUp.csv'), 'a') as errorServer:
                                errorServer = csv.writer(errorServer, delimiter = ',')
                                errorServer.writerow([i, linei[0], linei[1]])
                    else:
                        pass
                    counterForDelay += 1
        else:
            pass
        conditional = 0
        j = 0

#print(len(listDistances))



                        #distance = math.sqrt(pow(float(linei[2]) - float(linej[2]), 2)+ pow(float(linei[3]) - float(linej[3]), 2))
                        #print('This i:', linei[0], '/ This j:', linej[0], 'Distance:', distance)
                        #print('This j:', linej[0], '/ This i:', linei[0], 'Distance:', distance)

    #First 6 and then 5 index from the csv in the response URL

    #response = urlopen('http://router.project-osrm.org/trip/v1/driving/-58.430085,-34.588136;-58.413186,-34.597955?source=first&destination=last')
    #a = json.load(response)
    #print(a['trips'][0]['legs'][0]['distance'])




#rC = routing()
#print(rC)
