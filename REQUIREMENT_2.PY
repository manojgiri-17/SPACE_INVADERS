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

# ---------------- GAME SETUP -----------------
player = Defender(WIDTH//2 - 35, HEIGHT - 80)

running = True
while running:
    dt = clock.tick(FPS)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # -------- PLAYER MOVEMENT --------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 8:
        player.x += player.speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.WIDTH - 8:
        player.x -= player.speed

    player.update()

    # -------- DRAW --------
    screen.fill(BG_COLOR)
    player.draw(screen)
    
    pygame.display.update()

pygame.quit()
sys.exit()
