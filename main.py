import cv2
import numpy as np
from hand_detection import HandDetection

# Initialize video capture
vid = cv2.VideoCapture(0)

# Create an instance of HandDetection
hand_detection = HandDetection()
hand_detection.create_trackbars()

# Initialize slider variables
WIDTH, HEIGHT = 700, 500
ball_radius = 15
# Decrease the height for a horizontal slider
PADDLE_WIDTH, PADDLE_HEIGHT = 150, 20
WHITE = (255, 255, 255)
slider_color = (0, 255, 0)


class Paddle:
    COLOR = WHITE
    VEL = 10

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, frame):
        cv2.rectangle(
            frame,
            (int(self.x - self.width // 2), int(HEIGHT - self.height)),
            (int(self.x + self.width // 2), int(HEIGHT)),
            (255, 255, 255),
            -1,
        )

    def move(self, frame, centroid_x):
        self.x = centroid_x

    # Ensure the paddle stays within the frame boundaries
        if self.x - self.width//2 < 0:
            self.x = self.width//2
        if self.x + self.width//2 > WIDTH:
            self.x = WIDTH - self.width//2
        self.draw(frame)

    def reset(self):
        self.x = self. original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 5
    ball_color = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = 3
        self.y_vel = -3

    def draw(self, canvas):
        cv2.circle(canvas, (int(self.x), int(self.y)),
                   self.radius, (255, 255, 255), -1)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def collision(ball, paddle):
    # Collision with side edges
    if ball.x - ball.radius <= 0 or ball.x + ball.radius >= 700:
        ball.x_vel = -ball.x_vel

    # Collision with top edge
    if ball.y - ball.radius <= 0:
        ball.y_vel = -ball.y_vel

    # Collision with the slider
    if (
        ball.y + ball.radius >= paddle.y - paddle.height and
        ball.x + ball.radius >= paddle.x - paddle.width // 2 and
        ball.x - ball.radius <= paddle.x + paddle.width // 2
    ):
        ball.y_vel = -ball.y_vel
        # Increase the ball's speed
        ball.x_vel *= 1.3
        ball.y_vel *= 1.3


# Function to draw pieces in the main function
def draw_pieces(frame, paddle, ball):
    paddle.draw(frame)
    ball.draw(frame)


def main():

    paddle = Paddle(WIDTH//2, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, ball_radius)
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
        draw_pieces(frame, paddle, ball)
        # handle collision function here
        collision(ball, paddle)
        # print(centroid_x, centroid_y)
        cv2.imshow('Hand Gesture Slider', frame)

        key = cv2.waitKey(10)

        if key == ord('q'):
            break

    # Release the video capture and close all OpenCV windows
    vid.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
