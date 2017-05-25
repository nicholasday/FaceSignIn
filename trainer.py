import glob
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

images = []

for path in glob.glob("./*.png"):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    roi_gray = 0
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (100, 100), cv2.INTER_LINEAR)

    images.append(roi_gray.flatten())

average = np.average(images, axis=0)

cv2.imwrite('average.png', average.reshape((50, 50)))

map(lambda x: x - average, images)

R = np.cov(images.T)

w, v = np.linalg.eigh(R)

with open('w.pickle', 'wb') as f:
    np.save(f, w)

with open('v.pickle', 'wb') as g:
    np.save(g, v)
