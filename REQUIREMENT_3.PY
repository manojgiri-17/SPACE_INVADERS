import pygame, random, sys
pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
FPS = 60

GREEN = (50,220,50)
BG = (6,6,12)

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

barriers = []
gap = WIDTH // 5
for i in range(4):
    bx = gap * (i+1) - 60
    by = HEIGHT - 200
    barriers.append(create_barrier(bx, by))

running = True
timer = 0

while running:
    dt = clock.tick(FPS)
    timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(BG)

    # draw barriers
    for barrier in barriers:
        for block in barrier:
            block.draw(screen)

    pygame.display.flip()