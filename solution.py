import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (64, 224, 208)
RED = (255, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("Papyrus", 30)
WINNING_SCORE = 10

# Difficulty levels
DIFFICULTIES = {
    "Easy": {"ai_speed": 3, "ball_speed": 4},
    "Medium": {"ai_speed": 5, "ball_speed": 5},
    "Hard": {"ai_speed": 9, "ball_speed": 9},
    "Extreme": {"ai_speed": 11, "ball_speed": 12},  
}

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.VEL = speed

    def draw(self, win):
        pygame.draw.rect(win, BLUE, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.MAX_VEL = speed
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, RED, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, ((WIDTH // 4) - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, ((WIDTH * 3/4) - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def handle_ai_movement(ball, left_paddle):
    if ball.y < left_paddle.y and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    elif ball.y > left_paddle.y + left_paddle.height and left_paddle.y + left_paddle.height + left_paddle.VEL <= HEIGHT:
        left_paddle.move(up=False)

def handle_paddle_movement(keys, right_paddle):
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def choose_difficulty():
    run = True
    while run:
        WIN.fill(BLACK)
        title_text = SCORE_FONT.render("Choose Difficulty", 1, WHITE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        easy_text = SCORE_FONT.render("1. Easy", 1, WHITE)
        WIN.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 60))
        
        medium_text = SCORE_FONT.render("2. Medium", 1, WHITE)
        WIN.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 - 20))
        
        hard_text = SCORE_FONT.render("3. Hard", 1, WHITE)
        WIN.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 20))

        extreme_text = SCORE_FONT.render("4. Extreme", 1, WHITE)
        WIN.blit(extreme_text, (WIDTH // 2 - extreme_text.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return DIFFICULTIES["Easy"]
                elif event.key == pygame.K_2:
                    return DIFFICULTIES["Medium"]
                elif event.key == pygame.K_3:
                    return DIFFICULTIES["Hard"]
                elif event.key == pygame.K_4:
                    return DIFFICULTIES["Extreme"]

def display_end_screen(win_text):
    text = SCORE_FONT.render(win_text, 1, BLUE)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

    restart_text = SCORE_FONT.render("Press 'r' to Restart or 'q' to Quit", 1, WHITE)
    WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  
                    run = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def main():
    clock = pygame.time.Clock()
    difficulty = choose_difficulty()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, difficulty["ai_speed"])
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, 7)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, difficulty["ball_speed"])

    left_score = 0
    right_score = 0
    run = True

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, right_paddle)
        handle_ai_movement(ball, left_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Nice job, AI! You won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Nice job, player on the right! You won!"
    
        if won:
            display_end_screen(win_text)
            break
    
    pygame.quit()  

if __name__ == '__main__':
    main()