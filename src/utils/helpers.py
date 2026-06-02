import pygame

from src.entities.fish import FishType
from src.entities.powerup import PowerUpType
from src.game.constants import (
    ALGAE_HEIGHT,
    ALGAE_WIDTH,
    BACKGROUND_MUSIC,
    BLUE,
    BUBBLE_COLOR,
    BULLET_HEIGHT,
    BULLET_WIDTH,
    CYAN,
    FISH1_HEIGHT,
    FISH1_WIDTH,
    FISH2_HEIGHT,
    FISH2_WIDTH,
    FISH3_HEIGHT,
    FISH3_WIDTH,
    GAME_OVER_SOUND,
    GREEN,
    HEIGHT,
    IMAGE_DIR,
    ORANGE,
    PEARL_HEIGHT,
    PEARL_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    PURPLE,
    RED,
    SEAWEED_HEIGHT,
    SEAWEED_WIDTH,
    SHELL_HEIGHT,
    SHELL_WIDTH,
    WHITE,
    WIDTH,
    YELLOW,
)


def set_music_volume(volume):
    try:
        pygame.mixer.music.set_volume(max(0, min(volume, 1)))
    except pygame.error:
        pass


def start_background_music(volume=0.45):
    if not BACKGROUND_MUSIC.exists():
        return

    try:
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        set_music_volume(volume)
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass


def stop_background_music():
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        pass


def play_game_over_sound(volume=0.75):
    if not GAME_OVER_SOUND.exists():
        return

    try:
        sound = pygame.mixer.Sound(GAME_OVER_SOUND)
        sound.set_volume(volume)
        sound.play()
    except pygame.error:
        pass


def load_image(name, width, height, default_color=None):
    try:
        image = pygame.image.load(IMAGE_DIR / f"{name}.png")
        try:
            image = image.convert_alpha()
        except Exception:
            image = image.convert()
        return pygame.transform.scale(image, (width, height))
    except pygame.error:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if default_color:
            surface.fill(default_color)
        return surface


def create_bubble_surface(radius):
    bubble = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(bubble, BUBBLE_COLOR, (radius, radius), radius)
    pygame.draw.circle(bubble, (255, 255, 255, 50),
                       (radius, radius), radius, 1)
    return bubble


def load_assets():
    try:
        background = pygame.transform.scale(
            pygame.image.load(IMAGE_DIR / "orig.png"), (WIDTH, HEIGHT)
        )
    except pygame.error:
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill((0, 100, 200))

    try:
        menu_background = pygame.transform.scale(
            pygame.image.load(IMAGE_DIR / "menu_bg.png"), (WIDTH, HEIGHT)
        )
    except pygame.error:
        menu_background = background

    return {
        "bg": background,
        "menu_bg": menu_background,
        "logo": load_image("logo", 700, 364, ),
        "bubbles": {
            "small": create_bubble_surface(5),
            "medium": create_bubble_surface(10),
            "large": create_bubble_surface(15),
        },
        "player": load_image("player", PLAYER_WIDTH, PLAYER_HEIGHT, RED),
        "fish": {
            FishType.TYPE1: load_image("fish1", FISH1_WIDTH, FISH1_HEIGHT, BLUE),
            FishType.TYPE2: load_image("fish2", FISH2_WIDTH, FISH2_HEIGHT, GREEN),
            FishType.TYPE3: load_image("fish3", FISH3_WIDTH, FISH3_HEIGHT, PURPLE),
        },
        "bullet": load_image("bullet", BULLET_WIDTH, BULLET_HEIGHT, YELLOW),
        "powerups": {
            PowerUpType.PEARL: load_image("pearl", PEARL_WIDTH, PEARL_HEIGHT, WHITE),
            PowerUpType.SHELL: load_image("shell", SHELL_WIDTH, SHELL_HEIGHT, ORANGE),
            PowerUpType.SEAWEED: load_image("seaweed", SEAWEED_WIDTH, SEAWEED_HEIGHT, GREEN),
            PowerUpType.ALGAE: load_image("algae", ALGAE_WIDTH, ALGAE_HEIGHT, CYAN),
        },
    }
