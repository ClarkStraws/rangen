import random
from typing import Union, Optional, List
from entities import Star, BinaryStarSystem, BinaryArchetype, BinaryOrbitType, ZoneProfile, Planet
from profiles import generate_planet_profile
from generator_settings import SINGLE_STAR_PROBABILITY, HABITABILITY_CHANCE
import math
import json


def generate_solar_system() -> None:
    planets = []
    star_system = generate_star_system()
    if isinstance(star_system, Star):
        print("Generated single star system:")
        star_system.print()
        planet_profile = generate_planet_profile(star_system)
    else:
        print("Generated binary star system:")
        star_system.print()
        planet_profile = generate_planet_profile(star_system)

    for zone in planet_profile.zones:
        planets.extend(generate_planets_in_zone(zone))

    print(f"\nGenerated {len(planets)} planets:")
    for planet in planets:
        print(f"  {planet.name}: Type {planet.type}, Size {planet.size:.2f} Earths, Habitable: {planet.habitable}, Color: {planet.color}")
    
    save_solar_system("data/solar_system.json", star_system, planets)


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
        water_percentage=planet.water_percentage,
        climate=planet.climate,
        atmosphere=planet.atmosphere,
        gravity=planet.gravity,
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
        # planet location: sample orbital radius, then place on a random angle
        distance = random.uniform(zone.orbit_start_au, zone.outer_zone_end_au)
        angle = random.uniform(0, 2 * math.pi)
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)

        # planet type based on location relative to frost line
        planet_type = ""
        water_percentage = 0.0
        climate = ""
        atmosphere = ""
        gravity = 0.0
        if distance < zone.frost_line_au:
            planet_type = random.choices(list(zone.inner_type_weights.keys()), weights=list(zone.inner_type_weights.values()))[0]

            if planet_type in ["Rocky", "SuperEarth"] and distance > .05:  # Very close planets may lose water, but others can have some
                water_percentage = random.uniform(0, .9)
                climate = random.choice(["Hot", "Temperate", "Cold"])
                atmosphere = random.choice(["Thin", "Breathable", "Thick"])
                gravity = random.uniform(0.5, 2.0)  # Earth gravity as baseline
            elif planet_type in ["Rocky", "SuperEarth"] and distance < .05:
                water_percentage = 0.0
                climate = "Scorching"
                atmosphere = "Thin"
                gravity = random.uniform(0.5, 2.0)
            else:
                water_percentage = random.uniform(0, 1)
                climate = random.choice(["Gas Giant", "Ice Giant"])
                atmosphere = "Thick"
                gravity = random.uniform(1.0, 3.0)  # Gas giants have stronger gravity
        else:
            planet_type = random.choices(list(zone.outer_type_weights.keys()), weights=list(zone.outer_type_weights.values()))[0]

        # habitability - simple model: only rocky/superearths in the inner zone can be habitable
        habitable = False
        if planet_type in ["Rocky", "SuperEarth"] and distance < zone.inner_zone_end_au:
            habitable = random.random() < HABITABILITY_CHANCE
    

        planet = Planet(name=f"Planet-{i}", x=x, y=y, type=planet_type, size=random.uniform(0.5, 2.5), water_percentage=water_percentage, climate=climate, atmosphere=atmosphere, gravity=gravity, habitable=habitable, color=(0, 0, 0))
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

_SPECTRAL_ORDER = ['O', 'B', 'A', 'F', 'G', 'K', 'M']

def _determine_archetype(primary: Star, secondary: Star, separation_au: float) -> BinaryArchetype:
    p = primary.classification.upper()
    s = secondary.classification.upper()
    p_idx = _SPECTRAL_ORDER.index(p)
    s_idx = _SPECTRAL_ORDER.index(s)
    diff = abs(p_idx - s_idx)

    # Physically touching or extremely close stars
    if separation_au < 0.5:
        return BinaryArchetype.CONTACT_BINARY

    # O or B star: massive enough to produce compact object remnants
    if p in ('O', 'B') or s in ('O', 'B'):
        return BinaryArchetype.COMPACT_OBJECT

    # One A-type star: A stars evolve into white dwarfs
    if p == 'A' or s == 'A':
        if diff == 0:
            return BinaryArchetype.TWIN_MAIN_SEQUENCE        # A + A
        elif diff <= 2:
            return BinaryArchetype.UNEQUAL_MAIN_SEQUENCE     # A + F/G
        else:
            return BinaryArchetype.WHITE_DWARF_MAIN_SEQUENCE # A + K/M

    # Both stars are cool main sequence (F through M)
    if diff <= 1:
        return BinaryArchetype.TWIN_MAIN_SEQUENCE
    elif diff == 2:
        return BinaryArchetype.UNEQUAL_MAIN_SEQUENCE
    else:
        return BinaryArchetype.GIANT_MAIN_SEQUENCE           # e.g. F + M (large luminosity gap)

def _determine_orbit_type(separation_au: float, archetype: BinaryArchetype) -> BinaryOrbitType:
    # Contact binaries and very close pairs: planet must orbit both stars (circumbinary)
    if archetype == BinaryArchetype.CONTACT_BINARY or separation_au < 2:
        return BinaryOrbitType.P_TYPE
    # Moderate separation: stable orbit around just one star
    elif separation_au < 50:
        return BinaryOrbitType.S_TYPE
    # Very wide pair: stars barely influence each other
    else:
        return BinaryOrbitType.WIDE

def generate_binary_star_system() -> BinaryStarSystem:
    primary = generate_star()
    secondary = generate_star()
    separation_au = random.uniform(0.1, 100)
    archetype = _determine_archetype(primary, secondary, separation_au)
    orbit_type = _determine_orbit_type(separation_au, archetype)
    return BinaryStarSystem(primary=primary, secondary=secondary, archetype=archetype, orbit_type=orbit_type, separation_au=separation_au)

def generate_star_system() -> Union[Star, BinaryStarSystem]:

    if random.random() < SINGLE_STAR_PROBABILITY:
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
