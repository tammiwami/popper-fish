import sys
import math

import pygame

from src.game.constants import (
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    HEIGHT,
    WIDTH,
)
from src.game.game_state import game_loop
from src.game.ui import Button, draw_game_over_screen, draw_start_screen, initialize_fonts
from src.utils.helpers import (
    load_assets,
    play_game_over_sound,
    set_music_volume,
    start_background_music,
    stop_background_music,
)


def create_settings():
    return {
        "left": pygame.K_a,
        "right": pygame.K_d,
        "shoot": pygame.K_SPACE,
        "volume": 0.45,
    }


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


def wait_for_start(window, assets, settings):
    button_gap = 52
    start_width = 180
    settings_width = 210
    button_y = HEIGHT // 2 + 155
    group_x = WIDTH // 2 - (start_width + button_gap + settings_width) // 2
    start_button = Button(
        group_x,
        button_y,
        start_width,
        50,
        "Start",
        BUTTON_COLOR,
        BUTTON_HOVER_COLOR,
        BUTTON_TEXT_COLOR,
    )
    settings_button = Button(
        group_x + start_width + button_gap,
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
    clock = pygame.time.Clock()

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
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        start_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        if show_settings:
            controls["save"].check_hover(mouse_pos)
        if start_button.is_clicked(mouse_pos, mouse_clicked):
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
            start_button,
            settings_button,
            settings,
            controls,
            active_binding,
            show_settings,
            has_unsaved_changes,
        )
        clock.tick(60)


def wait_for_logo(window, assets):
    clock = pygame.time.Clock()
    prompt_font = pygame.font.SysFont("Arial", 24, bold=True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return True

        window.blit(assets["bg"], (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 20, 45, 185))
        window.blit(overlay, (0, 0))

        logo = assets["logo"]
        logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 45))
        window.blit(logo, logo_rect)

        prompt = prompt_font.render(
            "Press anywhere to start", True, (255, 255, 255))
        alpha = 80 + \
            int(175 * ((math.sin(pygame.time.get_ticks() / 420) + 1) / 2))
        prompt.set_alpha(alpha)
        prompt_rect = prompt.get_rect(
            center=(WIDTH // 2, logo_rect.bottom + 35))
        window.blit(prompt, prompt_rect)

        pygame.display.update()
        clock.tick(60)


def prompt_player_name(window, assets, max_length=12):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22, bold=True)
    name = ""
    confirm_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 40, 100, 34, "Confirm",
                            BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR)

    blink_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Enter still confirms, but instruction removed from prompt
                    return name.strip() if name.strip() else "You"
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    char = event.unicode
                    if char.isprintable() and len(name) < max_length:
                        name += char
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if confirm_button.is_clicked(mouse_pos, True) and name.strip():
                    return name.strip()

        window.blit(assets["bg"], (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 20, 45, 185))
        window.blit(overlay, (0, 0))

        logo = assets["logo"]
        # Scale logo to fit comfortably on the prompt screen and place near top
        lw, lh = logo.get_size()
        max_logo_height = int(HEIGHT * 0.38)
        max_logo_width = int(WIDTH * 0.9)
        scale = min(max_logo_width / lw, max_logo_height / lh, 1.0)
        if scale < 1.0:
            logo_scaled = pygame.transform.smoothscale(
                logo, (int(lw * scale), int(lh * scale)))
        else:
            logo_scaled = logo
        logo_rect = logo_scaled.get_rect(
            center=(WIDTH // 2, logo_scaled.get_height() // 2 + 24))
        window.blit(logo_scaled, logo_rect)

        prompt = font.render("Enter your name:", True, (255, 255, 255))
        prompt_rect = prompt.get_rect(
            center=(WIDTH // 2, logo_rect.bottom + 20))
        window.blit(prompt, prompt_rect)

        # Input box is centered; Confirm button will be below it
        box_width, box_height = 360, 48
        box_rect = pygame.Rect(
            WIDTH // 2 - box_width // 2, prompt_rect.bottom + 20, box_width, box_height)
        # shadow
        shadow = pygame.Surface(
            (box_rect.width + 6, box_rect.height + 6), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 100),
                         shadow.get_rect(), border_radius=8)
        window.blit(shadow, (box_rect.x - 3, box_rect.y - 3))
        # box
        pygame.draw.rect(window, (6, 36, 48), box_rect, border_radius=8)
        pygame.draw.rect(window, (120, 200, 220), box_rect, 2, border_radius=8)

        # Position Confirm button centered below the input box
        confirm_w = 160
        confirm_h = 40
        confirm_x = box_rect.centerx - confirm_w // 2
        confirm_y = box_rect.bottom + 14
        confirm_button.rect = pygame.Rect(
            confirm_x, confirm_y, confirm_w, confirm_h)

        # blinking caret
        blink_timer += clock.get_time()
        show_caret = (blink_timer // 500) % 2 == 0

        display_text = name or ""
        name_surf = font.render(display_text, True, (230, 245, 250))
        name_pos = (box_rect.x + 14, box_rect.y +
                    (box_height - name_surf.get_height()) // 2)
        window.blit(name_surf, name_pos)
        if show_caret and len(display_text) < max_length:
            caret_x = name_pos[0] + name_surf.get_width() + 3
            caret_y = name_pos[1]
            caret_h = name_surf.get_height()
            pygame.draw.rect(window, (230, 245, 250),
                             (caret_x, caret_y, 2, caret_h))

        # Draw confirm button beside the input box
        confirm_button.check_hover(pygame.mouse.get_pos())
        confirm_button.draw(window)

        pygame.display.update()
        clock.tick(60)


def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass
    pygame.font.init()

    initialize_fonts()

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Popper Fish")
    settings = create_settings()
    start_background_music(settings["volume"])

    assets = load_assets()
    if not wait_for_logo(win, assets):
        pygame.quit()
        sys.exit()

    player_name = prompt_player_name(win, assets)
    if player_name is None:
        pygame.quit()
        sys.exit()

    if not wait_for_start(win, assets, settings):
        pygame.quit()
        sys.exit()

    while True:
        play_button = Button(
            WIDTH // 2 - 200,
            HEIGHT - 78,
            170,
            38,
            "Play Again",
            BUTTON_COLOR,
            BUTTON_HOVER_COLOR,
            BUTTON_TEXT_COLOR,
        )
        exit_button = Button(
            WIDTH // 2 + 50,
            HEIGHT - 78,
            130,
            38,
            "Exit",
            BUTTON_COLOR,
            BUTTON_HOVER_COLOR,
            BUTTON_TEXT_COLOR,
        )

        should_continue, final_score = game_loop(win, assets, settings)
        if not should_continue:
            break

        waiting = True
        clock = pygame.time.Clock()
        game_over_started = pygame.time.get_ticks()
        stop_background_music()
        play_game_over_sound(settings["volume"])
        while waiting:
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            play_button.check_hover(mouse_pos)
            exit_button.check_hover(mouse_pos)

            if play_button.is_clicked(mouse_pos, mouse_clicked):
                start_background_music(settings["volume"])
                waiting = False
            elif exit_button.is_clicked(mouse_pos, mouse_clicked):
                pygame.quit()
                sys.exit()

            win.fill((0, 0, 0))
            elapsed_time = (pygame.time.get_ticks() - game_over_started) / 1000
            draw_game_over_screen(
                win, final_score, play_button, exit_button, assets, elapsed_time, player_name
            )
            pygame.display.update()
            clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
