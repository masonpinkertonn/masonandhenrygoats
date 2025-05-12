import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

running = True
clock = pygame.time.Clock()

myrect1 = pygame.Rect(0,0,50,50)
myrect2 = pygame.Rect(0,100,50,50)

while running:
    screen.fill((0,0,0))

    pygame.draw.rect(screen, "red", myrect1)
    pygame.draw.rect(screen, "red", myrect2)

    distance = pygame.Vector2(myrect1.center).distance_to(pygame.Vector2(myrect2.center))

    print(distance)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    key = pygame.key.get_pressed()

    if key[pygame.K_w] and distance >= 0:
        myrect2.y -= distance

    pygame.display.flip()
    clock.tick(60)