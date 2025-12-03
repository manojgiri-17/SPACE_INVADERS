import pygame, sys, os, random

pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255,255,255)
YELLOW = (240,220,40)
RED = (255,20,20)
BG_COLOR = (6,6,12)

# ---------------- LOAD IMAGE FUNCTION ----------------
def load_image(filename):
    if os.path.exists(filename):
        return pygame.image.load(filename).convert_alpha()
    return None

life_icon = pygame.transform.scale(load_image("defender.png"), (20,20))

# ---------------- DEFENDER CLASS -----------------
class Defender:
    WIDTH = 70
    HEIGHT = 60
    def __init__(self, x, y):
        img = load_image("defender.png")
        if img:
            self.img = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
        else:
            self.img = None
        self.x = x
        self.y = y
        self.speed = 6
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.lives = 3

    def update(self):
        self.rect.topleft = (self.x, self.y)

    def draw(self, surf):
        if self.img:
            surf.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(surf, (40,200,40), self.rect)

# ---------------- BULLET CLASS -----------------
class Bullet:
    def __init__(self, x, y, vy, color):
        self.rect = pygame.Rect(x, y, 6, 12)
        self.vy = vy
        self.color = color

    def update(self):
        self.rect.y += self.vy

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

# ---------------- GAME SETUP -----------------
player = Defender(WIDTH//2 - 35, HEIGHT - 80)
player_bullets = []

invaders = []
invader_bullets = []

running = True
while running:
    dt = clock.tick(FPS)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Shoot bullet on key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_bullets.append(Bullet(player.x + player.WIDTH//2 - 3, player.y, -8, YELLOW))
    
    # -------- PLAYER MOVEMENT --------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 8:
        player.x -= player.speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.WIDTH - 8:
        player.x += player.speed

    player.update()
    
    # -------- UPDATE BULLETS --------
    for b in player_bullets[:]:
        b.update()
        # Remove bullets off-screen
        if b.rect.y < -20:
            player_bullets.remove(b)
        else:
            # Check collision with invaders
            for inv in invaders[:]:
                if b.rect.colliderect(inv.rect):
                    player_bullets.remove(b)
                    invaders.remove(inv)
                    break

    for b in invader_bullets[:]:
        b.update()
        if b.rect.y > HEIGHT + 20:
            invader_bullets.remove(b)
        else:
            # Check collision with player
            if b.rect.colliderect(player.rect):
                invader_bullets.remove(b)
                player.lives -= 1
                if player.lives > 0:
                    # respawn player at center
                    player.x = WIDTH//2 - player.WIDTH//2
                    player.y = HEIGHT - 80
                else:
                    print("Game Over")
                    running = False

    # -------- DRAW --------
    screen.fill(BG_COLOR)
    player.draw(screen)
    
    for b in player_bullets:
        b.draw(screen) 
    
    # Draw player lives
    for i in range(player.lives):
        screen.blit(life_icon, (10 + i*25, HEIGHT - 25))

    pygame.display.update()

pygame.quit()
sys.exit()
