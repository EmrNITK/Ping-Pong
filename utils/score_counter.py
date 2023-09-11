scoreCount = 0
missCount = 0


def hit(ball, paddle):
    global scoreCount, missCount
    if (
        ball.y + ball.radius >= paddle.y - paddle.height and
        ball.x + ball.radius >= paddle.x - paddle.width // 2 and
        ball.x - ball.radius <= paddle.x + paddle.width // 2
    ):
        scoreCount = scoreCount + 1
        print(scoreCount)


def restart():
    global scoreCount, missCount
    scoreCount = 0
    missCount = 0


def miss(ball, paddle):
    global scoreCount, missCount
    if (
        ball.y + ball.radius >= paddle.y - paddle.height and
        ball.x + ball.radius <= paddle.x - paddle.width // 2 and
        ball.x - ball.radius >= paddle.x + paddle.width // 2
    ):
        missCount += 1
        print("miss", missCount)
        if (missCount >= 3):
            restart()
