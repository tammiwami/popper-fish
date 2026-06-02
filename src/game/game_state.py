import random
import time

import pygame

from src.entities.fish import Fish, FishType
from src.entities.powerup import PowerUp, PowerUpType
from src.game.constants import (
    ATTACK_MAX_POWER,
    ATTACK_POWER_GAIN,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    BULLET_HEIGHT,
    BULLET_VELOCITY,
    BULLET_WIDTH,
    FISH_SIZES,
    HEIGHT,
    PLAYER_HEIGHT,
    PLAYER_MAX_HEALTH,
    PLAYER_VELOCITY,
    PLAYER_WIDTH,
    POWERUP_SIZES,
    WIDTH,
)
from src.game.ui import Button, draw, draw_start_screen
from src.utils.helpers import set_music_volume


def create_settings_controls():
    field_width = 520
    field_x = WIDTH // 2 - field_width // 2
    volume_width = 255
    return {
        "left": pygame.Rect(field_x, HEIGHT // 2 - 47, field_width, 38),
        "right": pygame.Rect(field_x, HEIGHT // 2 + 1, field_width, 38),
        "shoot": pygame.Rect(field_x, HEIGHT // 2 + 49, field_width, 38),
        "volume": pygame.Rect(WIDTH // 2 - 72, HEIGHT // 2 + 112, volume_width, 18),
        "save": Button(
            WIDTH // 2 - 35,
            HEIGHT // 2 - 80,
            70,
            25,
            "Save",
            BUTTON_COLOR,
            BUTTON_HOVER_COLOR,
            BUTTON_TEXT_COLOR,
            small=True,
        ),
    }


def handle_settings_click(mouse_pos, mouse_clicked, settings, controls):
    if not mouse_clicked:
        return None

    for action in ("left", "right", "shoot"):
        if controls[action].collidepoint(mouse_pos):
            return action

    if controls["volume"].collidepoint(mouse_pos):
        settings["volume"] = round(
            max(0, min(
                (mouse_pos[0] - controls["volume"].left) / controls["volume"].width, 1)),
            2,
        )
        set_music_volume(settings["volume"])
        return "changed"

    return None


def pause_for_menu(window, assets, clock, settings):
    button_gap = 52
    resume_width = 180
    settings_width = 210
    button_y = HEIGHT // 2 + 155
    group_x = WIDTH // 2 - (resume_width + button_gap + settings_width) // 2
    resume_button = Button(
        group_x,
        button_y,
        resume_width,
        50,
        "Resume",
        BUTTON_COLOR,
        BUTTON_HOVER_COLOR,
        BUTTON_TEXT_COLOR,
    )
    settings_button = Button(
        group_x + resume_width + button_gap,
        button_y,
        settings_width,
        50,
        "Settings",
        BUTTON_COLOR,
        BUTTON_HOVER_COLOR,
        BUTTON_TEXT_COLOR,
    )
    controls = create_settings_controls()
    active_binding = None
    show_settings = False
    has_unsaved_changes = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if active_binding:
                    settings[active_binding] = event.key
                    active_binding = None
                    has_unsaved_changes = True
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        resume_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        if show_settings:
            controls["save"].check_hover(mouse_pos)
        if resume_button.is_clicked(mouse_pos, mouse_clicked):
            return True
        if settings_button.is_clicked(mouse_pos, mouse_clicked):
            show_settings = not show_settings
            active_binding = None
        if show_settings and has_unsaved_changes and controls["save"].is_clicked(mouse_pos, mouse_clicked):
            has_unsaved_changes = False

        if show_settings:
            new_binding = handle_settings_click(
                mouse_pos, mouse_clicked, settings, controls)
            if new_binding in ("left", "right", "shoot"):
                active_binding = new_binding
            elif new_binding == "changed":
                has_unsaved_changes = True

        draw_start_screen(
            window,
            assets,
            resume_button,
            settings_button,
            settings,
            controls,
            active_binding,
            show_settings,
            has_unsaved_changes,
        )
        clock.tick(60)


def game_loop(window, assets, settings):
    clock = pygame.time.Clock()
    start_time = time.time()

    score = 0
    player_health = PLAYER_MAX_HEALTH
    attack_power = 1
    attack_timer = 0
    score_popups = []
    # floating bubbles that appear occasionally during gameplay
    floating_bubbles = []
    bubble_spawn_timer = 0
    next_bubble_spawn = random.randint(800, 2200)

    fish_add_increment = 2000
    fish_count = 0
    powerup_add_increment = 5000
    powerup_count = 0

    fishes = []
    bullets = []
    powerups = []
    player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_HEIGHT -
                         10, PLAYER_WIDTH, PLAYER_HEIGHT)
    menu_button = Button(
        WIDTH - 94,
        15,
        74,
        29,
        "Menu",
        BUTTON_COLOR,
        BUTTON_HOVER_COLOR,
        BUTTON_TEXT_COLOR,
        menu=True,
    )

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
                width, height = FISH_SIZES[fish_type.value]
                fish_x = random.randint(0, WIDTH - width)
                fishes.append(Fish(fish_x, -height, fish_type,
                              assets["fish"][fish_type]))

            fish_add_increment = max(1000, fish_add_increment - 50)
            fish_count = 0

        if powerup_count >= powerup_add_increment:
            powerup_type = random.choice(list(PowerUpType))
            width, height = POWERUP_SIZES[powerup_type.value]
            powerup_x = random.randint(0, WIDTH - width)
            powerups.append(PowerUp(powerup_x, -height,
                            powerup_type, assets["powerups"][powerup_type]))
            powerup_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, score
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if menu_button.is_clicked(pygame.mouse.get_pos(), True):
                    pause_started = time.time()
                    should_resume = pause_for_menu(
                        window, assets, clock, settings)
                    start_time += time.time() - pause_started
                    if not should_resume:
                        return False, score
                    continue
            if event.type == pygame.KEYDOWN and event.key == settings["shoot"]:
                bullet = pygame.Rect(
                    player.x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2,
                    player.y,
                    BULLET_WIDTH,
                    BULLET_HEIGHT,
                )
                bullets.append(bullet)

        keys = pygame.key.get_pressed()
        if keys[settings["left"]] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[settings["right"]] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        menu_button.check_hover(pygame.mouse.get_pos())

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
                        score_popups.append(
                            {
                                "x": fish.rect.centerx,
                                "y": fish.rect.centery,
                                "score": score_gain,
                                "alpha": 255,
                            }
                        )
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
                    attack_power = min(
                        ATTACK_MAX_POWER, attack_power + ATTACK_POWER_GAIN)
                    # Set attack duration to 12 seconds (12000 ms)
                    attack_timer = 12000
                elif powerup.type in [PowerUpType.SEAWEED, PowerUpType.ALGAE]:
                    player_health = min(PLAYER_MAX_HEALTH, player_health + 20)

        # Update floating bubbles spawn timer and create occasional bubbles
        bubble_spawn_timer += delta_time
        if bubble_spawn_timer >= next_bubble_spawn:
            bubble_spawn_timer = 0
            next_bubble_spawn = random.randint(800, 2200)
            r = random.choice([5, 7, 9, 12])
            bx = random.randint(20, WIDTH - 20)
            by = HEIGHT + r
            speed = random.uniform(30, 90)  # px per second
            floating_bubbles.append(
                {"x": bx, "y": by, "r": r, "alpha": 200, "speed": speed})

        # Update floating bubbles positions and alpha
        for b in floating_bubbles[:]:
            b["y"] -= b["speed"] * (delta_time / 1000.0)
            b["alpha"] -= int(30 * (delta_time / 1000.0))
            if b["y"] < -b["r"] or b["alpha"] <= 0:
                floating_bubbles.remove(b)

        draw(
            window,
            assets,
            player,
            elapsed_time,
            fishes,
            bullets,
            powerups,
            score,
            player_health,
            attack_power,
            menu_button,
            score_popups,
            floating_bubbles,
        )

    return True, score
