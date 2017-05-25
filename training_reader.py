import numpy as np
import cv2

with open('w.pickle', 'rb') as f:
    w = np.load(f)

with open('v.pickle', 'rb') as f:
    v = np.load(f)

for b, i in enumerate(reversed(v.T)):
    i.shape = (50, 50)
    i = i/(i.max()/255.0)
    cv2.imshow('test', i)
    cv2.imwrite("eigenresults/" + str(b) + ".png", i)
    cv2.waitKey(1000)
