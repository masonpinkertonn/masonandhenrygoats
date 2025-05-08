import pygame
import sys

pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load image
image = pygame.image.load("your_image.png")
image_width, image_height = image.get_size()

# Initial position (fully offscreen left)
x = -image_width
y = (screen_height - image_height) // 2

# Reveal starts here
reveal_x = 100

# Speed
speed = 5

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move image
    x += speed

    # If image is not yet intersecting the reveal zone, do nothing
    if x + image_width > reveal_x:
        # Calculate visible region
        visible_x = max(reveal_x - x, 0)  # how far into the image to start drawing
        visible_width = min(image_width - visible_x, screen_width - x)

        # Only blit the visible portion
        if visible_width > 0:
            visible_part = image.subsurface((visible_x, 0, visible_width, image_height))
            screen.blit(visible_part, (x + visible_x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
