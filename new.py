import pygame
import random

# Define constants
SCREEN_WIDTH = 728
SCREEN_HEIGHT = 735
ENEMY_SPEED = 4
BULLET_SPEED = 35
ENEMY_COUNT = 18
SCORE_FONT_SIZE = 25
GAMEOVER_FONT_SIZE = 70
BACKGROUND_SPEED = 0.5

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space invaders')

# Load resources
icon_image = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon_image)
background_image = pygame.image.load('background_1.png')
player_image = pygame.image.load('spaceship.png')
bullet_image = pygame.image.load('bullet.png')
enemy_images = [pygame.image.load('enemy_1.png'), pygame.image.load('enemy_2.png')]
shoot_sound = pygame.mixer.Sound('shoot.wav')
kill_sound = pygame.mixer.Sound('invaderkilled.wav')
gameover_font = pygame.font.Font('freesansbold.ttf', GAMEOVER_FONT_SIZE)
score_font = pygame.font.Font('freesansbold.ttf', SCORE_FONT_SIZE)

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 7
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 7
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        if len(bullets) < 3:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

# Create enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -50)
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speed = -self.speed
            self.rect.y += self.rect.height

# Create bullet sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Player.shoot()

    # Update sprites
    all_sprites.update()

    # Draw everything
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
