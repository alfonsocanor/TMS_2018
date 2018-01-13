import os
import csv
i = 0
with open(os.path.join(os.path.dirname(__file__), 'latLngInfo10012018.csv')) as Y:
    Y = csv.reader(Y)
    for row in Y:
        with open(os.path.join(os.path.dirname(__file__), 'latLngInfo10012018_1.csv'), 'a') as X:
            X = csv.writer(X, delimiter = ',')
            X.writerow([str(i), row[0], row[1], row[2], row[3], row[4]])
        i += 1

    