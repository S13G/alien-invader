import math
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
PLAYER_HEALTH = 100

# Initialize pygame
pygame.init()

# Set the screen size to match the display resolution
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

transition_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

transition_surface.fill((255, 255, 255))

pygame.display.set_caption('resources/MapleStory Universe')

# Load resources
icon_image = pygame.image.load('resources/player.png')

pygame.display.set_icon(icon_image)

background_image = pygame.image.load('resources/bg.JPG')

main_background_image = pygame.image.load('resources/bg2.jpg')

# Set up the initial position of the background
background_x = 0

# Set up the scrolling speed of the background
scroll_speed = 1

# Scale the background image to fit the screen
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_image2 = background_image.copy()

main_background_image = pygame.transform.scale(main_background_image, (screen_width, screen_height))

# Create a start button
start_button = pygame.image.load('resources/start1.png')
start_button_rect = start_button.get_rect(center=(screen.get_width()/2, screen.get_height()/2 + 50))


player_image = pygame.image.load('resources/player.png')
bullet_image = pygame.image.load('resources/bullet.png')
enemy_images = [pygame.image.load('resources/enemy_1.png'), pygame.image.load('resources/enemy_2.png')]
shoot_sound = pygame.mixer.Sound('resources/shoot.wav')
kill_sound = pygame.mixer.Sound('resources/invaderkilled.wav')
gameover_font = pygame.font.Font('resources/TeachableSans-Bold.ttf', GAMEOVER_FONT_SIZE)
score_font = pygame.font.Font('resources/TeachableSans-Bold.ttf', SCORE_FONT_SIZE)
enemy_bullet_image = [pygame.image.load("resources/bullet3.png"), pygame.image.load('resources/bullet5.png')]

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
        self.rect.y = random.randrange(-10, 30)
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
        self.image = random.choice(enemy_bullet_image)
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


def game_loop():
    global running, score, enemies_killed, transition_alpha, background_x
    background_music = pygame.mixer.music
    background_music.load("resources/DeathMatch (Boss Theme).ogg")
    background_music.play(-1)

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
        for _ in hits:
            enemies_killed += 1
            score += 10
            kill_sound.play()
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        

        # Draw everything
        screen.blit(background_image, (background_x, 0))
        if background_x > 0:
            screen.blit(background_image, (background_x - screen_width, 0))
        else:
            screen.blit(background_image, (background_x + screen_width, 0))
        # Scroll the background image to the left
        background_x -= scroll_speed
        # If the background goes off the screen, wrap it around to the right side
        if background_x <= -screen_width:
            background_x = 0
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

        # Draw transition effect
        if transition_alpha > 0:
            transition_surface.set_alpha(transition_alpha)
            screen.blit(transition_surface, (0, 0))
            transition_alpha = max(0, transition_alpha - 5)

        # Check for collisions between player and enemy bullets
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for _ in hits:
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
        clock.tick(60)
    background_music.stop()


# Main Screen
main_background_music = pygame.mixer.music
main_background_music.load("resources/Alone.ogg")
main_background_music.play(-1)
# Main screen loop
while True:
    # Draw the background image
    screen.blit(main_background_image, (0, 0))
    
    # Draw the start button
    screen.blit(start_button, start_button_rect)

    # Check for mouse click on start button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_pos):
                main_background_music = pygame.mixer.music
                main_background_music.load("resources/Alone.ogg")
                main_background_music.play(-1)
                transition_alpha = 255
                pygame.mixer.music.stop()
                # Start the game
                game_loop()
                running = True
                pygame.mixer.music
                pygame.mixer.music.load("resources/Alone.ogg")
                pygame.mixer.music.play(-1)
   
    pygame.display.flip()
    clock.tick(60)