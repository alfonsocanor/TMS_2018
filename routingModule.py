import csv
import os
from flask import Flask, request, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField
from time import strftime

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ThisissecretIFTS18'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Reference(FlaskForm):
    submit = BooleanField()

class Route():
    def __init__(self, routeSheetFileName): #1.Route sheet 2.Distances matrix 3.File Routed due Disjkstra's Algorithm
        self.routeSheetFileName = routeSheetFileName
        self.time = strftime("%Y%m%d_%H%M%S")
        self.routedFileName = 'Route_'+self.time

#   def startPoint(self, starPoint):
#       starPoint =

    def showRouteSheet(self):
        self.clientsRouteList = [['1', '0001_1', 'ZETAMIX']]
        with open(os.path.join(os.path.dirname(__file__), self.routeSheetFileName)) as clientsRouteFile:
            clientsRouteFile = csv.reader(clientsRouteFile)
            for row in clientsRouteFile:
                self.clientsRouteList.append(row)

        #This with open('w') is used to save the name of the program the user charge through HTML
        #in a file with a default name that later is used for "routingOperation" method in this same class Route
        with open(os.path.join(os.path.dirname(__file__), 'startPointFileConditional.csv'), 'w') as startPointFileConditional:
            startPointFileConditional = csv.writer(startPointFileConditional)
            startPointFileConditional.writerow([self.routeSheetFileName]) 

        return self.clientsRouteList

    def routingOperation(self, startPoint, distancesFileName):
        self.startPoint = startPoint
        self.distancesFileName =  distancesFileName
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
                    print(row_k)
                    if row_k[1] == self.startPoint + self.minDistance:
                        with open(os.path.join(os.path.dirname(__file__), self.routedFileName), 'a') as routeFile:
                            routeFile = csv.writer(routeFile, delimiter=',')
                            routeFile.writerow([self.startPoint+row_k[4], row_k[5], row_k[6], row_k[4]])
            self.startPoint = self.minDistance  
            self.distancesRouteDict = {}
            self.routes += 1
        routingList = []
        with open(os.path.join(os.path.dirname(__file__), self.routedFileName)) as routing_HTML_Table:
            routing_HTML_Table = csv.reader(routing_HTML_Table)
            for row in routing_HTML_Table:
                routingList.append(row)
        return routingList


@app.route('/routed')
def routed():
    return 'submit'


@app.route('/routing', methods=['GET', 'POST'])
def routing():
    submit = Reference()
    if request.method == 'POST':
        directory = os.path.join(APP_ROOT)
        ifDisplayHTMLConditional = False
        if not os.path.isdir(directory):
            os.mkdir(directory)
        for file in request.files.getlist("file"):
            filename = file.filename
            destination = "/".join([directory, filename])
            if file.filename != '':
                file.save(destination)
                clientsInRouteSheet = Route(filename)
                showClientsInRouteSheet = clientsInRouteSheet.showRouteSheet()
                ifDisplayHTMLConditional = True
        if submit.validate_on_submit():

        ####Start

            #This is code is used to transform the return of the request.form.getlist("showClientsInRouteSheet")
            #from the template routing.html => ["['12', '1499_3', 'ROMERO CARLOS ENRIQUE']"]
            #into a value that the class routing can take in its contructor attribute "startPoint""
            startPointConditional = request.form.getlist("showClientsInRouteSheet")
            startPointList = []
            fixingStartPoint = startPointConditional[0].replace(' ','')
            aux_1 = '' #aux_1 variable is used to handle method replace to modifide the string as the class need
            for i in fixingStartPoint:
                aux_1 = aux_1 + i
            aux_1 = aux_1.replace('[', '')
            aux_1 = aux_1.replace(']', '')
            aux_2 = '' #aux_2 variable is used in the conditional to create the list for getting the value of the ID client
            for i in aux_1:
                if i != ',':
                    aux_2 = aux_2 + i
                else:
                    startPointList.append(aux_2)
            startPoint = startPointList[1].replace("'", '')

        ####Finish

            #looking for the name of the routeSheet

            with open(os.path.join(os.path.dirname(__file__), 'startPointFileConditional.csv')) as fileNameRequest:
                fileNameRequest = csv.reader(fileNameRequest)
                for i in fileNameRequest:
                    routeSheetFileName = i[0]

            #DO TO: Friday 02/02/2018

            routing = Route(routeSheetFileName)
            routingPost = routing.routingOperation(startPoint, 'totalDistances_AB_BA_12012018.csv' )                  

            return render_template('routed.html', routingPost=routingPost)
        return render_template('routing.html', submit=submit, showClientsInRouteSheet=showClientsInRouteSheet, ifDisplayHTMLConditional=ifDisplayHTMLConditional)
    return render_template('routing.html')

if __name__=='__main__':
    app.run(debug=True)