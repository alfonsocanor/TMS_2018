import googlemaps
import geocoder
from geopy.distance import vincenty
from urllib.request import urlopen
import json

gmaps = googlemaps.Client(key='AIzaSyBMwXuzxKO2EY2eoNX163Iojydhmi39i1U') #From googlaMaps API
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
B = str('(') + str(LAT2) + str(',') + str(LONG2) + str(')')
#INFO = osrm.simple_route([LAT1, LONG1],[LAT2, LONG2], output='route', overview="full", geometry='wkt')
INFO = vincenty(A, B).kilometers
#print(INFO)

response = urlopen('http://router.project-osrm.org/trip/v1/driving/-58.430085,-34.588136;-58.413186,-34.597955?source=first&destination=last')
a = json.load(response)
#print(a)
print(a['trips'][0]['legs'][0]['distance'])