import cv2
import pyautogui
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

wScr, hScr = pyautogui.size()
frameR = 100 
hCam, wCam = 480, 640

plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 7
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        x, y, _ = lmList[8]
        x1, y1, _ = lmList[4]
        x2, y2, _ = lmList[8]
        length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        if length < 30:
            pyautogui.click()
            time.sleep(0.3)
        x3 = np.interp(x, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y, (frameR, hCam - frameR), (0, hScr))
        dx = x3 - plocX
        dy = y3 - plocY
        if abs(dx) < 8 and abs(dy) < 8:
            pass
        else:
            clocX = plocX + (x3 - plocX)
            clocY = plocY + (y3 - plocY)
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY
    cv2.imshow("Image", img)
    cv2.waitKey(1)	