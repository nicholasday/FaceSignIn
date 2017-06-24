import glob
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

images = []

#for path in glob.glob("./*.png"):
for path in glob.glob("/home/nicholas/downloads/faces94/*.jpg"):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#
#    roi_gray = 0
#    for (x,y,w,h) in faces:
#        roi_gray = gray[y:y+h, x:x+w]
#        roi_color = frame[y:y+h, x:x+w]
#        roi_gray = cv2.resize(roi_gray, (100, 100), cv2.INTER_LINEAR)

    roi_gray = cv2.resize(gray, (50, 50), cv2.INTER_LINEAR)

    images.append(roi_gray.flatten())

images = np.array(images)

average = np.mean(images, axis=0)

cv2.imwrite('average.png', average.reshape((50, 50)))

average = cv2.imread('average.png', cv2.IMREAD_GRAYSCALE)
average = average.flatten()

diff_images = []

for column in images:
    column = cv2.subtract(column, average)
    diff_images.append(column.flatten())

diff_images = np.array(diff_images)

R = np.cov(diff_images.T)

w, v = np.linalg.eigh(R)

with open('w.pickle', 'wb') as f:
    np.save(f, w)

with open('v.pickle', 'wb') as g:
    np.save(g, v)
