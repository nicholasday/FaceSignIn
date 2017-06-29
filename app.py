import cv2
import math
import time

cap = cv2.VideoCapture(0)

cv2.namedWindow("App")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 
current_click = [0, 0]

def click_listener(event, x, y, flags, param):
    global current_click

    if event == cv2.EVENT_LBUTTONUP:
        current_click = [x, y]

cv2.setMouseCallback("App", click_listener)

running = True

class State:
    initialized = False

    def init(self):
        self.initialized = True

    def stop(self):
        self.initialized = False

    def loop(self, frame):
        print("loop")

    def isFinished(self):
        print("isFinished")
        return False

class Button():
    def __init__(self, x, y, width, height, text, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action

    def draw(self, frame):
        rect(self.x, self.y, self.width, self.height, frame)
        text(self.text, self.x + 10, self.y + 10, 1, frame)

    def clicked(self, x, y):
        return x < self.x + self.width and x > self.x and y < self.y + self.height and y > self.y

class Main(State):
    buttons = []
    button_id = 0

    def loop(self, frame):
        text(str(current_click), 100, 100, 10, frame)
        for button in self.buttons:
            button.draw(frame)

    def isFinished(self):
        for i, button in enumerate(self.buttons):
            if button.clicked(current_click[0], current_click[1]):
                self.button_id = i 
                return True
        return False

    def init(self):
        super().init()
        current_click[0] = 0
        current_click[1] = 0
        self.button_id = 0
        self.buttons = []
        self.buttons.append(Button(10, 10, 100, 100, "click", TakePics(1)))
        self.buttons.append(Button(200, 200, 100, 100, "click2", TakePics(2)))

    def stop(self):
        super().stop()

    def next(self):
        return self.buttons[self.button_id].action


class TakePics(State):
    def __init__(self, pics_left):
        self.pics_left = pics_left
        self.time_length = 5

    def init(self):
        self.start_time = time.time()
        super().init()

    def loop(self, frame):
        time_elapsed = time.time() - self.start_time

        if time_elapsed >= self.time_length:
            cv2.imwrite(str(self.pics_left) + ".png", frame)
            self.pics_left = self.pics_left - 1
            self.start_time = time.time()

        text(str(self.pics_left), frame.shape[1] - 100, 50, 1, frame)

        top_left_x = math.floor(frame.shape[1]/2 - 200)
        top_left_y = frame.shape[0] - 100
        percentage_bar_length = 500
        rect(top_left_x, top_left_y, percentage_bar_length, 70, frame)

        percentage = math.floor(time_elapsed/self.time_length * percentage_bar_length)
        filled_rect(top_left_x, top_left_y, percentage, 70, frame)

    def isFinished(self):
        return self.pics_left == 0

    def next(self):
        return Main()

def text(text, x, y, size, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (x, y), font, 2, (255,255,255), 2, cv2.LINE_AA)

def rect(x, y, width, height, frame):
    cv2.rectangle(frame, (x, y), (x + width, y + height), (0,255,0), 3)

def filled_rect(x, y, width, height, frame):
    cv2.rectangle(frame, (x, y), (x + width, y + height), (0,255,0), -1)

current = Main()

while running:
    ret, frame = cap.read()

    if current.initialized is False:
        current.init()

    if current.isFinished() is False:
        current.loop(frame)
    else:
        current.stop()
        current = current.next()

    cv2.imshow('App', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
