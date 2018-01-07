import googlemaps
import geocoder
from geopy.distance import vincenty
from urllib.request import urlopen
import json
import os
import csv
import math

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
listDistances = []
with open(os.path.join(os.path.dirname(__file__), 'latLngInfocopy.csv')) as X:
    X = csv.reader(X)
    for i, linei in enumerate(X):
        print(i)
        with open(os.path.join(os.path.dirname(__file__), 'latLngInfocopy.csv')) as Y:
            Y = csv.reader(Y)
            for j, linej in enumerate(Y):
                print(j)
                try:
                    with open(os.path.join(os.path.dirname(__file__), 'distanceInfo')) as headersFile:
                        pass
                except FileNotFoundError:
                    with open(os.path.join(os.path.dirname(__file__), 'distanceInfo'), 'a') as headersFile:
                        headersFile = csv.writer(headersFile, delimiter = ',')
                        headersFile.writerow(['id_AddressNumber_A', 'name_A', 'id_AddressNumber_B', 'name_B', 'distanceAB'])
                if i <= j or linei[0]=='client_id' or linej[0]=='client_id':
                    pass
                else:
                    lookingForDistance = urlopen('http://router.project-osrm.org/trip/v1/driving/'+linei[5]+','+linei[4]+';'+linej[5]+','+linej[4]+'?source=first&destination=last')
                    infoFromOSRM = json.load(lookingForDistance)
                    distanceAB = infoFromOSRM['trips'][0]['legs'][0]['distance']
                    with open(os.path.join(os.path.dirname(__file__), 'distanceInfo'), 'a') as distanceInfo:
                        distanceInfo = csv.writer(distanceInfo, delimiter = ',')
                        distanceInfo.writerow([str(linei[0]+'_'+linei[2]), linei[1], str(linej[0]+'_'+linej[2]), linej[1], str(distanceAB)])
                        #print(linei[5],linei[4],linej[5],linei[4])
                        #info = 'From:',linei[0],linei[1],'to:',linej[0],linej[1],'The distance is:',distanceAB
                        #print('From:',linei[0],linei[1],'to:',linej[0],linej[1],'The distance is:',distanceAB)
                        #listDistances.append(info)

#print(len(listDistances))



                    #distance = math.sqrt(pow(float(linei[2]) - float(linej[2]), 2)+ pow(float(linei[3]) - float(linej[3]), 2))
                    #print('This i:', linei[0], '/ This j:', linej[0], 'Distance:', distance)
                    #print('This j:', linej[0], '/ This i:', linei[0], 'Distance:', distance)

#First 6 and then 5 index from the csv in the response URL

#response = urlopen('http://router.project-osrm.org/trip/v1/driving/-58.430085,-34.588136;-58.413186,-34.597955?source=first&destination=last')
#a = json.load(response)
#print(a['trips'][0]['legs'][0]['distance'])
