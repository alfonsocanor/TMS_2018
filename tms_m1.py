import csv
import os
import geocoder
import googlemaps

'''Read the csv and deploying uselful information'''

key = 'AIzaSyBMwXuzxKO2EY2eoNX163Iojydhmi39i1U' #googleMaps API key - Userd in class GoogleMapsInfo

class FileCheck():
    def __init__(self, fileName):
        self.fileName = fileName
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            pass

    def orderField(self):
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X:
            X = X.readline()
            X = X.replace('\n', '')
            X = X.split(',')
            for column in X:
                if column == 'client_id':
                    self.client_id = X.index(column)
                elif column == 'client':
                    self.client = X.index(column)
                elif column == 'addressNumber':
                    self.addressNumber = X.index(column)
                elif column == 'address':
                    self.address = X.index(column)
            return self.client_id, self.client, self.addressNumber, self.address #This returns a tupla

class GoogleMapsInfo(FileCheck):
    def __init__(self, fileName):
        super().__init__(fileName)

    def latLongInfo(self):
        self.fields = FileCheck(self.fileName)
        self.addressLatLng = self.fields.orderField()

        aux0 = self.addressLatLng[0] #client_id Comes from the tupla orderFields from class FileCheck
        aux1 = self.addressLatLng[1] #client Comes from the tupla orderFields from class FileCheck
        aux2 = self.addressLatLng[2] #addressNumber Comes from the tupla orderFields from class FileCheck
        aux3 = self.addressLatLng[3] #address Comes from the tupla orderFields from class FileCheck

        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as X: #X Random named
            X = csv.reader(X)
            for row in X:
                print(row)
                gmaps = googlemaps.Client(key='AIzaSyBMwXuzxKO2EY2eoNX163Iojydhmi39i1U') #From googlaMaps API
                getInfo = gmaps.geocode(row[aux3]) #Getting latitude and longitude from an address
                if getInfo == []:
                    pass
                else:
                    lat = getInfo[0]['geometry']['location']['lat']
                    lng = getInfo[0]['geometry']['location']['lng']
                with open(os.path.join(os.path.dirname(__file__), 'latLngInfo08012018.txt'), 'a') as Y:
                    if row[aux0] == 'client_id':
                        Y = csv.writer(Y, delimiter=',')
                        Y.writerow([str(row[aux0]), str(row[aux1]), str(row[aux2]), str(row[aux3]), 'Latitude', 'Longitude'])
                    else:
                        Y = csv.writer(Y, delimiter=',')
                        Y.writerow([str(row[aux0]), str(row[aux1]), str(row[aux2]), str(row[aux3]), str(lat), str(lng)])

class Osmr_Api():
    pass


X = GoogleMapsInfo('zetamixClientAddresses.txt')
X.latLongInfo()
