from utils.constants import WIDTH, speed_increment

def collision(ball, paddle):
    # Collision with side edges
    if ball.x - ball.radius <= 0 or ball.x + ball.radius >= WIDTH:
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
        ball.x_vel *= speed_increment
        ball.y_vel *= speed_increment