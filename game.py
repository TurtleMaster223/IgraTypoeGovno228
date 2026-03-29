import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Pygame")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
BALL_SIZE = 15

player = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

ball_speed_x = 5
ball_speed_y = 5
player_speed = 0
opponent_speed = 7

score_a, score_b = 0, 0
font = pygame.font.SysFont("Arial", 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: player_speed -= 7
            if event.key == pygame.K_s: player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: player_speed += 7
            if event.key == pygame.K_s: player_speed -= 7

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    if ball.left <= 0:
        score_b += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1
    if ball.right >= WIDTH:
        score_a += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    if opponent.top < ball.y: opponent.y += opponent_speed
    if opponent.bottom > ball.y: opponent.y -= opponent_speed

    player.y += player_speed
    player.clamp_ip(win.get_rect())
    opponent.clamp_ip(win.get_rect())


    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    win.fill(BLACK)
    pygame.draw.rect(win, WHITE, player)
    pygame.draw.rect(win, WHITE, opponent)
    pygame.draw.ellipse(win, WHITE, ball)
    pygame.draw.aaline(win, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))


    score_text = font.render(f"{score_a} : {score_b}", True, WHITE)
    win.blit(score_text, (WIDTH//2 - 30, 20))

    pygame.display.flip()
    clock.tick(60) 
