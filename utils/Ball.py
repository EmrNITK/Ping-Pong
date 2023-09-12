import cv2

class Ball:
    def __init__(self, x, y, radius, MAX_VEL, ball_color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.MAX_VEL = MAX_VEL
        self.ball_color = ball_color
        self.x_vel = MAX_VEL
        self.y_vel = -1*MAX_VEL

    def draw(self, canvas):
        cv2.circle(canvas, (int(self.x), int(self.y)),
                   self.radius, (255, 255, 255), -1)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel = self.MAX_VEL
        self.y_vel = -1*self.MAX_VEL