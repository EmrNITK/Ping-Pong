def ScoreCounter():
    score = 0
    miss_count = 0

    def hit():
        nonlocal score, miss_count
        score = score + 1
        miss_count = 0
    def restart():
        nonlocal score, miss_count
        score = 0
        miss_count = 0
        print("Restarting Game")
    def miss():
        nonlocal miss_count
        miss_count = miss_count + 1
        if miss_count >= 3:
            restart()
