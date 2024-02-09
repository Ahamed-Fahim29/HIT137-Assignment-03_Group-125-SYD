# https://github.com/Ahamed-Fahim29/HIT137-Assignment-03_Group-125-SYD
import pygame
import sys
import random
import os
import math

# Initialize Pygame
pygame.init()

# Set up display constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up paths for images
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')

# Load images with appropriate sizes
background_images = [pygame.image.load(os.path.join(image_path, f"background_{i}.jpg")) for i in range(1, 4)]
background_images = [pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT)) for image in background_images]

player_images = [pygame.image.load(os.path.join(image_path, f"player_{i}.png")) for i in range(1, 4)]
player_images = [pygame.transform.scale(image, (150, 150)) for image in player_images]

collectible_images = [pygame.image.load(os.path.join(image_path, f"collectible_{i}.png")) for i in range(1, 4)]
collectible_images = [pygame.transform.scale(image, (40, 40)) for image in collectible_images]

special_collectible_image = pygame.image.load(os.path.join(image_path, "special_collectible.png"))
special_collectible_image = pygame.transform.scale(special_collectible_image, (50, 50))

projectile_image = pygame.image.load(os.path.join(image_path, "projectile.jpg"))
projectile_image = pygame.transform.scale(projectile_image, (15, 15))

boss_enemy_image = pygame.image.load(os.path.join(image_path, "boss_enemy.png"))
boss_enemy_image = pygame.transform.scale(boss_enemy_image, (300, 300))

enemy_image = pygame.image.load(os.path.join(image_path, "enemy.png"))
enemy_image = pygame.transform.scale(enemy_image, (90, 90))

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = player_images
        self.image = self.images[0]  # Initial image
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.speed_y = 0
        self.speed_x = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.jump_levels = 3  # Number of jump levels
        self.current_jump = 0  # Current jump level
        self.jump_height = [SCREEN_HEIGHT * 2 // 3, SCREEN_HEIGHT * 1 // 3, SCREEN_HEIGHT * 0]  # Jump heights
        self.health = 100
        self.lives = 3
        self.score = 0
        self.level = 1

    def update(self):
        # Apply gravity
        self.speed_y += self.gravity

        # Update player position
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # Check if player is on the ground
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0
            self.current_jump = 0  # Reset jump level when on the ground

        # Ensure player stays within screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def jump(self):
        # Player jumps if not already at the maximum jump level
        if self.current_jump < self.jump_levels:
            self.speed_y = self.jump_power
            self.rect.y += self.jump_height[self.current_jump] - self.rect.bottom
            self.current_jump += 1

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.lives -= 1
            self.health = 100
            if self.lives <= 0:
                return True
        return False

# Define Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, angle, speed, damage):
        super().__init__()
        self.image = pygame.transform.rotate(projectile_image, angle)
        self.rect = self.image.get_rect()
        self.angle = math.radians(angle)
        self.speed = speed
        self.damage = damage

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y -= self.speed * math.sin(self.angle)

# Define Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(900, 1200), random.randint(50, SCREEN_HEIGHT - 50))
        self.speed_x = -5 - level * 2
        self.health = 100

    def update(self):
        self.rect.x += self.speed_x

# Define Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = collectible_images[level - 1]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(900, 1200), random.randint(50, SCREEN_HEIGHT - 50))
        self.speed_x = -3

    def update(self):
        self.rect.x += self.speed_x

# Define BossEnemy class
class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = boss_enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (700, 200)  # Static position
        self.speed_x = 0
        self.health = 500
        self.lives = 5
        self.shot_delay = 0
        self.projectiles = pygame.sprite.Group()

    def update(self):
        if self.shot_delay <= 0:
            # Shoot projectile
            self.shoot_projectile()
            self.shot_delay = 60  # Reset shot delay to 60 frames (1 second at 60 FPS)
        else:
            self.shot_delay -= 1

        # Update projectiles
        self.projectiles.update()

    def shoot_projectile(self):
        angle = random.randint(160, 200)
        projectile = Projectile(angle, 8, 10)  # Angle, speed, damage
        projectile.rect.center = self.rect.center
        self.projectiles.add(projectile)

    # Function to handle boss enemy getting hit
    def take_hit(self):
        self.health -= 10
        if self.health <= 0:
            self.lives -= 1
            if self.lives <= 0:
                return True
            else:
                self.health = 500  # Reset health for next life
        return False

# Define game over function
def game_over(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    instructions_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
    instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(instructions_text, instructions_rect)

    pygame.display.flip()

    # Wait for player to press 'R' to restart or 'Q' to quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Define main function
def main():
    # Initialize Pygame screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("simple side-scrolling 2D game")

    # Create clock object to control FPS
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    # Create player object
    player = Player()
    all_sprites.add(player)

    # Define level variable
    level = 1

    # Define score thresholds for each level
    LEVEL_2_THRESHOLD = 50
    LEVEL_3_THRESHOLD = 100

    # Flag to track whether the special collectible has appeared
    special_collectible_appeared = False

    # Flag to track boss enemy kill count
    boss_enemy_kills = 0

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Player jumps when spacebar is pressed
                    player.jump()
                elif event.key == pygame.K_LEFT:
                    # Move player left
                    player.speed_x = -5
                elif event.key == pygame.K_RIGHT:
                    # Move player right
                    player.speed_x = 5
                elif event.key == pygame.K_UP:
                    # Player shoots projectile upwards
                    projectile = Projectile(45, 10, 10)  # Angle, speed, damage
                    projectile.rect.center = player.rect.center
                    all_sprites.add(projectile)
                    projectiles.add(projectile)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    # Stop player movement when arrow keys released
                    player.speed_x = 0

        # Update game elements
        all_sprites.update()

        # Spawn boss enemy if in level 3 and score is 105
        if level == 3 and player.score >= 105:
            # Add boss enemy
            boss_enemy = BossEnemy(level)
            all_sprites.add(boss_enemy)
            enemies.add(boss_enemy)
        elif level == 2 and player.score >= LEVEL_2_THRESHOLD:
            if random.randint(0, 100) < 3 + level * 2:
                enemy = Enemy(level)
                all_sprites.add(enemy)
                enemies.add(enemy)

            if random.randint(0, 100) < 2 + level:
                collectible = Collectible(level)
                all_sprites.add(collectible)
                collectibles.add(collectible)
        elif level == 1:
            if random.randint(0, 100) < 3 + level * 2:
                enemy = Enemy(level)
                all_sprites.add(enemy)
                enemies.add(enemy)

            if random.randint(0, 100) < 2 + level:
                collectible = Collectible(level)
                all_sprites.add(collectible)
                collectibles.add(collectible)

        # Check for collisions between player and enemies
        if pygame.sprite.spritecollide(player, enemies, True):
            if player.take_damage(10):
                # Game over, prompt for restart or quit
                if not game_over(screen):
                    return

        # Check for collisions between player and collectibles
        collected = pygame.sprite.spritecollide(player, collectibles, True)
        for collectible in collected:
            # Add score or health to player based on the type of collectible
            player.score += 10

        # Check for collisions between projectiles and enemies
        for projectile in projectiles:
            enemies_hit = pygame.sprite.spritecollide(projectile, enemies, True)
            for enemy in enemies_hit:
                enemy.health -= projectile.damage
                if enemy.health <= 0:
                    if isinstance(enemy, BossEnemy):
                        boss_enemy.take_hit()  # Update boss enemy hit mechanism
                        player.score += 10  # Increase score if boss enemy is hit
                        if boss_enemy_kills >= 10:
                            show_congratulations_screen(screen, "Congratulations! You defeated the Boss!")
                            return
                    else:
                        player.score += 50  # Increase score if enemy is killed
                projectiles.remove(projectile)
                all_sprites.remove(projectile)

        # Check if the player's score meets the threshold for level progression
        if level == 1 and player.score >= LEVEL_2_THRESHOLD:
            level = 2
            player.image = player_images[1]
            show_congratulations_screen(screen, "Congratulations! Level 2 Unlocked!")
        elif level == 2 and player.score >= LEVEL_3_THRESHOLD:
            level = 3
            player.image = player_images[2]
            show_congratulations_screen(screen, "Congratulations! Level 3 Unlocked!")
        elif level == 3 and player.score >= 200:
            show_congratulations_screen(screen, "Congratulations! You've reached the boss level!")
            return

        # Spawn special collectible if the player scores half of the current level's threshold
        if not special_collectible_appeared:
            if player.score >= LEVEL_2_THRESHOLD // 2 and level == 1:
                special_collectible = Collectible(level)
                special_collectible.image = special_collectible_image
                all_sprites.add(special_collectible)
                collectibles.add(special_collectible)
                special_collectible_appeared = True

            if player.score >= LEVEL_3_THRESHOLD // 2 and level == 2:
                special_collectible = Collectible(level)
                special_collectible.image = special_collectible_image
                all_sprites.add(special_collectible)
                collectibles.add(special_collectible)
                special_collectible_appeared = True

        # Draw everything on the screen
        screen.fill(BLACK)
        screen.blit(background_images[level - 1], (0, 0))

        all_sprites.draw(screen)

        # Display score, health, lives, and level
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(player.score), True, WHITE)
        screen.blit(score_text, (10, 10))

        player_health_bar = pygame.Rect(10, 50, player.health, 20)
        pygame.draw.rect(screen, GREEN, player_health_bar)

        lives_text = font.render("Lives: " + str(player.lives), True, WHITE)
        screen.blit(lives_text, (10, 80))

        for enemy in enemies:
            enemy_health_bar = pygame.Rect(enemy.rect.x, enemy.rect.y - 5, min(enemy.health, 50), 5)
            pygame.draw.rect(screen, RED, enemy_health_bar)

        # Update the displayed level based on the player's progress
        level_text = font.render("Level: " + str(level), True, WHITE)
        screen.blit(level_text, (10, 110))

        # Display difficulty level
        difficulty_text = font.render("Difficulty: " + ["Simple", "Medium", "Hard"][level - 1], True, WHITE)
        screen.blit(difficulty_text, (10, 140))

        # Update display
        pygame.display.flip()

        # Limit FPS
        clock.tick(FPS)

def show_congratulations_screen(screen, message):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Display for 2 seconds

if __name__ == "__main__":
    main()
