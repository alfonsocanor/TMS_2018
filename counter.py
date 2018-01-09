import os
import csv
counter = -1
counterY = -1
with open(os.path.join(os.path.dirname(__file__), 'distanceInfo08012018')) as Y:
    Y = csv.reader(Y)
    for row in Y:
        counterY += 1
print(counterY)
with open(os.path.join(os.path.dirname(__file__), 'latLngInfo08012018 copy.csv')) as X:
    X = csv.reader(X)
    for row in X:
        if row[0] != '1844':
            counter+=1
            print(counter)
        else:  
            exit()

 
        