import cv2

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
 
t = 0
while t < 500:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (100, 100), cv2.INTER_LINEAR)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        if t % 10 == 0:
            cv2.imwrite(str(t) + ".png",roi_gray)

    t += 1
     
    cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()
