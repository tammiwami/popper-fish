import math
import pygame

from src.game.constants import (
    ATTACK_BOOST_COLOR,
    ATTACK_MAX_POWER,
    BUTTON_BORDER_COLOR,
    HEIGHT,
    PLAYER_MAX_HEALTH,
    TEXT_COLOR,
    UI_BORDER_COLOR,
    WIDTH,
)


UI_FONT = None
TITLE_FONT = None
OCEAN_FONT = None
BUTTON_FONT = None
SMALL_BUTTON_FONT = None
MENU_BUTTON_FONT = None
MISSION_FONT = None


def initialize_fonts():
    global UI_FONT, TITLE_FONT, OCEAN_FONT, BUTTON_FONT, SMALL_BUTTON_FONT, MENU_BUTTON_FONT, MISSION_FONT

    UI_FONT = pygame.font.SysFont("Arial", 16, bold=True)
    TITLE_FONT = pygame.font.SysFont("Arial", 40, bold=True)
    OCEAN_FONT = pygame.font.SysFont("Arial", 20, bold=True, italic=True)
    BUTTON_FONT = pygame.font.SysFont("Arial", 23, bold=True)
    SMALL_BUTTON_FONT = pygame.font.SysFont("Arial", 12, bold=True)
    MENU_BUTTON_FONT = pygame.font.SysFont("Arial", 18, bold=True)
    MISSION_FONT = pygame.font.SysFont("Arial", 20, bold=True)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, small=False, menu=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.small = small
        self.menu = menu

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BUTTON_BORDER_COLOR,
                         self.rect, 2, border_radius=10)

        if self.small:
            font = SMALL_BUTTON_FONT
        elif self.menu:
            font = MENU_BUTTON_FONT
        else:
            font = BUTTON_FONT
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click


def key_name(key):
    return pygame.key.name(key).upper()


def draw_setting_field(surface, rect, label, value, icon_text, is_active=False):
    body_color = (25, 83, 91, 220) if not is_active else (38, 112, 120, 235)
    edge_color = (145, 235, 245) if is_active else (92, 185, 195)
    text_color = (210, 250, 255) if not is_active else (255, 240, 150)

    field = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    points = [
        (18, 0),
        (rect.width - 28, 0),
        (rect.width - 8, rect.height // 2),
        (rect.width - 28, rect.height),
        (18, rect.height),
    ]
    pygame.draw.polygon(field, body_color, points)
    pygame.draw.lines(field, edge_color, True, points, 2)
    surface.blit(field, rect)

    icon_center = (rect.left + 18, rect.centery)
    icon_radius = rect.height // 2
    pygame.draw.circle(surface, (75, 145, 160), icon_center, icon_radius)
    pygame.draw.circle(surface, (190, 245, 250), icon_center, icon_radius, 2)
    icon = UI_FONT.render(icon_text, True, (220, 250, 255))
    surface.blit(icon, icon.get_rect(center=icon_center))

    text = UI_FONT.render(f"{label}: {value}", True, text_color)
    surface.blit(text, (rect.left + 55, rect.top + 9))


def draw_volume_field(surface, rect, volume, is_active=False):
    body_color = (25, 83, 91, 220)
    edge_color = (145, 235, 245) if is_active else (92, 185, 195)
    outer_rect = pygame.Rect(
        rect.left - 188, rect.top - 10, rect.width + 265, rect.height + 20)

    field = pygame.Surface(
        (outer_rect.width, outer_rect.height), pygame.SRCALPHA)
    points = [
        (18, 0),
        (outer_rect.width - 28, 0),
        (outer_rect.width - 8, outer_rect.height // 2),
        (outer_rect.width - 28, outer_rect.height),
        (18, outer_rect.height),
    ]
    pygame.draw.polygon(field, body_color, points)
    pygame.draw.lines(field, edge_color, True, points, 2)
    surface.blit(field, outer_rect)

    icon_center = (outer_rect.left + 18, outer_rect.centery)
    icon_radius = outer_rect.height // 2
    pygame.draw.circle(surface, (75, 145, 160), icon_center, icon_radius)
    pygame.draw.circle(surface, (190, 245, 250), icon_center, icon_radius, 2)
    icon = UI_FONT.render("V", True, (220, 250, 255))
    surface.blit(icon, icon.get_rect(center=icon_center))

    label = UI_FONT.render("Audio", True, (210, 250, 255))
    surface.blit(label, (outer_rect.left + 55, outer_rect.top + 9))

    pygame.draw.rect(surface, (4, 34, 45), rect, border_radius=4)
    fill_rect = pygame.Rect(rect.left, rect.top, int(
        rect.width * volume), rect.height)
    pygame.draw.rect(surface, (255, 205, 70), fill_rect, border_radius=4)
    pygame.draw.rect(surface, (220, 250, 255), rect, 2, border_radius=4)

    value = UI_FONT.render(f"{round(volume * 100)}%", True, (220, 250, 255))
    surface.blit(value, (rect.right + 12, rect.top - 1))


def draw_ui_panel(surface, x, y, width, height, bubbles):
    panel = pygame.Surface((width, height), pygame.SRCALPHA)

    for i in range(height):
        alpha = 180 - int(100 * (i / height))
        color = (0, 20 + int(30 * (i / height)),
                 40 + int(60 * (i / height)), alpha)
        pygame.draw.line(panel, color, (0, i), (width, i))

    pygame.draw.rect(panel, UI_BORDER_COLOR,
                     panel.get_rect(), 2, border_radius=6)

    panel.blit(bubbles["small"], (10, 15))
    panel.blit(bubbles["medium"], (width - 25, 30))
    panel.blit(bubbles["small"], (width - 15, 10))

    surface.blit(panel, (x, y))


def draw_health_bar(surface, x, y, current, max_health, width, height, bubbles):
    ratio = max(0, min(current / max_health, 1))
    fill_width = int(width * ratio)

    pygame.draw.rect(surface, (0, 35, 25),
                     (x, y, width, height), border_radius=3)
    pygame.draw.rect(surface, (35, 220, 90),
                     (x, y, fill_width, height), border_radius=3)

    border_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, UI_BORDER_COLOR, border_rect, 2, border_radius=3)

    if current > 0:
        bubble_pos = x + int(width * ratio) - 5
        surface.blit(bubbles["small"], (bubble_pos, y - 3))
    try:
        health_text = SMALL_BUTTON_FONT.render(
            f"{int(current)}/{int(max_health)}", True, (255, 255, 255))
    except Exception:
        health_text = UI_FONT.render(
            f"{int(current)}/{int(max_health)}", True, (255, 255, 255))
    ht_rect = health_text.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(health_text, ht_rect)


def draw_attack_power_bar(surface, x, y, current, max_power, width, height):
    ratio = max(0, min(current / max_power, 1))
    fill_width = int(width * ratio)

    pygame.draw.rect(surface, (0, 25, 45),
                     (x, y, width, height), border_radius=3)

    for i in range(fill_width):
        hue = int(300 * (i / max(width - 1, 1)))
        color = pygame.Color(0)
        color.hsva = (hue, 95, 100, 100)
        pygame.draw.rect(surface, color, (x + i, y, 1, height))

    pygame.draw.rect(surface, UI_BORDER_COLOR,
                     (x, y, width, height), 2, border_radius=3)

    value_text = SMALL_BUTTON_FONT.render(
        f"{current}/{max_power}", True, (255, 255, 255))
    value_rect = value_text.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(value_text, value_rect)


def draw_score_popup(surface, x, y, score, alpha):
    if alpha <= 0:
        return

    bubble = pygame.Surface((60, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(bubble, (0, 100, 150, alpha // 2), (0, 0, 60, 30))
    pygame.draw.ellipse(bubble, (0, 200, 255, alpha // 3), (0, 0, 60, 30), 2)
    bubble.set_alpha(alpha)
    surface.blit(bubble, (x - 30, y - 15))

    text = UI_FONT.render(f"+{score}", True, (255, 255, 255))
    text.set_alpha(alpha)
    surface.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


def format_score(score):
    return f"{score:,}"


def build_leaderboard_rows(current_score, player_name="You", max_rows=5):
    from src.game.constants import PROJECT_ROOT

    hs_file = PROJECT_ROOT / "highscore.txt"
    scores = {}

    if hs_file.exists():
        try:
            for line in hs_file.read_text().splitlines():
                if not line.strip():
                    continue
                if "," in line:
                    name, val = line.split(",", 1)
                    try:
                        val = int(val.strip())
                    except ValueError:
                        continue
                    name = name.strip()
                    scores[name] = max(scores.get(name, 0), val)
                else:
                    try:
                        val = int(line.strip())
                        scores.setdefault("Anonymous", 0)
                        scores["Anonymous"] = max(scores["Anonymous"], val)
                    except ValueError:
                        continue
        except Exception:
            scores = {}

    if player_name:
        scores[player_name] = max(scores.get(
            player_name, 0), int(current_score))

    sorted_rows = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

    top_n = 4
    top_players = sorted_rows[:top_n]

    rows = []
    for idx, (name, sc) in enumerate(top_players, start=1):
        rows.append((idx, name, sc, name == player_name))

    top_names = [n for n, _ in top_players]

    if player_name in top_names:
        if len(sorted_rows) > top_n:
            fifth_name, fifth_score = sorted_rows[top_n]
            rows.append((top_n + 1, fifth_name, fifth_score, False))
        else:
            rows.append((top_n + 1, "-", 0, False))
    else:
        player_rank = None
        player_score = int(current_score)
        for i, (n, s) in enumerate(sorted_rows, start=1):
            if n == player_name:
                player_rank = i
                player_score = s
                break
        if player_rank is None:
            player_rank = len(sorted_rows) + 1
        rows.append((player_rank, player_name, player_score, True))

    try:
        lines = [f"{name},{sc}" for name, sc in top_players]
        hs_file.write_text("\n".join(lines))
    except Exception:
        pass

    return rows


def draw_game_over_screen(surface, score, play_button, exit_button, assets, elapsed_time, player_name="You"):
    bubbles = assets["bubbles"]
    surface.blit(assets["menu_bg"], (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 35, 65, 110))

    bubble_sprites = [bubbles["small"], bubbles["medium"], bubbles["large"]]
    drift = 85 * math.log1p(elapsed_time * 0.75)
    for i in range(20):
        bubble_x = (37 + i * 127) % WIDTH
        bubble_y = (HEIGHT + ((19 + i * 83) % HEIGHT) - drift) % HEIGHT
        overlay.blit(bubble_sprites[i %
                     len(bubble_sprites)], (bubble_x, bubble_y))

    surface.blit(overlay, (0, 0))

    lw, lh = assets["logo"].get_size()
    max_logo_w = int(min(WIDTH * 0.46, 420))
    max_logo_h = 92
    scale = min(max_logo_w / lw, max_logo_h / lh, 1.0)
    logo = pygame.transform.smoothscale(assets["logo"], (int(
        lw * scale), int(lh * scale))) if scale < 1.0 else assets["logo"]

    panel_width, panel_height = 650, 255
    panel_x = WIDTH // 2 - panel_width // 2
    panel_y = 145
    safe_bottom = panel_y - 34
    logo_center_y = safe_bottom - (logo.get_height() // 2)
    logo_rect = logo.get_rect(
        center=(WIDTH // 2, max(logo.get_height() // 2 + 8, logo_center_y)))
    surface.blit(logo, logo_rect)

    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

    pygame.draw.rect(surface, (3, 45, 82, 230), panel_rect, border_radius=8)
    pygame.draw.rect(surface, (244, 183, 31), panel_rect, 5, border_radius=8)
    pygame.draw.rect(surface, (42, 170, 210),
                     panel_rect.inflate(-14, -14), 2, border_radius=6)

    label_rect = pygame.Rect(WIDTH // 2 - 170, panel_y - 28, 340, 46)
    pygame.draw.rect(surface, (12, 77, 120), label_rect, border_radius=8)
    pygame.draw.rect(surface, (165, 235, 255), label_rect, 3, border_radius=8)
    label = BUTTON_FONT.render("LEADERBOARD", True, (255, 255, 255))
    surface.blit(label, label.get_rect(center=label_rect.center))

    header_y = panel_y + 35
    rank_col_x = panel_x + 58
    name_col_x = panel_x + 185
    score_col_x = panel_x + 495

    header = UI_FONT.render("RANK", True, (255, 213, 45))
    surface.blit(header, (panel_x + 45, header_y))
    header = UI_FONT.render("PLAYER", True, (255, 255, 255))
    surface.blit(header, (name_col_x, header_y))
    header = UI_FONT.render("SCORE", True, (255, 213, 45))
    surface.blit(header, (score_col_x, header_y))

    rows = build_leaderboard_rows(score, player_name)
    for display_index, (rank, name, row_score, is_player) in enumerate(rows, start=1):
        row_y = panel_y + 68 + (display_index - 1) * 35
        row_rect = pygame.Rect(panel_x + 22, row_y, panel_width - 44, 32)
        if is_player:
            pygame.draw.rect(surface, (221, 164, 23),
                             row_rect, border_radius=5)
            pygame.draw.rect(surface, (255, 225, 85),
                             row_rect, 2, border_radius=5)
            row_color = (255, 255, 255)
            score_color = (255, 255, 255)
        else:
            pygame.draw.rect(surface, (4, 51, 88, 205),
                             row_rect, border_radius=5)
            pygame.draw.rect(surface, (20, 101, 145),
                             row_rect, 1, border_radius=5)
            row_color = TEXT_COLOR
            score_color = (255, 213, 45)

        rank_text = UI_FONT.render(str(rank), True, row_color)
        surface.blit(rank_text, (rank_col_x, row_y + 6))
        name_text = UI_FONT.render(name, True, row_color)
        surface.blit(name_text, (name_col_x, row_y + 6))
        score_text = UI_FONT.render(format_score(row_score), True, score_color)
        surface.blit(score_text, (score_col_x, row_y + 6))

    play_button.draw(surface)
    exit_button.draw(surface)


def draw_drifting_bubbles(surface, bubbles, elapsed_time, count=18, speed=42):
    bubble_sprites = [bubbles["small"], bubbles["medium"], bubbles["large"]]

    for i in range(count):
        sprite = bubble_sprites[i % len(bubble_sprites)]
        x = (53 + i * 109 + math.sin(elapsed_time * 0.8 + i) * 14) % WIDTH
        y = (HEIGHT + ((29 + i * 71) % HEIGHT) - elapsed_time * speed) % HEIGHT
        surface.blit(sprite, (x, y))


def draw_start_screen(
    surface,
    assets,
    start_button,
    settings_button=None,
    settings=None,
    controls=None,
    active_binding=None,
    show_settings=False,
    has_unsaved_changes=False,
):
    bubbles = assets["bubbles"]
    surface.blit(assets["bg"], (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 20, 45, 170))
    draw_drifting_bubbles(
        overlay, bubbles, pygame.time.get_ticks() / 1000, count=24, speed=36)
    surface.blit(overlay, (0, 0))

    panel_width, panel_height = 720, 390
    panel_x = WIDTH // 2 - panel_width // 2
    panel_y = HEIGHT // 2 - panel_height // 2
    draw_ui_panel(surface, panel_x, panel_y,
                  panel_width, panel_height, bubbles)

    lw, lh = assets["logo"].get_size()
    max_logo_w = int(panel_width * 0.5)
    max_logo_h = 120
    scale = min(max_logo_w / lw, max_logo_h / lh, 1.0)
    title_logo = pygame.transform.smoothscale(assets["logo"], (int(
        lw * scale), int(lh * scale))) if scale < 1.0 else assets["logo"]
    title_rect = title_logo.get_rect(center=(WIDTH // 2, panel_y + 60))
    surface.blit(title_logo, title_rect)

    left_key = key_name(settings["left"]) if settings else "A"
    right_key = key_name(settings["right"]) if settings else "D"
    shoot_key = key_name(settings["shoot"]) if settings else "SPACE"

    if settings_button:
        settings_button.draw(surface)

    if show_settings and settings and controls:
        rows = [
            (
                "Left",
                "Press key..." if active_binding == "left" else key_name(
                    settings["left"]),
                "L",
                "left",
            ),
            (
                "Right",
                "Press key..." if active_binding == "right" else key_name(
                    settings["right"]),
                "R",
                "right",
            ),
            (
                "Shoot",
                "Press key..." if active_binding == "shoot" else key_name(
                    settings["shoot"]),
                "S",
                "shoot",
            ),
        ]

        for label, value, icon, binding in rows:
            draw_setting_field(
                surface,
                controls[binding],
                label,
                value,
                icon,
                active_binding == binding,
            )

        draw_volume_field(surface, controls["volume"], settings["volume"])

        if has_unsaved_changes:
            controls["save"].draw(surface)
    else:
        instructions = [
            "Goal: survive as long as you can and pop fish for points.",
            f"Move: press {left_key} to swim left and {right_key} to swim right.",
            f"Shoot: press {shoot_key} to fire bubbles upward.",
            "Avoid fish: touching them damages your health.",
            "Pearl or shell: gives temporary 2x attack power (lasts 12s).",
            "Seaweed or algae: restores some health.",
        ]

        y = panel_y + 135
        for line in instructions:
            text = UI_FONT.render(line, True, TEXT_COLOR)
            surface.blit(text, (panel_x + 70, y))
            y += 34

        player_preview = pygame.transform.scale(assets["player"], (105, 84))
        preview_rect = player_preview.get_rect(
            center=(panel_x + panel_width - 150, panel_y + 230))
        surface.blit(player_preview, preview_rect)

    start_button.draw(surface)

    hint = UI_FONT.render(
        f"Press ENTER or click {start_button.text} when ready.", True, (255, 255, 255))
    hint_rect = hint.get_rect(
        center=(WIDTH // 2, start_button.rect.bottom + 28))
    surface.blit(hint, hint_rect)
    pygame.display.update()


def draw(
    surface,
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
    floating_bubbles=None,
):
    bubbles = assets["bubbles"]
    surface.blit(assets["bg"], (0, 0))

    if floating_bubbles:
        for b in floating_bubbles:
            try:
                r = int(b.get("r", 6))
                alpha = max(0, min(int(b.get("alpha", 200)), 255))
                bubble_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    bubble_surf, (200, 240, 255, alpha), (r, r), r)
                surface.blit(
                    bubble_surf, (b.get("x", 0) - r, b.get("y", 0) - r))
            except Exception:
                continue

    surface.blit(assets["player"], player)
    for fish in fishes:
        surface.blit(fish.image, fish.image_rect)
    for bullet in bullets:
        surface.blit(assets["bullet"],
                     assets["bullet"].get_rect(center=bullet.center))
    for powerup in powerups:
        surface.blit(powerup.image, powerup.image_rect)

    menu_button.draw(surface)

    time_text = UI_FONT.render(
        f"TIME: {round(elapsed_time)}s", True, TEXT_COLOR)
    score_text = UI_FONT.render(f"SCORE: {score}", True, TEXT_COLOR)
    attack_bar_text = UI_FONT.render("POWER:", True, TEXT_COLOR)
    health_text = UI_FONT.render("HEALTH:", True, TEXT_COLOR)

    attack_label_x, attack_label_y = 25, 65
    health_label_x, health_label_y = 25, 87
    bar_width = 130
    bar_height = 16
    bar_gap = 10
    label_width = max(attack_bar_text.get_width(), health_text.get_width())
    bar_x = attack_label_x + label_width + bar_gap
    attack_bar_y = attack_label_y + attack_bar_text.get_height() // 2 - \
        bar_height // 2
    health_bar_y = health_label_y + health_text.get_height() // 2 - bar_height // 2

    panel_x, panel_y = 10, 10
    panel_right = bar_x + bar_width + 12
    panel_bottom = health_bar_y + bar_height + 9
    panel_width = max(220, panel_right - panel_x)
    panel_height = max(96, panel_bottom - panel_y)
    draw_ui_panel(surface, panel_x, panel_y,
                  panel_width, panel_height, bubbles)

    surface.blit(time_text, (25, 15))
    surface.blit(score_text, (25, 40))
    surface.blit(attack_bar_text, (attack_label_x, attack_label_y))
    surface.blit(health_text, (health_label_x, health_label_y))

    draw_attack_power_bar(surface, int(bar_x), int(attack_bar_y), attack_power,
                          ATTACK_MAX_POWER, bar_width, bar_height)
    draw_health_bar(surface, int(bar_x), int(health_bar_y), player_health,
                    PLAYER_MAX_HEALTH, bar_width, bar_height, bubbles)

    for popup in score_popups[:]:
        draw_score_popup(
            surface, popup["x"], popup["y"], popup["score"], popup["alpha"])
        popup["y"] -= 1
        popup["alpha"] -= 3
        if popup["alpha"] <= 0:
            score_popups.remove(popup)

    pygame.display.update()
