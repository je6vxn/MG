import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Power Animation")

# Load and verify images a1.png to a4.png
power_images = []
for i in range(1, 5):
    filename = f"a{i}.png"
    if not os.path.exists(filename):
        print(f"Error: {filename} not found in directory {os.getcwd()}")
        pygame.quit()
        sys.exit()
    power_images.append(pygame.image.load(filename).convert_alpha())

# Animation variables
power_rect = pygame.Rect(100, HEIGHT // 2, 50, 50)  # starting position
power_frame = 0
frame_delay = 100  # milliseconds per frame
last_update = pygame.time.get_ticks()
power_active = False
direction = None  # 'left' or 'right'

# Clock for frame rate
clock = pygame.time.Clock()

# Main loop
while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Trigger animation based on key combination
    if keys[pygame.K_a] and keys[pygame.K_RIGHT]:
        power_active = True
        direction = "right"
        power_rect.x = 100  # start from left
    elif keys[pygame.K_a] and keys[pygame.K_LEFT]:
        power_active = True
        direction = "left"
        power_rect.x = WIDTH - 100  # start from right

    # Update animation frame
    now = pygame.time.get_ticks()
    if power_active and now - last_update > frame_delay:
        power_frame = (power_frame + 1) % len(power_images)
        last_update = now

        # Move the power effect
        if direction == "right":
            power_rect.x += 10
            if power_rect.x > WIDTH:
                power_active = False
        elif direction == "left":
            power_rect.x -= 10
            if power_rect.x < -50:
                power_active = False

    # Clear screen
    screen.fill((30, 30, 30))

    # Draw animation
    if power_active:
        screen.blit(power_images[power_frame], power_rect)

    # Update display
    pygame.display.flip()
    clock.tick(60)
