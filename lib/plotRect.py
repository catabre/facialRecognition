import numpy as np
import cv2 as cv
import sys
import csv

with open('resultSet.csv') as csv_file:         ### Ensure the file name is same or change the name here. 
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    lineToPlot = int(sys.argv[1]) 
    for row in csv_reader:
        line_count += 1 
        if line_count == lineToPlot:
            le = float(row[5])
            to = float(row[6])
            he = float(row[7])
            wi = float(row[8])
            print(row[5], row[6], row[7], row[8])
            imagePath = '/Users/300002291/Documents/facialRecognition/'
            imagePath = imagePath + row[3]
            personName = row[4]

img = cv.imread(imagePath)
h, w, channels = img.shape 

left = int(le * w)
top = int(to * h )
bottom = int(top + he * h)
right = int(left + wi * w)

img = cv.rectangle(img, (left,top), (right, bottom), (0,255,0), 4)
cv.putText(img, personName , (left,top-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 4)

img = cv.resize(img, (int(w*0.50), int(h*0.50)),interpolation = cv.INTER_NEAREST)

cv.imshow('Draw01',img)
cv.waitKey(0)
