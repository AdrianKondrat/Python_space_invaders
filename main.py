import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders... ish")

clock= pygame.time.Clock()

player_image = pygame.image.load("./assets/spaceship.png").convert_alpha()
enemy_image = pygame.image.load("./assets/invader.png").convert_alpha()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT-50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed = -self.speed
            self.rect.y += 20
    
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

player = Player()
player_group.add(player)

for i in range(10):
    for j in range(4):
        enemy = Enemy(60 + 70 * i, 50 * (j+1))
        enemy_group.add(enemy)

running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullet_group.add(bullet)
    
    player_group.update()
    bullet_group.update()
    enemy_group.update()

    pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)

    player_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
