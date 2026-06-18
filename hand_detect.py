import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1,
					  min_detection_confidence=0.5,
					  min_tracking_confidence=0.5)

mpDraw = mp.solutions.drawing_utils

while True:
	success, img = cap.read()

	if not success:
		break
	img = cv2.flip(img, 1)

	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	results = hands.process(imgRGB)
	print(results)

	if results.multi_hand_landmarks:
		for handLms in results.multi_hand_landmarks:
			mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
	cv2.imshow("Hand Tracking", img)
	if cv2.waitKey(1) & 0xFF == 27:
		break
	

