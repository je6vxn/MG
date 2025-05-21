import pygame
import os
import random

pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Character Animation")

# Load background
background = pygame.image.load("f5.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Font setup
font = pygame.font.SysFont("Arial", 24)

# Load images
def load_images(filenames, scale=(120, 120)):
    images = []
    for filename in filenames:
        if os.path.exists(filename):
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, scale)
            images.append(img)
    return images

left_walk_frames = load_images(["l1.JPG", "l2.JPG"])
right_walk_frames = load_images(["r1.JPG", "r2.JPG"])
transformation_frames = load_images([f"t{i}.JPG" for i in range(1, 20)])
attack_frames = load_images([f"k{i}.JPG" for i in range(1, 7)])
jump_frames = load_images([f"j{i}.JPG" for i in range(1, 7)])
power_img = pygame.image.load("a.JPG")
power_img = pygame.transform.scale(power_img, (50, 50))
enemy_img = pygame.image.load("e.jpg")
enemy_img = pygame.transform.scale(enemy_img, (120, 120))

# Constants
WALK_FRAME_DELAY = 150
JUMP_FRAME_DELAY = 80
ANIM_FRAME_DELAY = 80
GRAVITY = 0.6
JUMP_VELOCITY = -12
WALK_SPEED = 5
GROUND_Y = SCREEN_HEIGHT - 120
ENEMY_SPAWN_INTERVAL = 2000

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Power:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10
        self.active = True

    def update(self):
        self.x += self.speed if self.direction == 'right' else -self.speed
        if self.x > SCREEN_WIDTH or self.x < -50:
            self.active = False

    def draw(self, surface):
        img = pygame.transform.flip(power_img, True, False) if self.direction == 'left' else power_img
        surface.blit(img, (self.x, self.y))

class Enemy:
    def __init__(self):
        self.y = GROUND_Y
        self.speed = random.randint(1, 2)
        self.direction = random.choice(['left', 'right'])
        self.active = True
        self.x = SCREEN_WIDTH if self.direction == 'left' else -80

    def update(self):
        if self.direction == 'left':
            self.x -= self.speed
        else:
            self.x += self.speed

    def draw(self, surface):
        img = pygame.transform.flip(enemy_img, True, False) if self.direction == 'left' else enemy_img
        surface.blit(img, (self.x, self.y))

def reset_game():
    global x_pos, y_pos, velocity_y, is_jumping, is_attacking, direction
    global frame_index, last_anim_update, walking_left, walking_right
    global walk_frame_index, last_walk_update, powers, enemies, enemy_spawn_timer
    global score, game_state

    x_pos = SCREEN_WIDTH // 2 - 60
    y_pos = GROUND_Y
    velocity_y = 0
    is_jumping = False
    is_attacking = False
    direction = 'right'
    frame_index = 0
    last_anim_update = pygame.time.get_ticks()
    walking_left = False
    walking_right = False
    walk_frame_index = 0
    last_walk_update = pygame.time.get_ticks()
    powers = []
    enemies = []
    enemy_spawn_timer = pygame.time.get_ticks()
    score = 0
    game_state = 'start'

# Game state
reset_game()
current_static_image = transformation_frames[-1] if transformation_frames else None
start_button = Button("Start", 250, 140, 100, 40)
pause_button = Button("Pause", 500, 10, 80, 30)
restart_button = Button("Restart", 250, 200, 100, 40)

running = True
clock = pygame.time.Clock()

while running:
    now = pygame.time.get_ticks()
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 'start' and start_button.is_clicked(event.pos):
                game_state = 'playing'
            elif game_state == 'gameover' and restart_button.is_clicked(event.pos):
                reset_game()
            elif game_state == 'playing' and pause_button.is_clicked(event.pos):
                game_state = 'paused'
            elif game_state == 'paused' and pause_button.is_clicked(event.pos):
                game_state = 'playing'

        if event.type == pygame.KEYDOWN and game_state == 'playing':
            if event.key == pygame.K_LEFT:
                walking_left = True
                direction = 'left'
            elif event.key == pygame.K_RIGHT:
                walking_right = True
                direction = 'right'
            elif event.key == pygame.K_k and not (is_jumping or is_attacking):
                is_attacking = True
                frame_index = 0
                last_anim_update = now
            elif event.key == pygame.K_SPACE and not is_jumping and y_pos == GROUND_Y:
                is_jumping = True
                velocity_y = JUMP_VELOCITY
                frame_index = 0
                last_anim_update = now

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                walking_left = False
            elif event.key == pygame.K_RIGHT:
                walking_right = False

    if game_state == 'start':
        start_button.draw(screen)

    elif game_state == 'playing':
        pause_button.draw(screen)

        if is_jumping:
            y_pos += velocity_y
            velocity_y += GRAVITY
            if y_pos >= GROUND_Y:
                y_pos = GROUND_Y
                velocity_y = 0
                is_jumping = False

        if is_attacking:
            if now - last_anim_update > ANIM_FRAME_DELAY:
                last_anim_update = now
                frame_index += 1
                if frame_index == 5:
                    px = x_pos + 70 if direction == 'right' else x_pos - 10
                    py = y_pos + 40
                    powers.append(Power(px, py, direction))
                if frame_index >= len(attack_frames):
                    is_attacking = False
                    frame_index = 0
            img = attack_frames[min(frame_index, len(attack_frames) - 1)]
            if direction == 'left':
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (x_pos, y_pos))

        elif is_jumping:
            if now - last_anim_update > JUMP_FRAME_DELAY:
                last_anim_update = now
                frame_index = (frame_index + 1) % len(jump_frames)
            img = jump_frames[frame_index]
            if direction == 'left':
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (x_pos, y_pos))

        elif walking_left or walking_right:
            if now - last_walk_update > WALK_FRAME_DELAY:
                last_walk_update = now
                walk_frame_index = 1 if walk_frame_index == 0 else 1
            if walking_left:
                img = left_walk_frames[walk_frame_index]
                screen.blit(img, (x_pos, y_pos))
                x_pos = max(0, x_pos - WALK_SPEED)
            elif walking_right:
                img = right_walk_frames[walk_frame_index]
                screen.blit(img, (x_pos, y_pos))
                x_pos = min(SCREEN_WIDTH - 120, x_pos + WALK_SPEED)
        else:
            img = current_static_image
            if img:
                if direction == 'left':
                    img = pygame.transform.flip(img, True, False)
                screen.blit(img, (x_pos, y_pos))

        for power in powers:
            power.update()
            power.draw(screen)
        powers = [p for p in powers if p.active]

        if now - enemy_spawn_timer > ENEMY_SPAWN_INTERVAL:
            enemies.append(Enemy())
            enemy_spawn_timer = now

        hero_rect = pygame.Rect(x_pos, y_pos, 120, 120)
        new_enemies = []
        for enemy in enemies:
            enemy.update()
            enemy_rect = pygame.Rect(enemy.x, enemy.y, 120, 120)

            if hero_rect.colliderect(enemy_rect):
                game_state = 'gameover'
                break

            hit = False
            for power in powers:
                power_rect = pygame.Rect(power.x, power.y, 50, 50)
                if power_rect.colliderect(enemy_rect):
                    power.active = False
                    hit = True
                    score += 10
                    break
            if not hit:
                enemy.draw(screen)
                new_enemies.append(enemy)
        enemies = new_enemies

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    elif game_state == 'paused':
        pause_button.draw(screen)
        pause_text = font.render("Paused", True, (255, 255, 255))
        screen.blit(pause_text, (250, 140))

    elif game_state == 'gameover':
        game_over_text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
        screen.blit(game_over_text, (180, 140))
        restart_button.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
