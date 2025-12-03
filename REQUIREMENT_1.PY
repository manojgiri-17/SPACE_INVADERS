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

    # ====== DRAW SECTION ======
    screen.fill((10,10,20))

    for inv in invaders:
        inv.update()
        inv.draw(screen)
    
    pygame.display.update()

pygame.quit()
sys.exit()
