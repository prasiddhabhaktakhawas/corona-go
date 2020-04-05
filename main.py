import pygame
import random
import math
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800, 600))
back = pygame.image.load("background.jpg")
mixer.music.load('backmusic.mp3')
mixer.music.play(-1)
pygame.display.set_caption("CORONA GO !")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
player = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8
for i in range(num_of_enemies):
    enemyX_change.append(2)
    enemyY_change.append(40)
    enemy.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(32, 735))
    enemyY.append(random.randint(50, 150))
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
def show_score(x, y):
    score_value = font.render("Score:" + str(score), True, (255,255,255))
    screen.blit(score_value, (x, y))
def players(x,y):
    screen.blit(player, (x, y))
def enemies(x,y,i):
    screen.blit(enemy[i], (x, y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY - bulletY,2))
    if distance < 27:
        return True
    else:
        return False
over_font1 = pygame.font.Font('freesansbold.ttf', 50)
over_font2 = pygame.font.Font('freesansbold.ttf', 100)
def game_over_text():
    over_text1 = over_font1.render("YOU HAVE BEEN INFECTED BY", True, (255,0,0))
    over_text2 = over_font2.render("CORONA", True, (255, 0, 0))
    screen.blit(over_text1, (30, 200))
    screen.blit(over_text2, (200, 300))

#gameloop
running = True
while running:

    screen.blit(back, (0,0))
    pygame.draw.line(screen, (205, 92, 92), (0, 425), (800, 425))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                 playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)
        enemies(enemyX[i], enemyY[i],i)
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    players(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()