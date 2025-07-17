import pygame
import sys
from game.constants import WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VELOCITY, BULLET_WIDTH, BULLET_HEIGHT
from game.ui import draw, draw_game_over_screen
from game.game_state import GameState
from utils.helpers import load_assets

def main():
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    
    # Set up display
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Popper Fish")
    
    # Load assets
    assets = load_assets()
    
    # Initialize game state
    game_state = GameState()
    clock = pygame.time.Clock()
    
    # Create player rectangle
    player = pygame.Rect(WIDTH//2, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    # Main game loop
    while game_state.running:
        delta_time = clock.tick(60)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = pygame.Rect(
                    player.x + PLAYER_WIDTH//2 - BULLET_WIDTH//2,
                    player.y,
                    BULLET_WIDTH,
                    BULLET_HEIGHT
                )
                game_state.bullets.append(bullet)
        
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_d] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY
        
        # Update game state
        game_state.update_attack_power(delta_time)
        game_state.spawn_fish(assets['fish_images'])
        game_state.spawn_powerups(assets['powerup_images'])
        game_state.update_bullets()
        game_state.update_entities()
        game_state.check_collisions(player)  # Pass player to check collisions
        game_state.update_score_popups()
        
        # Draw everything
        draw(WIN, assets['bg'], player, assets['player_img'], 
            game_state.get_elapsed_time(), game_state.fishes, game_state.bullets, 
            assets['bullet_img'], game_state.powerups, game_state.score, 
            game_state.player_health, game_state.attack_power, 
            game_state.attack_timer, game_state.score_popups)
    
    # Game over screen
    draw_game_over_screen(WIN, game_state.score, WIDTH, HEIGHT)
    pygame.display.update()
    
    # Wait for user to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()