import pygame
import time
import random
pygame.font.init()


pygame.init()


WIDTH, HEIGHT = 1000, 500
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5
FISH_WIDTH = 10
FISH_HEIGHT = 20
FISH_VELOCITY = 3
FONT = pygame.font.SysFont("comicsans", 30)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Popper Fish")


BG = pygame.transform.scale(pygame.image.load("assets/images/bg.png"), (WIDTH, HEIGHT))


def draw(player, elapsed_time, fishes):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, "red", player)
    

    for fish in fishes:
        pygame.draw.rect(WIN, "blue", fish)

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    fish_add_increment = 2000
    fish_count = 0

    fishes = []
    hit = False

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    while run:
        fish_count += clock.tick(60) 
        elapsed_time = time.time() - start_time

        if fish_count >= fish_add_increment:
            for _ in range(3):
                fish_x = random.randint(0, WIDTH - FISH_WIDTH)
                fish = pygame.Rect(fish_x, -FISH_HEIGHT, FISH_WIDTH, FISH_HEIGHT)
                fishes.append(fish)

            fish_add_increment = max(200, fish_add_increment - 50)
            fish_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_VELOCITY >=0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame .K_d] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        for fish in fishes[:]:
            fish.y += FISH_VELOCITY
            if fish.y > HEIGHT:
                fishes.remove(fish)
            elif fish.y + fish.height >= player.y and fish.colliderect(player):
                fishes.remove(fish)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You got hit by a fish!", 1, "red")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, fishes)

    pygame.quit()

if __name__ == "__main__":
    main()
