import csv
import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from time import strftime

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ThisissecretIFTS18'


class Route():
    def __init__(self, routeSheetFileName, distancesFileName): #1.Route sheet 2.Distances matrix 3.File Routed due Disjkstra's Algorithm
        self.routeSheetFileName = routeSheetFileName
        self.distancesFileName =  distancesFileName
        self.time = strftime("%Y%m%d_%H%M%S")
        self.routedFileName = 'Route_'+self.time

    def routing1(self):
        self.distancesRouteDict = {}
        self.distancesRouteList = []
        self.minDistance = 0
        self.startPoint = '0001_1' #Start point
        self.counterLine = 0
        self.routes = 0
        with open(os.path.join(os.path.dirname(__file__), self.routeSheetFileName )) as routeSheetFile:
            routeSheetFile = csv.reader(routeSheetFile)
            for row in routeSheetFile:
                self.counterLine += 1
        while self.routes < self.counterLine:
            print(self.routes, self.counterLine)
            with open(os.path.join(os.path.dirname(__file__), self.routeSheetFileName)) as routeSheetFile:
                routeSheetFile = csv.reader(routeSheetFile)
                for row_i in routeSheetFile:
                    id_Concatenate = self.startPoint + row_i[1]
                    with open(os.path.join(os.path.dirname(__file__), self.distancesFileName)) as compareDistances:
                        compareDistances = csv.reader(compareDistances)
                        for row_j in compareDistances:
                            #print(row_j[1], 'and', id_Concatenate)
                            if (id_Concatenate == row_j[1]) and (row_j[4] not in self.distancesRouteList):
                                #print('THE DICT VALUE TO ADD IS:', row_j)
                                self.distancesRouteDict[row_j[4]] = float(row_j[6]) #It could be read: Client_id (row_j[4]) is far X meters (row_j[6]) from start point It's storaged in Dictionary (distancesRouteDict)
                if self.distancesRouteDict == {}:
                    pass
                else:
                    self.minDistance = min(self.distancesRouteDict, key=lambda k: self.distancesRouteDict[k]) #Formula found on internet for getting the min value in a dict
                self.distancesRouteList.append(self.minDistance)
            with open(os.path.join(os.path.dirname(__file__), self.distancesFileName)) as lookingUpClientInfo:
                lookingUpClientInfo = csv.reader(lookingUpClientInfo)
                for row_k in lookingUpClientInfo:
                    if row_k[1] == self.startPoint + self.minDistance:
                        with open(os.path.join(os.path.dirname(__file__), self.routedFileName), 'a') as routeFile:
                            routeFile = csv.writer(routeFile, delimiter=',')
                            routeFile.writerow([self.startPoint+row_k[4], row_k[5], row_k[6]])
            self.startPoint = self.minDistance  
            self.distancesRouteDict = {}
            self.routes += 1

    '''def routing():
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
            routes += 1'''

X = Route('routeSheet_12012018', 'totalDistances_AB_BA_12012018.csv')
X.routing1()

@app.route('/routing', methods=['GET', 'POST'])
def routing():
    return render_template('routing.html')

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/routing', methods=['GET', 'POST'])
def upload():
    target = os.path.join(APP_ROOT)
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    
    for file in request.files.getlist("file"):
        print(dir(file))
        filename = file.filename
        print(filename)
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template('complete.html')

if __name__=='__main__':
    app.run(debug=False)