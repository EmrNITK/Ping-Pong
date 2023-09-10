def handle_collision(ball,paddle):
    
    # handle collision with paddle
    if ((ball.x >= paddle.x - (paddle.width //2)) and (ball.x <= paddle.x + (paddle.width //2))):
        if (ball.y + ball.radius >= HEIGHT):
            print("ball colleded")
            ball.y_vel *= -1
    
            middle_x = paddle.x + paddle.WIDTH / 2
            difference_in_x = middle_x - ball.x
            reduction_factor = (paddle.width / 2) / ball.MAX_VEL
            x_vel = difference_in_x / reduction_factor
            ball.x_vel = -1 * x_vel    
    # handle collision with upper boundry        
    if (ball.y <= ball.radius):
        print("upper boundry collision")
        ball.y_vel *= -1
        
    if (ball.x <= ball.radius):
        print("left boundry collision")
        ball.x_vel *= -1
    
    if (ball.x + ball.radius >= WIDTH):
        print("right boundry collision")
        ball.x_vel *= -1
