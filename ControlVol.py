import cv2
import mediapipe as mp
import pyautogui
import time
pTime = 0
capture_hand = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

camera = cv2.VideoCapture(0)
x1 = y1 = x2 = y2 = 0
while True:
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    _,image = camera.read()
    image_height, image_width, _ = image.shape
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.putText(image, f'FPS: {int(fps)}', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    output_hands = capture_hand.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int (lm.x * image_width)
                y = int (lm.y * image_height)
                print(x, y)
                if id == 8:
                    mouse_x = (screen_width / image_width * x)
                    mouse_y = (screen_height / image_height * y)
                    cv2.circle(image, (x, y), 10, (0, 255, 0))
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1 = x
                    y1 = y
                if id == 4:
                    x2 = x
                    y2 = y
                    cv2.circle(image, (x, y), 10, (0, 255, 0))
        dist = y2 - y1
        print(dist)
        if(dist<25):
            pyautogui.click()
            print("Clicked")

    cv2.imshow("Hand movement video capture", image)
    key = cv2.waitKey(1)
    if key == 27:
        break
camera.release()
cv2.destroyAllWindows()
