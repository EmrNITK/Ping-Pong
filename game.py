import cv2
import time
WIDTH, HEIGHT = 700,500
ball_radius = 15
PADDLE_WIDTH, PADDLE_HEIGHT =  150,20
WHITE = (255,255,255)
FPS = 100
frame_delay = 1 / FPS
canvas = cv2.imread("blank.png")  
canvas = cv2.resize(canvas,(WIDTH,HEIGHT))

class Paddle:
    COLOR = WHITE
    VEL = 10
    def __init__(self,x,y,width,height):
        self.x =self.original_x =  x
        self.y =self.original_y =  y
        self.width = width
        self.height = height
    
    def draw(self,canvas):
        cv2.rectangle(
            canvas,
            (int(WIDTH//2 - self.width // 2), int(HEIGHT - self.height)),
            (int(WIDTH//2 + self.width // 2), int(HEIGHT)),
            (255, 255, 255),
            -1,
        )
    
    def move(self, move_right = True):
        if move_right == True:
            self.x += self.VEL
        else:
            self.x -= self.VEL
  
    
    def reset(self):
        self.x = self. original_x
        self.y = self.original_y
        
class Ball:
    MAX_VEL = 5
    ball_color = WHITE
    def __init__(self,x,y,radius):
        self.x = self.original_x=x
        self.y = self.original_y= y
        self.radius = radius
        self.x_vel = 0
        self.y_vel =self.MAX_VEL
    
    def draw(self,canvas):
        cv2.circle(canvas, (self.x,self.y), self.radius, (255, 255, 255), -1)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y 
        self.y_vel = 0
        self.x_vel *= -1
        
def draw(canvas,ball,paddle):
    canvas.fill(0)
    ball.draw(canvas)
    paddle.draw(canvas)
        
def main():
    ball = Ball(WIDTH//2,HEIGHT//2,ball_radius)
    paddle = Paddle(WIDTH//2,HEIGHT,PADDLE_WIDTH,PADDLE_HEIGHT)
    while True:
        start_time = time.time()
        draw(canvas,ball,paddle)
        ball.move()
        
        
        cv2.imshow("Pong Game", canvas)
        elapsed_time = time.time() - start_time
        if elapsed_time < frame_delay:
            time.sleep(frame_delay - elapsed_time)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()