import cv2
import numpy as np

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
average = cv2.imread('average.png', cv2.IMREAD_GRAYSCALE)

with open('ratios.pickle', 'rb') as f:
    ratios = np.load(f)

with open('v.pickle', 'rb') as f:
    v = np.load(f)
 
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (50, 50), cv2.INTER_LINEAR)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

    
    diff = roi_gray - average

    diff_vec = diff.flatten()

    new_ratios = np.dot(diff_vec, v)

    results = []

    for i, column in enumerate(ratios.T):
        ratio_diff = new_ratios - column
        mag = np.linalg.norm(ratio_diff)
        print(i)
        results.append(mag)

    name = results.index(min(results))

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(name), (frame.shape[1] - 100,50), font, 2, (255,255,255), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()
