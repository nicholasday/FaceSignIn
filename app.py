import cv2
import math
import time

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 
time_length = 5
start_time = time.time()
pics_left = 10
while pics_left > 0:
    ret, frame = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time_elapsed = time.time() - start_time

    if time_elapsed >= time_length:
        cv2.imwrite(str(pics_left) + ".png", frame)
        pics_left = pics_left - 1
        start_time = time.time()

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(pics_left), (frame.shape[1] - 100,50), font, 2, (255,255,255), 2, cv2.LINE_AA)

    top_left_x = math.floor(frame.shape[1]/2 - 200)
    top_left_y = frame.shape[0] - 100
    percentage_bar_length = 500
    cv2.rectangle(frame, (top_left_x, top_left_y), (top_left_x +
        percentage_bar_length, top_left_y + 70), (0,255,0), 3)
    percentage = math.floor(time_elapsed/time_length * percentage_bar_length)
    cv2.rectangle(frame, (top_left_x, top_left_y), (top_left_x + percentage, top_left_y + 70), (0,255,0), -1)
     
    cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()
