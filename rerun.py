import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((728, 735))
icon_image = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon_image)
pygame.display.set_caption('Space invaders')
background = pygame.image.load('background_1.png')
background_y = 0

mixer.music.load("DeathMatch (Boss Theme).ogg")
mixer.music.play(-1)

player_image = pygame.image.load('spaceship.png')
playerX = 335
playerY = 630

enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 9

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('enemy_1.png'))
    enemy_image.append(pygame.image.load('enemy_2.png'))
    enemyX.append(random.randint(0, 663))
    enemyY.append(random.randint(10, 45))
    enemyX_change.append(4)
    enemyY_change.append(4)

bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 630
bulletX_change = 0
bulletY_change = 35
bullet_state = 'ready'

clock = pygame.time.Clock()

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)
textX = 10
textY = 10

lose = pygame.font.Font('freesansbold.ttf', 70)

def show_score(x, y):
    print_score = font.render("Score: " + str(score_value), True, (255, 203, 164))
    screen.blit(print_score, (x, y))


def game_over():
    game_over_text = lose.render("GAME OVER", True, (223, 70, 97))
    screen.blit(game_over_text, (130, 335))


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def player(x, y):
    screen.blit(player_image, (round(x), round(y)))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (round(x), round(y)))


def enemy_shoot(enemyX, enemyY):
    global bullet_state
    bullet_state = 'fire'
    bullet_sound = mixer.Sound('shoot.wav')
    bullet_sound.play()
    screen.blit(bullet_image, (round(enemyX + 16), round(enemyY + 10)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_image, (round(x + 16), round(y + 10)))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y - 735))
    event_get = pygame.event.get()
    keys = pygame.key.get_pressed()
    background_y += 0.5
    if background_y >= 735:
        background_y = 0
    if keys[pygame.K_LEFT]:
        playerX -= 6.8
    if keys[pygame.K_RIGHT]:
        playerX += 6.8
    if keys[pygame.K_SPACE]:
        if bullet_state == 'ready':
            bullet_sound = mixer.Sound('shoot.wav')
            bullet_sound.play()
            bulletX = playerX
            fire_bullet(bulletX, bulletY)
    if playerX <= 0:
        playerX += 7
    if playerX >= 663:
        playerX -= 7

    for i in range(num_of_enemies):
        if enemyY[i] > 600:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            mixer.music.stop()
            bullet_sound.stop()
            bullet_state = 'ready'
            break
        # Move enemy and update bullet position
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] += 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 663:
            enemyX_change[i] -= 5
            enemyY[i] += enemyY_change[i]
        colliding = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if colliding:
            killed_sound = mixer.Sound("invaderkilled.wav")
            killed_sound.play()
            bulletY = 630
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 663)
            enemyY[i] = random.randint(10, 45)
        # draw enemy on the screen
        enemy(enemyX[i], enemyY[i], i)


    if bulletY <= 0:
        bulletY = 630
        bullet_state = 'ready'

    if bullet_state != 'fire':
        pass
    else:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    for event in event_get:
        if event.type == pygame.QUIT:
            running = False

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
    clock.tick(60)
