import cv2
import numpy as np
from utils.hand_detection import HandDetection
from utils.Ball import Ball
from utils.Paddle import Paddle
from utils.collision import collision
from utils.constants import WIDTH, HEIGHT, ball_radius, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE, speed_increment

# Initialize video capture
vid = cv2.VideoCapture(0)
# Create an instance of HandDetection
hand_detection = HandDetection()
hand_detection.create_trackbars()



# Function to draw pieces in the main function
def draw_pieces(frame, paddle, ball, scoreCount, missCount):
    cv2.putText(frame, f"Score: {scoreCount}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Miss: {missCount}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    paddle.draw(frame)
    ball.draw(frame)

def main():
    paddle = Paddle(WIDTH//2, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
    ball = Ball(WIDTH//2, HEIGHT//2, ball_radius, 5, WHITE)
    # Initialise Score Variables
    scoreCount = 0
    missCount = 0
    while vid.isOpened():
        _, frame = vid.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        mask = hand_detection.create_mask(frame)
        threshImg = hand_detection.threshold(mask)
        mask_cleaned = hand_detection.clean_image(threshImg)
        contours = hand_detection.find_contours(mask_cleaned)
        frame = cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)
        max_cntr = hand_detection.max_contour(contours)
        (centroid_x, centroid_y) = hand_detection.centroid(max_cntr)
        frame = cv2.circle(frame, (centroid_x, centroid_y), 5, (255, 255, 0),
                           -1)
        paddle.move(frame, centroid_x)
        ball.move()
        draw_pieces(frame, paddle, ball, scoreCount, missCount)
        # handle collision function here
        collision(ball, paddle)
        # Implement Score Functionality
        if (ball.y > HEIGHT):
            missCount += 1
            if (missCount >= 3):
                scoreCount = 0
                missCount = 0
            ball.reset()
        if (
            ball.y + ball.radius >= paddle.y - paddle.height and
            ball.x + ball.radius >= paddle.x - paddle.width // 2 and
            ball.x - ball.radius <= paddle.x + paddle.width // 2
        ):
            scoreCount += 1

        cv2.imshow('Hand Gesture Slider', frame)

        key = cv2.waitKey(10)

        if key == ord('q'):
            break

    # Release the video capture and close all OpenCV windows
    vid.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
