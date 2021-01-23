import numpy as np
import cv2 as cv

img = cv.imread('/Users/300002291/Documents/facialRecognition/TrainImages/Test/SWAP10072000000001H024.jpg')
h, w, channels = img.shape 

left = int(0.492199779 * w)
top = int(0.306379706 * h )
bottom = int(top + 0.428335011 * h)
right = int(left + 0.175940529 * w)

img = cv.rectangle(img, (left,top), (right, bottom), (0,255,0), 4)

img = cv.resize(img, (780, 540),interpolation = cv.INTER_NEAREST)

cv.imshow('Draw01',img)
cv.waitKey(0)
