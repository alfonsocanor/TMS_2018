import csv
import os
import geocoder
import googlemaps

'''Read the csv and deploying uselful information'''

key = 'AIzaSyBMwXuzxKO2EY2eoNX163Iojydhmi39i1U' #googleMaps API key - Userd in class GoogleMapsInfo

class FileCheck():
    def __init__(self, fileName):
        self.fileName = fileName

    def orderField(self):
        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as mainFileInformation:
            mainFileInformation = mainFileInformation.readline()
            mainFileInformation = mainFileInformation.replace('\n', '')
            mainFileInformation = mainFileInformation.split(',')
            for column in mainFileInformation:
                if column == 'client_id':
                    self.client_id = mainFileInformation.index(column)
                elif column == 'client':
                    self.client = mainFileInformation.index(column)
                elif column == 'addressNumber':
                    self.addressNumber = mainFileInformation.index(column)
                elif column == 'address':
                    self.address = mainFileInformation.index(column)
            return self.client_id, self.client, self.addressNumber, self.address #This returns a tupla

class GoogleMapsInfo(FileCheck):
    def __init__(self, fileName):
        super().__init__(fileName)

    def latLongInfo(self):
        self.fields = FileCheck(self.fileName)
        self.addressLatLng = self.fields.orderField()

        client_id = self.addressLatLng[0] #client_id Comes from the tupla orderFields from class FileCheck
        client = self.addressLatLng[1] #client Comes from the tupla orderFields from class FileCheck
        addressNumber = self.addressLatLng[2] #addressNumber Comes from the tupla orderFields from class FileCheck
        address = self.addressLatLng[3] #address Comes from the tupla orderFields from class FileCheck

        with open(os.path.join(os.path.dirname(__file__), self.fileName)) as mainFileInformation: #X Random named
            mainFileInformation = csv.reader(mainFileInformation)
            for row in mainFileInformation:
                print(row)
                gmaps = googlemaps.Client(key='AIzaSyBMwXuzxKO2EY2eoNX163Iojydhmi39i1U') #From googlaMaps API
                getInfo = gmaps.geocode(row[address]) #Getting latitude and longitude from an address
                if getInfo == []:
                    pass
                else:
                    lat = getInfo[0]['geometry']['location']['lat']
                    lng = getInfo[0]['geometry']['location']['lng']
                with open(os.path.join(os.path.dirname(__file__), 'latLngInfo08012018.txt'), 'a') as outputFileLatLng:
                    if row[client_id] == 'client_id':
                        outputFileLatLng = csv.writer(outputFileLatLng, delimiter=',')
                        outputFileLatLng.writerow([str(row[client_id]), str(row[client]), str(row[addressNumber]), str(row[address]), 'Latitude', 'Longitude'])
                    else:
                        outputFileLatLng = csv.writer(outputFileLatLng, delimiter=',')
                        outputFileLatLng.writerow([str(row[client_id]), str(row[client]), str(row[addressNumber]), str(row[address]), str(lat), str(lng)])


X = GoogleMapsInfo('zetamixClientAddresses.txt')
X.latLongInfo()
