import pygame, random, os, sys

pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
FPS = 60

# ------------------ LOAD IMAGES ------------------
def load_image(filename):
    if os.path.exists(filename):
        return pygame.image.load(filename).convert_alpha()
    return None

inv1_img = load_image("invader1.png")
inv2_img = load_image("invader2.png")
inv3_img = load_image("invader3.png")

# ------------------ INVADER CLASS ------------------
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
            pygame.draw.rect(surf, (200, 200, 200), self.rect)

# ------------------ BULLET CLASS ------------------
class Bullet:
    def __init__(self, x, y, vy, color):
        self.x = x
        self.y = y
        self.vy = vy
        self.color = color
        self.rect = pygame.Rect(x, y, 6, 12)

    def update(self):
        self.y += self.vy
        self.rect.y = self.y

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# ------------------ SPAWNING INVADERS ------------------
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

# ------------------ ENEMY BULLET SYSTEM ------------------
enemy_bullets = []
enemy_shoot_rate = 2500
last_enemy_shot = pygame.time.get_ticks()

# ------------------ MOVEMENT VARIABLES ------------------
move_right = True
initial_enemy_speed = 0.3
enemy_speed = initial_enemy_speed
total_invaders = len(invaders)
enemy_drop = 18

running = True

# ============ GAME LOOP =================
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # -------- LEFT / RIGHT MOVING + DROPPING --------
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
        enemy_bullets.append(Bullet(bx, by, 6, (255, 20, 20)))
        last_enemy_shot = now
    
    # -------- UPDATE ENEMY BULLETS --------
    for b in enemy_bullets[:]:
        b.update()
        if b.y > HEIGHT:
            enemy_bullets.remove(b)

    # ====== DRAW SECTION ======
    screen.fill((10,10,20))

    for inv in invaders:
        inv.update()
        inv.draw(screen)
    
    for b in enemy_bullets:
        b.draw(screen)
    
    pygame.display.update()

pygame.quit()
sys.exit()
