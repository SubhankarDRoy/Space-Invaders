import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# game window
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('Images\\background.png')

# Background Sound
mixer.music.load('Sounds\\background.wav')
mixer.music.play(-1)

# Setting logo and name
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('Images\\icon.png')
pygame.display.set_icon(icon)

# Player(spaceship)
playerImg = pygame.image.load('Images\\spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Images\\ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2.5)
    enemyY_change.append(45)

# Bullet
bulletImg = pygame.image.load('Images\\bullets.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 14
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
goX = 200
goY = 250


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance < 33:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (x, y))



running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    show_score(textX, textY)

    for event in pygame.event.get():

        # quit functionality
        if event.type == pygame.QUIT:
            running = False

        # key detection
        if event.type == pygame.KEYDOWN:
            # right key
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            # left key
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            # space for fire
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('Sounds\\laser.wav')
                bullet_sound.play()
                # get the current x coordinate of spaceship
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            playerX_change = 0

    player(playerX, playerY)

    playerX += playerX_change
    # Boundary creation for the spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(goX, goY)
            break
        enemy(enemyX[i], enemyY[i], i)
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 8:
            enemyX_change[i] = 2.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2.5
            enemyY[i] += enemyY_change[i]
        # collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('Sounds\\explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    pygame.display.update()
