import pygame, random, os, sys

pygame.init()

# ------------------ SETTINGS ------------------
WIDTH, HEIGHT = 600, 700
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# ------------------ COLORS ------------------
WHITE = (255,255,255)
YELLOW = (240,220,40)
RED = (255,20,20)
GREEN = (50,220,50)
BG_COLOR = (6,6,12)

# ------------------ IMAGE LOADING ------------------
def load_image(filename, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    return None

# ------------------ CLASSES ------------------
class Bullet:
    def __init__(self, x, y, vy, color):
        self.rect = pygame.Rect(x, y, 6, 12)
        self.vy = vy
        self.color = color

    def update(self):
        self.rect.y += self.vy

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

class Invader:
    WIDTH = 40
    HEIGHT = 30
    def __init__(self, x, y, image, score):
        self.img = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT)) if image else None
        self.x = x
        self.y = y
        self.score_val = score
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

    def update(self):
        self.rect.topleft = (self.x, self.y)

    def draw(self, surf):
        if self.img:
            surf.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(surf, WHITE, self.rect)

class Defender:
    WIDTH = 70
    HEIGHT = 60
    def __init__(self, x, y):
        img = load_image("defender.png")
        self.img = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT)) if img else None
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
            pygame.draw.rect(surf, GREEN, self.rect)

class Barrier:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 6)
        self.exists = True

    def draw(self, surf):
        if self.exists:
            pygame.draw.rect(surf, GREEN, self.rect)

def create_barrier(x, y):
    blocks = []
    for row in range(12):
        for col in range(20):
            if row < 4 or col < 4 or col > 15:
                continue
            blocks.append(Barrier(x + col * 6, y + row * 6))
    return blocks

# ------------------ LOAD INVADER IMAGES ------------------
inv1_img = load_image("invader1.png")
inv2_img = load_image("invader2.png")
inv3_img = load_image("invader3.png")

# ------------------ SPAWN INVADERS ------------------
rows_setup = [
    (inv1_img, 30),
    (inv2_img, 20),
    (inv3_img, 10),
    (inv3_img, 10),
]

invaders = []

def spawn_invaders(cols=10, start_x=40, start_y=80, sx=48, sy=48):
    invaders.clear()
    for r, (img, pts) in enumerate(rows_setup):
        y = start_y + r * sy
        for c in range(cols):
            x = start_x + c * sx
            invaders.append(Invader(x, y, img, pts))

spawn_invaders()

# ------------------ GAME OBJECTS ------------------
player = Defender(WIDTH//2 - 35, HEIGHT - 80)
player_bullets = []
enemy_bullets = []

# Barriers
barriers = []
gap = WIDTH // 5
for i in range(4):
    bx = gap * (i+1) - 60
    by = HEIGHT - 200
    barriers.append(create_barrier(bx, by))

# ------------------ MOVEMENT VARIABLES ------------------
move_right = True
initial_enemy_speed = 0.3
enemy_speed = initial_enemy_speed
total_invaders = len(invaders)
enemy_drop = 18
enemy_shoot_rate = 2500
last_enemy_shot = pygame.time.get_ticks()

# ------------------ LIFE ICON ------------------
life_icon = pygame.transform.scale(load_image("defender.png", (20,20)), (20,20)) if os.path.exists("defender.png") else None

# ------------------ GAME LOOP ------------------
running = True
while running:
    dt = clock.tick(FPS)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    # -------- INVADER MOVEMENT --------
    dead = total_invaders - len(invaders)
    enemy_speed = 0.3 + dead * 0.07

    move_down = False
    for inv in invaders:
        test_x = inv.x + (enemy_speed if move_right else -enemy_speed)
        if test_x <= 8 or test_x + inv.rect.width >= WIDTH - 8:
            move_down = True
            break

    for inv in invaders:
        inv.x += enemy_speed if move_right else -enemy_speed

    if move_down:
        move_right = not move_right
        for inv in invaders:
            inv.y += enemy_drop

    # -------- ENEMY SHOOTING --------
    now = pygame.time.get_ticks()
    if now - last_enemy_shot > enemy_shoot_rate and invaders:
        shooter = random.choice(invaders)
        bx = shooter.x + shooter.WIDTH//2 - 3
        by = shooter.y + shooter.HEIGHT
        enemy_bullets.append(Bullet(bx, by, 6, RED))
        last_enemy_shot = now

    # -------- UPDATE BULLETS --------
    for b in player_bullets[:]:
        b.update()
        # Remove off-screen
        if b.rect.y < -20:
            player_bullets.remove(b)
            continue
        # Collision with invaders
        for inv in invaders[:]:
            if b.rect.colliderect(inv.rect):
                player_bullets.remove(b)
                invaders.remove(inv)
                break
        # Collision with barriers
        for barrier in barriers:
            for block in barrier:
                if block.exists and b.rect.colliderect(block.rect):
                    block.exists = False
                    if b in player_bullets:
                        player_bullets.remove(b)
                    break

    for b in enemy_bullets[:]:
        b.update()
        # Remove off-screen
        if b.rect.y > HEIGHT + 20:
            enemy_bullets.remove(b)
            continue
        # Collision with player
        if b.rect.colliderect(player.rect):
            enemy_bullets.remove(b)
            player.lives -= 1
            if player.lives > 0:
                player.x = WIDTH//2 - player.WIDTH//2
                player.y = HEIGHT - 80
            else:
                print("Game Over")
                running = False
        # Collision with barriers
        for barrier in barriers:
            for block in barrier:
                if block.exists and b.rect.colliderect(block.rect):
                    block.exists = False
                    if b in enemy_bullets:
                        enemy_bullets.remove(b)
                    break

    # -------- DRAW --------
    screen.fill(BG_COLOR)
    for inv in invaders:
        inv.update()
        inv.draw(screen)
    for b in player_bullets:
        b.draw(screen)
    for b in enemy_bullets:
        b.draw(screen)
    player.draw(screen)
    # Draw barriers
    for barrier in barriers:
        for block in barrier:
            block.draw(screen)
    # Draw lives
    for i in range(player.lives):
        if life_icon:
            screen.blit(life_icon, (10 + i*25, HEIGHT - 25))
    pygame.display.update()

pygame.quit()
sys.exit()
