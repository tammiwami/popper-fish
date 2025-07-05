import pygame
import time
import random
pygame.font.init()


pygame.init()


WIDTH, HEIGHT = 1200, 700
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5
FONT = pygame.font.SysFont("comicsans", 30)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Popper Fish")


BG = pygame.transform.scale(pygame.image.load("assets/images/bg.png"), (WIDTH, HEIGHT))


def draw(player, elapsed_time):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {int(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, "red", player)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    while run:
        clock.tick(60) 
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >=0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame .K_RIGHT] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        draw(player, elapsed_time)

    pygame.quit()

if __name__ == "__main__":
    main()
