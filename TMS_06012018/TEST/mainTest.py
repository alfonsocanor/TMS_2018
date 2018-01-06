#This is an attemp to understand how could I read and write csv
import os
import csv
import math

with open(os.path.join(os.path.dirname(__file__), 'matrixCalculation.csv')) as X:
    X = csv.reader(X)
    for i, linei in enumerate(X):
        with open(os.path.join(os.path.dirname(__file__), 'matrixCalculation.csv')) as Y:
            Y = csv.reader(Y)
            for j, linej in enumerate(Y):
                if i <= j:
                    pass
                else:
                    distance = math.sqrt(pow(float(linei[2]) - float(linej[2]), 2)+ pow(float(linei[3]) - float(linej[3]), 2))
                    print('This i:', linei[0], '/ This j:', linej[0], 'Distance:', distance)
                    print('This j:', linej[0], '/ This i:', linei[0], 'Distance:', distance)
