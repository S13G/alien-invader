import pygame
import random
import sys

# Define constants
# SCREEN_WIDTH = 728
# SCREEN_HEIGHT = 735
ENEMY_SPEED = 4
ENEMY_BULLET_SPEED = 2.5
ENEMY_BULLET_DAMAGE = random.randint(5, 20)
BULLET_SPEED = 30
ENEMY_COUNT = 8
SCORE_FONT_SIZE = 25
GAMEOVER_FONT_SIZE = 70
BACKGROUND_SPEED = 0.5
PLAYER_HEALTH = 100

# Initialize pygame
pygame.init()

# Set the screen size to match the display resolution
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

pygame.display.set_caption('Space invaders')

# Load resources
icon_image = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon_image)

background_image = pygame.image.load('bg6.jpg')

# Scale the background image to fit the screen
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

player_image = pygame.image.load('spaceship.png')
bullet_image = pygame.image.load('bullet.png')
enemy_images = [pygame.image.load('enemy_1.png'), pygame.image.load('enemy_2.png')]
shoot_sound = pygame.mixer.Sound('shoot.wav')
kill_sound = pygame.mixer.Sound('invaderkilled.wav')
background_music = pygame.mixer.music
background_music.load("DeathMatch (Boss Theme).ogg")
background_music.play(-1)
gameover_font = pygame.font.Font('freesansbold.ttf', GAMEOVER_FONT_SIZE)
score_font = pygame.font.Font('freesansbold.ttf', SCORE_FONT_SIZE)
enemy_bullet_image = pygame.image.load("bullet3.png")

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Create player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = pygame.FULLSCREEN / 2
        self.rect.bottom = screen_height - 5
        self.health = PLAYER_HEALTH
        all_sprites.add(self)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 7
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 7
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_height

    def shoot(self):
        if len(bullets) < 3:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    def draw_health_bar(self):
        # Draw the health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.left, self.rect.top - 10, self.rect.width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.left, self.rect.top - 10, self.health / 100 * self.rect.width, 5))
            

# Create enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = random.randrange(10, 30)
        self.speed = ENEMY_SPEED
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_delay = random.randint(3000, 5000) # time of last shot
        all_sprites.add(self)
        enemies.add(self)

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > screen_width or self.rect.left < 0:
            self.speed = -self.speed
            self.rect.y += self.rect.height
        if pygame.time.get_ticks() - self.last_shot_time > self.shot_delay:
            self.last_shot_time = pygame.time.get_ticks()
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)


    def shoot(self):
        enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(enemy_bullet)
        enemy_bullets.add(enemy_bullet)
        self.last_shot_time = pygame.time.get_ticks()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_BULLET_SPEED
        all_sprites.add(self)
        enemy_bullets.add(self)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

# Create bullet sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = BULLET_SPEED
        all_sprites.add(self)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

running = True
clock = pygame.time.Clock()
score = 0
enemies_killed = 0

# Create enemies
for i in range(ENEMY_COUNT):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Create player
player = Player()
all_sprites.add(player)

while running:
# Set framerate
    clock.tick(60)
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update sprites
    all_sprites.update()

    # Check for collisions between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemies_killed += 1
        score += 10
        kill_sound.play()
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw everything
    screen.blit(background_image, (0, 0))
    screen.blit(background_image, (0, background_image.get_height()))
    background_image_rect = background_image.get_rect()
    background_image_rect.y -= BACKGROUND_SPEED
    if background_image_rect.bottom <= 0:
        background_image_rect.y = 0
    screen.blit(background_image, background_image_rect)
    all_sprites.draw(screen)

    # Draw health bars
    for sprite in all_sprites:
        if isinstance(sprite, Player):
            sprite.draw_health_bar()

    # Draw score
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw enemies killed
    enemies_killed_text = score_font.render(f'Enemies Killed: {enemies_killed}', True, (255, 255, 255))
    screen.blit(enemies_killed_text, (screen_width - enemies_killed_text.get_width() - 10, 10))

    # Check for collisions between player and enemy bullets
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits:
        player.health -= ENEMY_BULLET_DAMAGE
        if player.health <= 0:
            player.kill()
            game_over()

    # Check for collisions between player and enemies
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        player.kill()
        game_over()

    def game_over():
        gameover_text = gameover_font.render('Game Over!', True, (223, 50, 73))
        screen.blit(gameover_text, (screen_width / 2 - gameover_text.get_width() / 2, screen_height / 2 - gameover_text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        background_music.stop()
        pygame.quit()
        sys.exit()

    # Check if game is over
    if not enemies:
        gameover_text = gameover_font.render('You Win!', True, (255, 255, 255))
        screen.blit(gameover_text, (screen_width / 2 - gameover_text.get_width() / 2, screen_height / 2 - gameover_text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        background_music.stop()
        running = False

    # Flip the display
    pygame.display.flip()

