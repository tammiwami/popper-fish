import pygame
import time
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import math
from enum import Enum

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 500

PLAYER_WIDTH, PLAYER_HEIGHT = 100, 80
FISH1_WIDTH, FISH1_HEIGHT = 40, 30
FISH2_WIDTH, FISH2_HEIGHT = 70, 55
FISH3_WIDTH, FISH3_HEIGHT = 100, 80
BULLET_WIDTH, BULLET_HEIGHT = 40, 50
PEARL_WIDTH, PEARL_HEIGHT = 33, 33
SHELL_WIDTH, SHELL_HEIGHT = 120, 90
SEAWEED_WIDTH, SEAWEED_HEIGHT = 60, 80
ALGAE_WIDTH, ALGAE_HEIGHT = 38, 32

PLAYER_VELOCITY = 6
FISH_VELOCITY = 3
BULLET_VELOCITY = 12
POWERUP_VELOCITY = 2
PLAYER_MAX_HEALTH = 100

# UI Constants
UI_FONT = pygame.font.SysFont("Arial", 24, bold=True)
TITLE_FONT = pygame.font.SysFont("Arial", 40, bold=True)
OCEAN_FONT = pygame.font.SysFont("Arial", 32, bold=True, italic=True)
UI_PADDING = 15
UI_BG_COLOR = (0, 20, 40, 180)  
UI_BORDER_COLOR = (0, 150, 200) 
HEALTH_COLOR = (255, 50, 50)
ATTACK_BOOST_COLOR = (255, 215, 0)
TEXT_COLOR = (200, 240, 255)  
BUBBLE_COLOR = (200, 240, 255, 100)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Popper Fish")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

class FishType(Enum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3

class PowerUpType(Enum):
    PEARL = 1
    SHELL = 2
    SEAWEED = 3
    ALGAE = 4

def load_image(name, width, height, default_color=None):
    try:
        image = pygame.image.load(f"assets/images/{name}.png")
        return pygame.transform.scale(image, (width, height))
    except:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if default_color:
            surface.fill(default_color)
        return surface


def create_bubble_surface(radius):
    bubble = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(bubble, BUBBLE_COLOR, (radius, radius), radius)
    pygame.draw.circle(bubble, (255, 255, 255, 50), (radius, radius), radius, 1)
    return bubble

BUBBLE_SMALL = create_bubble_surface(5)
BUBBLE_MEDIUM = create_bubble_surface(10)
BUBBLE_LARGE = create_bubble_surface(15)

try:
    BG = pygame.transform.scale(pygame.image.load("assets/images/orig.png"), (WIDTH, HEIGHT))
except:
    BG = pygame.Surface((WIDTH, HEIGHT))
    BG.fill((0, 100, 200))

player_img = load_image("player", PLAYER_WIDTH, PLAYER_HEIGHT, RED)
fish_images = {
    FishType.TYPE1: load_image("fish1", FISH1_WIDTH, FISH1_HEIGHT, BLUE),
    FishType.TYPE2: load_image("fish2", FISH2_WIDTH, FISH2_HEIGHT, GREEN),
    FishType.TYPE3: load_image("fish3", FISH3_WIDTH, FISH3_HEIGHT, PURPLE)
}
bullet_img = load_image("bullet", BULLET_WIDTH, BULLET_HEIGHT, YELLOW)
powerup_images = {
    PowerUpType.PEARL: load_image("pearl", PEARL_WIDTH, PEARL_HEIGHT, WHITE),
    PowerUpType.SHELL: load_image("shell", SHELL_WIDTH, SHELL_HEIGHT, ORANGE),
    PowerUpType.SEAWEED: load_image("seaweed", SEAWEED_WIDTH, SEAWEED_HEIGHT, GREEN),
    PowerUpType.ALGAE: load_image("algae", ALGAE_WIDTH, ALGAE_HEIGHT, CYAN)
}
powerup_sizes = {
    PowerUpType.PEARL: (PEARL_WIDTH, PEARL_HEIGHT),
    PowerUpType.SHELL: (SHELL_WIDTH, SHELL_HEIGHT),
    PowerUpType.SEAWEED: (SEAWEED_WIDTH, SEAWEED_HEIGHT),
    PowerUpType.ALGAE: (ALGAE_WIDTH, ALGAE_HEIGHT)
}

class Fish:
    def __init__(self, x, y, fish_type):
        self.type = fish_type
        self.health = self.type.value
        sizes = {
            FishType.TYPE1: (FISH1_WIDTH, FISH1_HEIGHT),
            FishType.TYPE2: (FISH2_WIDTH, FISH2_HEIGHT),
            FishType.TYPE3: (FISH3_WIDTH, FISH3_HEIGHT)
        }
        width, height = sizes[self.type]
        self.rect = pygame.Rect(x, y, width, height)
        self.image = fish_images[self.type]
        if random.random() > 0.5:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image_rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.y += FISH_VELOCITY
        self.image_rect.center = self.rect.center

class PowerUp:
    def __init__(self, x, y):
        self.type = random.choice(list(PowerUpType))
        width, height = powerup_sizes[self.type]
        self.rect = pygame.Rect(x, y, width, height)
        self.image = powerup_images[self.type]
        self.image_rect = self.image.get_rect(center=self.rect.center)
    
    def update(self):
        self.rect.y += POWERUP_VELOCITY
        self.image_rect.center = self.rect.center

def draw_ui_panel(surface, x, y, width, height):
    panel = pygame.Surface((width, height), pygame.SRCALPHA)
    
    
    for i in range(height):
        alpha = 180 - int(100 * (i/height))
        color = (0, 20 + int(30 * (i/height)), 40 + int(60 * (i/height)), alpha)
        pygame.draw.line(panel, color, (0, i), (width, i))
    
    
    border_points = []
    wave_height = 5
    for i in range(0, width + 1, 10):
        progress = i / width
        offset = wave_height * math.sin(progress * math.pi * 4)
        border_points.append((i, offset))
    
    
    border_points.append((width, height))
    border_points.append((0, height))
    
    if len(border_points) > 2:
        pygame.draw.polygon(panel, UI_BORDER_COLOR + (100,), border_points, 0)
        pygame.draw.lines(panel, UI_BORDER_COLOR, False, border_points[:-2], 2)
    
    
    panel.blit(BUBBLE_SMALL, (10, 15))
    panel.blit(BUBBLE_MEDIUM, (width - 25, 30))
    panel.blit(BUBBLE_SMALL, (width - 15, 10))
    
    surface.blit(panel, (x, y))

def draw_health_bar(surface, x, y, current, max_health, width, height):
    ratio = current / max_health
    
    
    for i in range(int(width * ratio)):
        
        if i < width * 0.3:
            r = 255
            g = int(255 * (i / (width * 0.3)))
            b = 0
        elif i < width * 0.6:
            r = int(255 * (1 - (i - width*0.3) / (width*0.3)))
            g = 255
            b = int(255 * (i - width*0.3) / (width*0.3))
        else:
            r = 0
            g = int(255 * (1 - (i - width*0.6) / (width*0.4)))
            b = 255
        
        
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        pygame.draw.rect(surface, (r, g, b), (x + i, y, 1, height))
    
   
    border_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, UI_BORDER_COLOR, border_rect, 2, border_radius=3)
    
    
    if current > 0:
        bubble_pos = x + int(width * ratio) - 5
        surface.blit(BUBBLE_SMALL, (bubble_pos, y - 3)) 

def draw_attack_timer(surface, x, y, width, height, timer, max_time):
    if timer > 0:
        ratio = timer / max_time
        
        for i in range(int(width * ratio)):
            intensity = 150 + int(105 * (i / (width * ratio)))
            pygame.draw.rect(surface, (intensity, intensity//2, 0), (x + i, y, 1, height))
        
       
        if random.random() < 0.1:
            sparkle_x = x + random.randint(0, int(width * ratio))
            sparkle_y = y + random.randint(0, height)
            pygame.draw.rect(surface, (255, 255, 255), (sparkle_x, sparkle_y, 2, 2))
        
        pygame.draw.rect(surface, (255, 200, 0), (x, y, int(width * ratio), height), border_radius=3)
        pygame.draw.rect(surface, UI_BORDER_COLOR, (x, y, width, height), 2, border_radius=3)

def draw_score_popup(surface, x, y, score, alpha):
    if alpha > 0:
        
        bubble = pygame.Surface((60, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(bubble, (0, 100, 150, alpha//2), (0, 0, 60, 30))
        pygame.draw.ellipse(bubble, (0, 200, 255, alpha//3), (0, 0, 60, 30), 2)
        bubble.set_alpha(alpha)
        surface.blit(bubble, (x - 30, y - 15))
        
        text = UI_FONT.render(f"+{score}", True, (255, 255, 255))
        text.set_alpha(alpha)
        surface.blit(text, (x - text.get_width()//2, y - text.get_height()//2))

def draw_game_over_screen(surface, score):
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
   
    for y in range(HEIGHT):
        depth = y / HEIGHT
        r = int(10 * depth)
        g = int(50 * depth)
        b = int(100 + 100 * depth)
        a = int(200 + 50 * depth)
        pygame.draw.line(overlay, (r, g, b, a), (0, y), (WIDTH, y))
    
    
    for wave_y in [HEIGHT//3, HEIGHT//2, HEIGHT//3*2]:
        for x in range(0, WIDTH, 5):
            offset = 5 * math.sin(x / 50 + time.time())
            pygame.draw.line(overlay, (0, 150, 200, 50), 
                           (x, wave_y + offset), (x + 5, wave_y + offset + 2), 2)
    
   
    for _ in range(20):
        bubble_x = random.randint(0, WIDTH)
        bubble_y = random.randint(0, HEIGHT)
        size = random.choice([BUBBLE_SMALL, BUBBLE_MEDIUM, BUBBLE_LARGE])
        overlay.blit(size, (bubble_x, bubble_y))
    
    surface.blit(overlay, (0, 0))
    
    
    panel_width, panel_height = 500, 300
    panel_x, panel_y = WIDTH//2 - panel_width//2, HEIGHT//2 - panel_height//2
    draw_ui_panel(surface, panel_x, panel_y, panel_width, panel_height)
    
   
    game_over_text = TITLE_FONT.render("GAME OVER", True, (255, 100, 100))
    text_x = WIDTH//2 - game_over_text.get_width()//2
    text_y = HEIGHT//2 - 80
    
    
    for i in range(0, game_over_text.get_width(), 2):
        offset = 3 * math.sin(i / 20 + time.time() * 2)
        surface.blit(game_over_text.subsurface((i, 0, 2, game_over_text.get_height())), 
                   (text_x + i, text_y + offset))
    
    
    score_text = OCEAN_FONT.render(f"Your Score: {score}", True, TEXT_COLOR)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    
    bubble_size = max(score_text.get_width() + 40, score_text.get_height() + 30)
    bubble = pygame.Surface((bubble_size, bubble_size), pygame.SRCALPHA)
    pygame.draw.ellipse(bubble, (0, 50, 100, 150), (0, 0, bubble_size, bubble_size))
    pygame.draw.ellipse(bubble, (0, 150, 200, 100), (0, 0, bubble_size, bubble_size), 3)
    surface.blit(bubble, (WIDTH//2 - bubble_size//2, HEIGHT//2 - bubble_size//2 + 10))
    
    surface.blit(score_text, score_rect)
    
    
    pulse = int(10 * abs(math.sin(time.time() * 2)))
    restart_text = UI_FONT.render("Press any key to quit", True, 
                                (200 + pulse, 240 + pulse, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
    surface.blit(restart_text, restart_rect)
    
    
    fish_silhouette = pygame.Surface((100, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(fish_silhouette, (0, 50, 100, 50), (0, 0, 80, 40))
    pygame.draw.polygon(fish_silhouette, (0, 50, 100, 50), 
                       [(80, 20), (100, 10), (100, 30)])
    
    
    left_fish = pygame.transform.flip(fish_silhouette, True, False)
    surface.blit(left_fish, (panel_x - 120, panel_y + 50))
    
    
    surface.blit(fish_silhouette, (panel_x + panel_width + 20, panel_y + 100))

def draw(surface, player, elapsed_time, fishes, bullets, powerups, score, player_health, attack_power, attack_timer, score_popups):
    surface.blit(BG, (0, 0))
    
    
    surface.blit(player_img, player)
    for fish in fishes:
        surface.blit(fish.image, fish.image_rect)
    for bullet in bullets:
        rotated_bullet = pygame.transform.rotate(bullet_img, 0)
        surface.blit(rotated_bullet, rotated_bullet.get_rect(center=bullet.center))
    for powerup in powerups:
        surface.blit(powerup.image, powerup.image_rect)
    
    
    draw_ui_panel(surface, 10, 10, 250, 120)
    
    
    time_text = UI_FONT.render(f"TIME: {round(elapsed_time)}s", True, TEXT_COLOR)
    score_text = UI_FONT.render(f"SCORE: {score}", True, TEXT_COLOR)
    health_text = UI_FONT.render("HEALTH:", True, TEXT_COLOR)
    attack_text = UI_FONT.render(f"ATTACK: {attack_power}x", True, 
                               ATTACK_BOOST_COLOR if attack_power > 1 else TEXT_COLOR)
    
    surface.blit(time_text, (25, 15))
    surface.blit(score_text, (25, 40))
    surface.blit(health_text, (25, 65))
    surface.blit(attack_text, (25, 90))
    
    
    draw_health_bar(surface, 130, 70, player_health, PLAYER_MAX_HEALTH, 120, 16)
    draw_attack_timer(surface, 150, 115, 150, 10, attack_timer, 5000)
    
    
    for popup in score_popups[:]:
        draw_score_popup(surface, popup['x'], popup['y'], popup['score'], popup['alpha'])
        popup['y'] -= 1
        popup['alpha'] -= 3
        if popup['alpha'] <= 0:
            score_popups.remove(popup)
    
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    start_time = time.time()
    
    
    score = 0
    player_health = PLAYER_MAX_HEALTH
    attack_power = 1
    attack_timer = 0
    score_popups = []
    
    
    fish_add_increment = 2000
    fish_count = 0
    powerup_add_increment = 5000
    powerup_count = 0
    
    
    fishes = []
    bullets = []
    powerups = []
    player = pygame.Rect(WIDTH//2, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    running = True
    while running:
        delta_time = clock.tick(60)
        fish_count += delta_time
        powerup_count += delta_time
        elapsed_time = time.time() - start_time
        
        
        if attack_timer > 0:
            attack_timer -= delta_time
            if attack_timer <= 0:
                attack_power = 1

        
        if fish_count >= fish_add_increment:
            for _ in range(3):
                fish_type = random.choice(list(FishType))
                width, height = {
                    FishType.TYPE1: (FISH1_WIDTH, FISH1_HEIGHT),
                    FishType.TYPE2: (FISH2_WIDTH, FISH2_HEIGHT),
                    FishType.TYPE3: (FISH3_WIDTH, FISH3_HEIGHT)
                }[fish_type]
                fish_x = random.randint(0, WIDTH - width)
                fishes.append(Fish(fish_x, -height, fish_type))
            
            fish_add_increment = max(1000, fish_add_increment - 50)
            fish_count = 0

        
        if powerup_count >= powerup_add_increment:
            powerup_type = random.choice(list(PowerUpType))
            width, height = powerup_sizes[powerup_type]
            powerup_x = random.randint(0, WIDTH - width)
            powerups.append(PowerUp(powerup_x, -height))
            powerup_count = 0

       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = pygame.Rect(
                    player.x + PLAYER_WIDTH//2 - BULLET_WIDTH//2,
                    player.y,
                    BULLET_WIDTH,
                    BULLET_HEIGHT
                )
                bullets.append(bullet)

      
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_d] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

       
        for bullet in bullets[:]:
            bullet.y -= BULLET_VELOCITY
            if bullet.y < 0:
                bullets.remove(bullet)

        
        for fish in fishes[:]:
            fish.update()
            if fish.rect.y > HEIGHT:
                fishes.remove(fish)

        
        for powerup in powerups[:]:
            powerup.update()
            if powerup.rect.y > HEIGHT:
                powerups.remove(powerup)

        
        for bullet in bullets[:]:
            for fish in fishes[:]:
                if bullet.colliderect(fish.rect):
                    fish.health -= attack_power
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if fish.health <= 0:
                        score_gain = fish.type.value * 10
                        score += score_gain
                        score_popups.append({
                            'x': fish.rect.centerx,
                            'y': fish.rect.centery,
                            'score': score_gain,
                            'alpha': 255
                        })
                        fishes.remove(fish)
                    break

        
        for fish in fishes[:]:
            if fish.rect.colliderect(player):
                fishes.remove(fish)
                player_health -= 10 * fish.type.value
                if player_health <= 0:
                    running = False

       
        for powerup in powerups[:]:
            if powerup.rect.colliderect(player):
                powerups.remove(powerup)
                if powerup.type in [PowerUpType.PEARL, PowerUpType.SHELL]:
                    attack_power = 2
                    attack_timer = 5000
                elif powerup.type in [PowerUpType.SEAWEED, PowerUpType.ALGAE]:
                    player_health = min(PLAYER_MAX_HEALTH, player_health + 20)

    
        draw(WIN, player, elapsed_time, fishes, bullets, powerups, score, 
            player_health, attack_power, attack_timer, score_popups)

  
    draw_game_over_screen(WIN, score)
    pygame.display.update()
    
 
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
       
        draw_game_over_screen(WIN, score)
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()