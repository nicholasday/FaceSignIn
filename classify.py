import cv2
import numpy as np
import sys

with open('v.pickle', 'rb') as f:
    v = np.load(f)

average = cv2.imread('average.png', cv2.IMREAD_GRAYSCALE)

test = cv2.imread('10.png')

gray = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in faces:
    roi_gray = gray[y:y+h, x:x+w]
    gray = cv2.resize(roi_gray, (100, 100), cv2.INTER_LINEAR)

gray = cv2.resize(gray, (50, 50), cv2.INTER_LINEAR)

cv2.imwrite("gray.png", gray)

#diff = cv2.subtract(gray, average)
diff = gray - average

diff_vec = diff.flatten()

ratios = np.dot(diff_vec, v)

try:
    with open('ratios.pickle', 'rb') as f:
        saved = np.load(f)
        new = np.column_stack((saved, ratios))
    with open('ratios.pickle', 'wb') as f:
        print(new.shape)
        np.save(f, new)
except IOError:
    with open('ratios.pickle', 'wb') as f:
        np.save(f, ratios)

reconstructed = np.dot(v, ratios)

reconstructed = reconstructed.astype(np.uint8).reshape((50, 50)) + average

cv2.imwrite("reconstruct.png", reconstructed)
