import pygame
import sys
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG ULTRA HACK V4 - FIXED SYNTAX")
clock = pygame.time.Clock()

# Шрифты и Цвета
font = pygame.font.SysFont("Consolas", 14)
WHITE, BLACK, GREEN, RED, YELLOW, BLUE, PURPLE = (255,255,255), (0,0,0), (0,255,0), (255,0,0), (255,255,0), (0,150,255), (150,0,255)

# Объекты
player = pygame.Rect(50, HEIGHT//2-45, 15, 90)
opponent = pygame.Rect(WIDTH-65, HEIGHT//2-45, 15, 90)
ball = pygame.Rect(WIDTH//2-7, HEIGHT//2-7, 14, 14)
b_sx, b_sy = 6, 6
score_a, score_b = 0, 0

# Состояния
show_menu = False
tab = 0 # 0: Cheats, 1: Visuals
sel = 0

# Словари состояний
C = {f"c{i}": False for i in range(20)}
V = {f"v{i}": False for i in range(20)}

C_NAMES = [
    "Silent Aim", "Speedhack x5", "Infinite Paddle", "Freeze Enemy", 
    "Small Enemy", "Auto-Win Score", "Ball Teleport", "Chaos Bounce", 
    "God Mode (Wall)", "Double Ball Spd", "Magnetic Field", "Hard Hit", 
    "No Clip Walls", "Enemy Lag", "Low Gravity", "Super Fast Ball", 
    "Rapid Fire", "Anti-Bounce", "Ghost Move", "Cheat Logic V2"
]

V_NAMES = [
    "Trajectory", "RGB Mode", "Motion Blur", "ESP Lines", 
    "Starfield", "Matrix Rain", "HitMarkers", "Scanlines", 
    "Ball Glow", "Crosshair", "Player Info", "Ball Trail", 
    "Screen Shake", "Flash On Hit", "Radar", "Wireframe", 
    "Chams", "Rainbow Score", "Glass Mode", "Debug Grid"
]

trail = []

def draw_menu():
    if not show_menu: return
    s = pygame.Surface((350, 520))
    s.set_alpha(240)
    s.fill((10,10,10))
    win.blit(s, (10, 10))
    pygame.draw.rect(win, BLUE if tab==0 else PURPLE, (10,10,350,520), 2)
    
    header = "[ CHEATS ]" if tab == 0 else "[ VISUALS ]"
    win.blit(font.render(header, True, YELLOW), (130, 20))

    names = C_NAMES if tab == 0 else V_NAMES
    states = C if tab == 0 else V
    prefix_key = 'c' if tab == 0 else 'v'

    for i in range(20):
        key = f"{prefix_key}{i}"
        is_on = states[key]
        color = YELLOW if i == sel else (GREEN if is_on else RED)
        status = "ON" if is_on else "OFF"
        # ИСПРАВЛЕННЫЙ ВЫВОД ТЕКСТА
        txt = f"{'>' if i == sel else ' '} {names[i]}: {status}"
        win.blit(font.render(txt, True, color), (25, 50 + i*22))

while True:
    t_ticks = pygame.time.get_ticks()
    rgb = (abs(math.sin(t_ticks*0.005))*255, abs(math.sin(t_ticks*0.005+2))*255, 255)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_HOME: show_menu = not show_menu
            if show_menu:
                if event.key == pygame.K_UP: sel = (sel - 1) % 20
                if event.key == pygame.K_DOWN: sel = (sel + 1) % 20
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                    tab = 1 - tab
                    sel = 0
                if event.key == pygame.K_RETURN: 
                    k = f"{'c' if tab==0 else 'v'}{sel}"
                    if tab == 0: C[k] = not C[k]
                    else: V[k] = not V[k]

    # --- ЛОГИКА ---
    p_spd = 25 if C["c1"] else 7
    player.height = HEIGHT if C["c2"] else 90
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.top > 0: player.y -= p_spd
    if keys[pygame.K_s] and player.bottom < HEIGHT: player.y += p_spd

    # Silent Aim & Magnet
    if (C["c0"] or C["c10"]) and b_sx < 0:
        if ball.centery < player.centery: b_sy = abs(b_sy)
        else: b_sy = -abs(b_sy)

    # Движение мяча
    ball.x += b_sx * (2.5 if C["c15"] else 1)
    ball.y += b_sy

    # God Mode (Стена)
    if C["c8"] and ball.left <= player.right + 10: b_sx = abs(b_sx)

    if ball.top <= 0 or ball.bottom >= HEIGHT: b_sy *= -1
    
    if ball.colliderect(player):
        b_sx = abs(b_sx)
        if C["c7"]: b_sy = random.randint(-12, 12) # Chaos
    if ball.colliderect(opponent):
        b_sx = -abs(b_sx)

    # Score
    if ball.left <= 0: 
        score_b += 1
        ball.center = (WIDTH//2, HEIGHT//2)
    if ball.right >= WIDTH: 
        score_a += (10 if C["c5"] else 1)
        ball.center = (WIDTH//2, HEIGHT//2)

    # AI Врага
    if not C["c3"]: # Freeze
        opponent.height = 20 if C["c4"] else 90
        spd_e = 2 if C["c13"] else 5 # Lag
        if opponent.centery < ball.centery: opponent.y += spd_e
        else: opponent.y -= spd_e

    # --- ВИЗУАЛЫ ---
    win.fill(BLACK)
    
    if V["v0"]: # Траектория
        tx, ty, tsx, tsy = ball.centerx, ball.centery, b_sx, b_sy
        points = [(tx, ty)]
        for _ in range(10):
            tx += tsx * 25
            ty += tsy * 25
            if ty <= 0 or ty >= HEIGHT: tsy *= -1
            points.append((tx, ty))
            if tx <= 0 or tx >= WIDTH: break
        if len(points) > 1: pygame.draw.lines(win, YELLOW, False, points, 2)

    if V["v3"]: # ESP
        pygame.draw.line(win, GREEN, player.center, ball.center, 1)
        pygame.draw.line(win, RED, opponent.center, ball.center, 1)

    if V["v11"]: # Trail
        trail.append(ball.center)
        if len(trail) > 15: trail.pop(0)
        for p in trail: pygame.draw.circle(win, BLUE, p, 4)

    # Отрисовка
    p_col = rgb if V["v1"] else WHITE
    pygame.draw.rect(win, p_col, player)
    pygame.draw.rect(win, WHITE if not V["v16"] else (40,40,40), opponent)
    
    if not V["v18"]: # Glass mode
        pygame.draw.ellipse(win, rgb if V["v8"] else WHITE, ball)

    win.blit(font.render(f"P1: {score_a}  P2: {score_b}", True, WHITE), (WIDTH//2-50, 10))
    draw_menu()
    pygame.display.flip()
    clock.tick(60)
