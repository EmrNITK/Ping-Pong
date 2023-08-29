import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Video capture
cap = cv2.VideoCapture(0)

# Initialize slider variables
slider_x = 100
slider_y = 100
slider_width = 20
slider_height = 150
slider_color = (0, 255, 0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    

    cv2.rectangle(frame, (slider_x, slider_y), (slider_x + slider_width, slider_y + slider_height), slider_color, -1)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            hand_y = int(landmarks.landmark[8].y * frame.shape[0])
            slider_y = hand_y - slider_height // 2

    cv2.imshow('Hand Gesture Slider', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
