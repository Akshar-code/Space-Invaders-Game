import pygame
import random
import math
from pygame import mixer
# initiate pygame
pygame.init()
# create screen
screen = pygame.display.set_mode((800, 600))
running = True

# title and icon
pygame.display.set_caption('Space Invaders')
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# preferred icon size is 32px
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Background Image
background = pygame.image.load('background.jpg')

#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)
# player stats
player_image = pygame.image.load('spaceship.png')
playerx = 370
playery = 480
playerx_change = 0
playery_change = 0

# enemy stats
enemy_image = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(0.7)
    enemyy_change.append(40)

# bullet stats
bullet_image = pygame.image.load('bullet.png')
bulletx = 0
bullety = 0
bullet_state = 'ready'
bullety_change = 3

#Score
score = 0
textx = 10
texty = 10
font = pygame.font.SysFont('comicsans',30)
game_over_font = pygame.font.SysFont('comicsans',100)

def game_over():
    text = game_over_font.render('GAME OVER',1,(255,255,255))
    screen.blit(text,(205,250))
def show_score(x,y):
    text = font.render('Score : {}'.format(score), 1, (0, 255, 00))
    screen.blit(text,(x,y))

def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y,i):
    screen.blit(enemy_image[i], (x, y))


def open_fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_image, (x + 16, y + 10))


# function for creating boundaries
def boundary_creation(x, y):
    if x < 0 and y < 0:
        x, y = 0, 0
    elif x < 0 and y > 536:
        x, y = 0, 536
    elif x > 736 and y < 0:
        x, y = 736, 0
    elif x > 736 and y > 536:
        x, y = 736, 536
    elif x < 0:
        x = 0
    elif x > 736:
        x = 736
    elif y < 0:
        y = 0
    elif y > 536:
        y = 536
    return x, y


def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((x1 - y1) ** 2 + (x2 - y2) ** 2)
    if distance < 27:
        return True
    return False


# gameloop
while running:
    screen.fill(WHITE)
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    bullety = playery
                    open_fire(bulletx, bullety)
            if event.key == pygame.K_LEFT:
                playerx_change = -2.5
            elif event.key == pygame.K_RIGHT:
                playerx_change = 2.5
            elif event.key == pygame.K_UP:
                playery_change = -2.5
            elif event.key == pygame.K_DOWN:
                playery_change = 2.5

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                playerx_change = 0
                playery_change = 0
    # Player movement mechanics
    playerx += playerx_change
    playery += playery_change
    playerx, playery = boundary_creation(playerx, playery)

    # Enemy Movement mechanics
    for i in range(num_of_enemies):
        if enemyy[i] > 480:
            for j in range(num_of_enemies):
                enemyy[j] = 1000
            game_over()
            break
        enemyx[i] += enemyx_change[i]
        if enemyx[i] < 0:
            enemyx_change[i] = 0.7
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] > 736:
            enemyx_change[i] = -0.7
            enemyy[i] += enemyy_change[i]
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletx = playerx
            bullety = playery
            bullet_state = 'ready'
            score += 1
            print(score)
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)
        enemyx[i], enemyy[i] = boundary_creation(enemyx[i], enemyy[i])
        enemy(enemyx[i], enemyy[i],i)

    if bullety <= 0:
        bullet_state = 'ready'
        bullety = 480
    if bullet_state == 'fire':
        open_fire(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(textx,texty)
    # to constantly update the screen
    pygame.display.update()
