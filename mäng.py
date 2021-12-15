import pygame

# Initializing pygame
pygame.init()

# Classes


class Player:
    def __init__(self, stop_img, right_img, left_img, mid_bottom, fps):
        self.img_list = [left_img, stop_img, right_img]
        self.index = 0
        self.rect = stop_img.get_rect(midbottom = mid_bottom)
        self.direction = "right"
        self.timer = fps // 6

    def draw(self, window):
        window.blit(self.img_list[self.index], self.rect)

    def flip(self):
        new_list = []
        for img in self.img_list:
            img = pygame.transform.flip(img, True, False)
            new_list.append(img)
        self.direction = "left" if self.direction == "right" else "right"
        self.img_list = new_list.copy()

    def walk(self, fps):
        if not self.timer:
            self.timer = fps // 6
            self.index += 1 if self.index != 2 else -2
        self.timer -= 1


class Level:
    def __init__(self, level):
        self.level = level


# Creating screen
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Game variables
gravity = 0.2
clock = pygame.time.Clock()
FPS = 90
RUN = True
platform = pygame.image.load("platform.png")
player_vel = 3
player_walk1 = pygame.image.load("player.png")
player_walk2 = pygame.image.load("player2.png")
player_walk3 = pygame.image.load("player3.png")
player = Player(player_walk1, player_walk3, player_walk2, (WIDTH // 2, HEIGHT), FPS)
background_img = pygame.image.load("bg.jpg")
background_img = pygame.transform.scale(background_img, (int(background_img.get_width() * 1.7), int(background_img.get_height() * 1.7)))
jumping = False

# Game loop

while RUN:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gravity = -7
                jumping = True

    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT]:
        if player.direction == "left":
            player.flip()
        if player.rect.right < WIDTH - player_vel:
            if not jumping:
                player.walk(FPS)
            player.rect.x += player_vel
        else:
            player.index = 0
    if key[pygame.K_LEFT]:
        if player.direction == "right":
            player.flip()
        if player.rect.left > player_vel:
            if not jumping:
                player.walk(FPS)
            player.rect.x -= player_vel
        else:
            player.index = 0
    if not (key[pygame.K_LEFT] or key[pygame.K_RIGHT]):
        player.index = 0
    if player.rect.bottom >= HEIGHT + 1:
        jumping = False
        gravity = 0
        player.rect.bottom = HEIGHT
    player.rect.y += gravity
    gravity += 0.2
    WIN.fill((255, 255, 255))
    WIN.blit(background_img, (0, 0))
    player.draw(WIN)
    pygame.display.flip()
pygame.quit()