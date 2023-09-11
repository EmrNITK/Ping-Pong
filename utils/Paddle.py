import cv2
from utils.constants import HEIGHT, WIDTH

class Paddle:
    def __init__(self, x, y, width, height, paddle_color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.paddle_color = paddle_color
        self.width = width
        self.height = height

    def draw(self, frame):
        cv2.rectangle(
            frame,
            (int(self.x - self.width // 2), int(HEIGHT - self.height)),
            (int(self.x + self.width // 2), int(HEIGHT)),
            self.paddle_color,
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