import json
import math
import random
import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
BACKGROUND_COLOR = (5, 5, 20)
TEXT_COLOR = (230, 230, 230)
BUTTON_COLOR = (60, 60, 80)
ORBIT_COLOR = (60, 60, 80)
BACKGROUND_STAR_COUNT = 200

STAR_RADIUS = 14
STAR_OFFSET = 18  # how far apart binary stars are drawn from the system center
MAX_PLANET_RADIUS = 18
ORBIT_MARGIN = 10
# closest a planet's orbit can be drawn to the system center, leaving room for
# the star icons (including the binary offset) plus the largest planet icon
MIN_ORBIT_RADIUS = STAR_OFFSET + STAR_RADIUS + MAX_PLANET_RADIUS + ORBIT_MARGIN
MAX_ORBIT_RADIUS = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2 - 60

STATE_GALAXY = "galaxy"
STATE_SYSTEM = "system"
STATE_PLANET = "planet"

# biome tile colors, keyed by the single-character codes written by map_generation.py
BIOME_COLORS = {
    "W": (40, 90, 200),    # Water
    "D": (210, 180, 110),  # Desert
    "F": (34, 120, 40),    # Forest
    "M": (120, 120, 130),  # Mountains
    "P": (140, 200, 90),   # Plains
    "T": (220, 230, 235),  # Tundra
}
BIOME_NAMES = {
    "W": "Water",
    "D": "Desert",
    "F": "Forest",
    "M": "Mountains",
    "P": "Plains",
    "T": "Tundra",
}
DEFAULT_BIOME_COLOR = (90, 90, 90)


def load_solar_system(path: str = "data/solar_system.json") -> dict:
    with open(path, "r") as f:
        return json.load(f)


def get_stars(star_system: dict) -> list[dict]:
    """Return a flat list of star dicts (1 or 2 entries) from the saved star_system data."""
    if "primary" in star_system:
        return [star_system["primary"], star_system["secondary"]]
    return [star_system]


def planet_radius(size: float) -> int:
    return max(3, min(18, int(size * 5)))


def max_orbit_distance(planets: list[dict]) -> float:
    return max((math.hypot(p["x"], p["y"]) for p in planets), default=0.0)


def planet_position(planet: dict, max_distance: float, center_x: int, center_y: int) -> tuple[int, int, int]:
    """Map a planet's (x, y) to a screen position and orbit radius in pixels.

    Orbit radius uses a square-root scale anchored at MIN_ORBIT_RADIUS so close-in
    planets are pushed clear of the star icons instead of clipping into them.
    """
    distance = math.hypot(planet["x"], planet["y"])
    angle = math.atan2(planet["y"], planet["x"])
    t = math.sqrt(distance / max_distance) if max_distance > 0 else 0.0
    orbit_radius = MIN_ORBIT_RADIUS + t * (MAX_ORBIT_RADIUS - MIN_ORBIT_RADIUS)
    px = center_x + int(orbit_radius * math.cos(angle))
    py = center_y + int(orbit_radius * math.sin(angle))
    return px, py, int(orbit_radius)


def generate_background_stars(count: int = BACKGROUND_STAR_COUNT) -> list[tuple[int, int, int]]:
    """Pre-compute a starfield so it stays static across frames."""
    return [
        (random.randint(0, WINDOW_WIDTH - 1), random.randint(0, WINDOW_HEIGHT - 1), random.randint(80, 255))
        for _ in range(count)
    ]


def draw_background_stars(screen, background_stars: list[tuple[int, int, int]]) -> None:
    for x, y, brightness in background_stars:
        screen.set_at((x, y), (brightness, brightness, brightness))


def load_planet_map(planet_name: str) -> list[str]:
    with open(f"data/maps/{planet_name}_map.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]


def build_planet_surface(planet_name: str) -> pygame.Surface:
    """Render a planet's biome map as a surface with one pixel per tile."""
    rows = load_planet_map(planet_name)
    width, height = len(rows[0]), len(rows)
    surface = pygame.Surface((width, height))
    pixels = pygame.PixelArray(surface)
    for y, row in enumerate(rows):
        for x, biome in enumerate(row):
            pixels[x, y] = BIOME_COLORS.get(biome, DEFAULT_BIOME_COLOR)
    pixels.close()
    return surface


def draw_galaxy_view(screen, font, star_system: dict, background_stars: list[tuple[int, int, int]]) -> pygame.Rect:
    """Draw the galaxy view and return the clickable rect for the system."""
    screen.fill(BACKGROUND_COLOR)
    draw_background_stars(screen, background_stars)
    stars = get_stars(star_system)

    center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
    radius = 24
    offsets = [(0, 0)] if len(stars) == 1 else [(-30, 0), (30, 0)]

    rects = []
    for star, (dx, dy) in zip(stars, offsets):
        x, y = center_x + dx, center_y + dy
        pygame.draw.circle(screen, star["color"], (x, y), radius)
        rects.append(pygame.Rect(x - radius, y - radius, radius * 2, radius * 2))

    # treat the whole system (both stars, if binary) as a single clickable button
    click_rect = rects[0].unionall(rects[1:])

    label_text = " / ".join(star["name"] for star in stars)
    label = font.render(label_text, True, TEXT_COLOR)
    screen.blit(label, (center_x - label.get_width() // 2, click_rect.bottom + 4))

    hint = font.render("Click the star system to view its planets", True, TEXT_COLOR)
    screen.blit(hint, (20, 20))
    return click_rect


def draw_system_view(
    screen, font, star_system: dict, planets: list[dict], background_stars: list[tuple[int, int, int]], mouse_pos: tuple[int, int]
) -> tuple[pygame.Rect, list[tuple[pygame.Rect, dict]]]:
    """Draw the system view and return the back-button rect and clickable planet rects."""
    screen.fill(BACKGROUND_COLOR)
    draw_background_stars(screen, background_stars)
    stars = get_stars(star_system)
    center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
    max_distance = max_orbit_distance(planets)

    # orbital paths, drawn behind the stars and planets
    for planet in planets:
        _, _, orbit_radius = planet_position(planet, max_distance, center_x, center_y)
        pygame.draw.circle(screen, ORBIT_COLOR, (center_x, center_y), orbit_radius, width=1)

    star_offsets = [(0, 0)] if len(stars) == 1 else [(-STAR_OFFSET, 0), (STAR_OFFSET, 0)]
    for star, (dx, dy) in zip(stars, star_offsets):
        pygame.draw.circle(screen, star["color"], (center_x + dx, center_y + dy), STAR_RADIUS)

    planet_rects = []
    for planet in planets:
        px, py, _ = planet_position(planet, max_distance, center_x, center_y)
        radius = planet_radius(planet["size"])
        pygame.draw.circle(screen, planet["color"], (px, py), radius)
        rect = pygame.Rect(px - radius, py - radius, radius * 2, radius * 2)
        planet_rects.append((rect, planet))
        if rect.collidepoint(mouse_pos):
            label = font.render(planet["name"], True, TEXT_COLOR)
            screen.blit(label, (px + radius + 4, py - label.get_height() // 2))

    hint = font.render("Click a planet to view its surface", True, TEXT_COLOR)
    screen.blit(hint, (20, WINDOW_HEIGHT - 30))

    back_rect = pygame.Rect(20, 20, 90, 32)
    pygame.draw.rect(screen, BUTTON_COLOR, back_rect)
    back_label = font.render("< Back", True, TEXT_COLOR)
    screen.blit(back_label, (back_rect.x + 10, back_rect.y + 6))
    return back_rect, planet_rects


def draw_planet_view(screen, font, planet: dict, planet_surface: pygame.Surface, background_stars: list[tuple[int, int, int]]) -> pygame.Rect:
    """Draw a planet's biome map, scaled to fit the window, and return the back-button rect."""
    screen.fill(BACKGROUND_COLOR)
    draw_background_stars(screen, background_stars)

    title = font.render(f"{planet['name']} - surface map", True, TEXT_COLOR)
    screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 60))

    src_width, src_height = planet_surface.get_size()
    max_width, max_height = WINDOW_WIDTH - 80, WINDOW_HEIGHT - 180
    scale = min(max_width / src_width, max_height / src_height)
    scaled = pygame.transform.scale(planet_surface, (int(src_width * scale), int(src_height * scale)))
    map_rect = scaled.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
    screen.blit(scaled, map_rect)

    # legend
    legend_y = map_rect.bottom + 20
    legend_x = map_rect.left
    for biome, color in BIOME_COLORS.items():
        pygame.draw.rect(screen, color, pygame.Rect(legend_x, legend_y, 16, 16))
        label = font.render(BIOME_NAMES[biome], True, TEXT_COLOR)
        screen.blit(label, (legend_x + 22, legend_y - 2))
        legend_x += 22 + label.get_width() + 20

    back_rect = pygame.Rect(20, 20, 90, 32)
    pygame.draw.rect(screen, BUTTON_COLOR, back_rect)
    back_label = font.render("< Back", True, TEXT_COLOR)
    screen.blit(back_label, (back_rect.x + 10, back_rect.y + 6))
    return back_rect


def main() -> None:
    data = load_solar_system()
    star_system = data["star_system"]
    planets = data["planets"]

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Solar System Viewer")
    font = pygame.font.SysFont(None, 22)
    clock = pygame.time.Clock()
    background_stars = generate_background_stars()

    state = STATE_GALAXY
    system_rect = pygame.Rect(0, 0, 0, 0)
    back_rect = pygame.Rect(0, 0, 0, 0)
    planet_rects: list[tuple[pygame.Rect, dict]] = []
    selected_planet: dict | None = None
    planet_surface: pygame.Surface | None = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == STATE_GALAXY:
                    if system_rect.collidepoint(event.pos):
                        state = STATE_SYSTEM
                elif state == STATE_SYSTEM:
                    if back_rect.collidepoint(event.pos):
                        state = STATE_GALAXY
                    else:
                        for rect, planet in planet_rects:
                            if rect.collidepoint(event.pos):
                                selected_planet = planet
                                planet_surface = build_planet_surface(planet["name"])
                                state = STATE_PLANET
                                break
                elif state == STATE_PLANET:
                    if back_rect.collidepoint(event.pos):
                        state = STATE_SYSTEM

        mouse_pos = pygame.mouse.get_pos()
        if state == STATE_GALAXY:
            system_rect = draw_galaxy_view(screen, font, star_system, background_stars)
        elif state == STATE_SYSTEM:
            back_rect, planet_rects = draw_system_view(screen, font, star_system, planets, background_stars, mouse_pos)
        else:
            back_rect = draw_planet_view(screen, font, selected_planet, planet_surface, background_stars)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
