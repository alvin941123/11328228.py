import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
FPS = 60
GRAVITY = 1
JUMP_STRENGTH = -15

# Load assets
font = pygame.font.Font(pygame.font.get_default_font(), 20)
dino_image = pygame.image.load("DINOSAUR.png")
obstacle_image = pygame.image.load("TREE.png")
background_image = pygame.image.load("DESERT.png")

# Scale images
dino_image = pygame.transform.scale(dino_image, (50, 50))
obstacle_image = pygame.transform.scale(obstacle_image, (20, 40))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()

# Dino class
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dino_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 20
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Prevent dino from falling through the floor
        if self.rect.bottom >= SCREEN_HEIGHT - 20:
            self.rect.bottom = SCREEN_HEIGHT - 20
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5  # Move obstacle to the left
        if self.rect.right < 0:
            self.kill()

# Background class
class Background:
    def __init__(self):
        self.image = background_image
        self.x1 = 0
        self.x2 = SCREEN_WIDTH

    def update(self):
        self.x1 -= 5
        self.x2 -= 5

        if self.x1 <= -SCREEN_WIDTH:
            self.x1 = SCREEN_WIDTH
        if self.x2 <= -SCREEN_WIDTH:
            self.x2 = SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))

# Game loop

def game_loop():
    running = True
    score = 0

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    # Create the dino
    dino = Dino()
    all_sprites.add(dino)

    # Create background
    background = Background()

    # Obstacle timer
    obstacle_timer = 0
    next_obstacle_time = random.randint(30, 90)  # Increased frequency and randomness

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump()

        # Update
        all_sprites.update()
        background.update()

        # Spawn obstacles
        obstacle_timer += 1
        if obstacle_timer > next_obstacle_time:
            obstacle_timer = 0
            next_obstacle_time = random.randint(30, 90)
            obstacle = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - obstacle_image.get_height() - 20)
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

        # Check collisions
        if pygame.sprite.spritecollideany(dino, obstacles):
            return score

        # Draw
        background.draw(screen)
        all_sprites.draw(screen)

        # Display score
        score += 0.05  # Lower score increment rate
        score_text = font.render(f"Score: {int(score)}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

def main():
    while True:
        # Start screen
        screen.fill(WHITE)
        start_text = font.render("Press SPACE to Start", True, BLACK)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

        # Run game loop
        score = game_loop()

        # Game over screen
        screen.fill(WHITE)
        game_over_text = font.render("Game Over", True, BLACK)
        score_text = font.render(f"Your Score: {int(score)}", True, BLACK)
        retry_text = font.render("Press R to Retry or ESC to Quit", True, BLACK)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
