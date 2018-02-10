from flask import Flask, render_template, request
import os
import csv
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'ThisIsSecret'
sort_keys = False

class Reference():
    def testList(self):
        testList = ['A', 'B', 'C', 'D', 'E']
        return testList

@app.route('/home', methods=['GET', 'POST'])
def home():
    test1 = Reference()
    test = test1.testList()
    print('helooooooo', test1.testList())
    selected_contacts1 = ['pointA', 'pointB']
    with open(os.path.join(os.path.dirname(__file__), 'fileTest')) as checkFile:
        checkFile = csv.reader(checkFile)
        counter = 0
        for i in checkFile:
            counter += 1
    if counter == 1:
        with open(os.path.join(os.path.dirname(__file__), 'fileTest')) as gettingPointA:
            gettingPointA = csv.reader(gettingPointA)
            selected_contacts1 = []
            for row in gettingPointA:
                selected_contacts1.append(row)
            selected_contacts1.append('PointB')
    else:
        with open(os.path.join(os.path.dirname(__file__), 'fileTest')) as gettingPoints:
            gettingPoints = csv.reader(gettingPoints)
            for i, line in enumerate(gettingPoints):
                if i == (counter - 2):
                    selected_contacts1[0] = line[0]
                if i == (counter - 1):
                    selected_contacts1[1] = line[0]
    
    if request.method == "POST":

        if counter == 0:
            selected_contactsA = request.form.getlist('test')
            with open(os.path.join(os.path.dirname(__file__), 'conditionalFile'), 'w') as conditionalFile:  
                conditionalFile = csv.writer(conditionalFile)
                conditionalFile.writerow(selected_contactsA)          
            print('WHEN COUNTER IS 0:', selected_contactsA)
            with open(os.path.join(os.path.dirname(__file__), 'fileTest'), 'a') as pointA:
                pointA = csv.writer(pointA)
                pointA.writerow(selected_contactsA)
        else:
            selected_contactsB = request.form.getlist("test")
            print('WHEN COUNTER IS 1 BEFORE REMOVE:', selected_contactsB)
            with open(os.path.join(os.path.dirname(__file__), 'conditionalFile')) as readingConditionalFile:
                readingConditionalFile = csv.reader(readingConditionalFile)
                for row in readingConditionalFile:
                    print('FILE ROW', row)
                    for i in row:
                        print('ITEM IN ROW', i)
            with open(os.path.join(os.path.dirname(__file__), 'conditionalFile')) as readingConditionalFile:
                readingConditionalFile = csv.reader(readingConditionalFile)
                for row in readingConditionalFile:
                    for i in row:
                        try:
                            selected_contactsB.remove(i)
                        except ValueError:
                            pass
            print('WHEN COUNTER IS 1 AFTER REMOVE:', selected_contactsB)
            with open(os.path.join(os.path.dirname(__file__), 'conditionalFile'), 'w') as conditionalFile:  
                conditionalFile = csv.writer(conditionalFile)
                conditionalFile.writerow(selected_contactsB)   
            X = selected_contactsB[0]
            print(X)
            with open(os.path.join(os.path.dirname(__file__), 'fileTest'), 'a') as pointB:
                pointB = csv.writer(pointB)
                pointB.writerow([X])

        with open(os.path.join(os.path.dirname(__file__), 'fileTest')) as checkFile:
            checkFile = csv.reader(checkFile)
            counter1 = 0
            for i in checkFile:
                counter1 += 1

        if counter1 == 1:
            with open(os.path.join(os.path.dirname(__file__), 'fileTest')) as gettingPoints:
                gettingPoints = csv.reader(gettingPoints)
                selected_contacts1 = []
                for row in gettingPoints:
                    print('ROOOOWWWW', row)
                    selected_contacts1.append(row[0])
                selected_contacts1.append('conditional')
        else:
            with open(os.path.join(os.path.dirname(__file__), 'fileTest')) as gettingPoints:
                gettingPoints = csv.reader(gettingPoints)
                selected_contacts1 = ['pointA', 'pointB']
                for i, line in enumerate(gettingPoints):
                    if i == (counter1 - 2):
                        selected_contacts1[0] = line[0]
                    if i == (counter1 - 1):
                        selected_contacts1[1] = line[0]
        print('HTML INFORMATION LIST', selected_contacts1)
        return render_template('checkBoxTest.html', test=test, selected_contacts1=selected_contacts1)
    return render_template('checkBoxTest.html', test=test, selected_contacts1=selected_contacts1)

if __name__ == '__main__':
    app.run(debug=True)