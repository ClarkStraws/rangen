import math
import json
from entities import Star, BinaryStarSystem, BinaryArchetype, BinaryOrbitType, ZoneProfile, Planet
from typing import Union, Optional, List
from profiles import generate_planet_profile
import random

def add_planet_color(planet: Planet) -> Planet:
    type_colors = {
        "Rocky": (150, 100, 50),
        "SuperEarth": (100, 150, 200),
        "GasGiant": (200, 150, 100),
        "IceGiant": (150, 200, 250)
    }
    color = type_colors.get(planet.type, (120, 120, 120))
    return Planet(
        name=planet.name,
        x=planet.x,
        y=planet.y,
        type=planet.type,
        size=planet.size,
        habitable=planet.habitable,
        color=color
    )

def add_star_color(star: Star) -> Star:
    classification_colors = {
        "O": (155, 176, 255),
        "B": (170, 191, 255),
        "A": (202, 215, 255),
        "F": (248, 247, 255),
        "G": (255, 244, 234),
        "K": (255, 210, 161),
        "M": (255, 204, 111)
    }
    color = classification_colors.get(star.classification.upper(), (200, 200, 200))
    return Star(
        name=star.name,
        x=star.x,
        y=star.y,
        classification=star.classification,
        color=color
    )

def generate_planets_in_zone(zone: ZoneProfile) -> List[Planet]:
    planets = []
    num_planets = random.randint(zone.min_planets, zone.max_planets)
    print(f"\nGenerating {num_planets} planets between {zone.orbit_start_au:.2f} AU and {zone.orbit_end_au:.2f} AU")
    for i in range(num_planets):
        # planet location
        x = random.uniform(zone.orbit_start_au, zone.outer_zone_end_au)
        y = random.uniform(zone.orbit_start_au, zone.outer_zone_end_au)

        # planet type based on location relative to frost line
        distance = math.sqrt((x)**2 + (y)**2)
        if distance < zone.frost_line_au:
            planet_type = random.choices(list(zone.inner_type_weights.keys()), weights=list(zone.inner_type_weights.values()))[0]
        else:
            planet_type = random.choices(list(zone.outer_type_weights.keys()), weights=list(zone.outer_type_weights.values()))[0]

        # habitability - simple model: only rocky/superearths in the inner zone can be habitable
        habitable = False
        if planet_type in ["Rocky", "SuperEarth"] and distance < zone.inner_zone_end_au:
            habitable = random.random() < 0.1  # 10% chance for habitable conditions
        
        planet = Planet(name=f"Planet-{i}", x=x, y=y, type=planet_type, size=random.uniform(0.5, 2.5), habitable=habitable, color=(0, 0, 0))
        planet = add_planet_color(planet)
        planets.append(planet)
    
    return planets

        

def generate_star() -> Star:
    spectral_classes = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    classification = random.choices(spectral_classes, weights=[0.00003, 0.13, 0.6, 3, 7.6, 12.1, 76.45])[0]
    name = f"Star-{random.randint(1000, 9999)}"
    x = random.uniform(-100, 100)
    y = random.uniform(-100, 100)
    star = Star(name=name, x=x, y=y, classification=classification, color=(0, 0, 0))
    star = add_star_color(star)
    return star

def generate_binary_star_system() -> BinaryStarSystem:
    primary = generate_star()
    secondary = generate_star()
    archetype = random.choice(list(BinaryArchetype))
    orbit_type = random.choice(list(BinaryOrbitType))
    separation_au = random.uniform(0.1, 100)  # rough separation in AU
    return BinaryStarSystem(primary=primary, secondary=secondary, archetype=archetype, orbit_type=orbit_type, separation_au=separation_au)

def generate_star_system() -> Union[Star, BinaryStarSystem]:

    random_value = random.random()
    if random_value < 0.7:
        return generate_star()
    else:
        return generate_binary_star_system()
    
def save_solar_system(filename: str, star_system: Union[Star, BinaryStarSystem], planets: List[Planet]) -> None:
     
     if isinstance(star_system, Star):
         star_data = star_system.__dict__
     else:
         star_data = {
             "primary": star_system.primary.__dict__,
             "secondary": star_system.secondary.__dict__,
             "archetype": star_system.archetype.name,
             "orbit_type": star_system.orbit_type.name,
             "separation_au": star_system.separation_au
         }
     
     json_data = {
         "star_system": star_data,
         "planets": [planet.__dict__ for planet in planets]
     }

     with open(filename, 'w', encoding='utf-8') as output_file:
        json.dump(json_data, output_file, indent=4)

def main() -> None:
    print("Beginning solar system generation...")
    star_system = generate_star_system()
    star_system.print()
    print("Generating a planet profile for the star system...")
    profile = generate_planet_profile(star_system)
    print("Generating planets in zones...")
    
    planets = []
    for i, zone in enumerate(profile.zones):
        planets.extend(generate_planets_in_zone(zone))

    print(f"Generated {len(planets)} planets.")
    for planet in planets:
        print(f"  {planet.name}: Type {planet.type}, Size {planet.size:.2f} Earths, Habitable: {planet.habitable}, at ({planet.x:.2f}, {planet.y:.2f})")

    save_solar_system("non_hm/rangen/data/solar_system.json", star_system, planets)

if __name__ == "__main__":
    main()