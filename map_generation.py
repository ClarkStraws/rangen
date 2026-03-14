from entities import BinaryStarSystem, Planet, Star
from typing import Union
import random
import math
from perlin_noise import PerlinNoise

MAP_WIDTH = 800
MAP_HEIGHT = 400


def generate_maps_for_planets(planets: list[Planet]) -> None:
    for planet in planets:
        generate_map(planet)

def generate_map(planet: Planet) -> None:
    ### generate map of planet using perlin noise and data from planet
    biome_noise = PerlinNoise(octaves=4, seed=random.randint(1, 10000))
    map_data = []
    biome_types = ["Water", "Desert", "Forest", "Mountains", "Plains", "Tundra"]

    for y in range(MAP_HEIGHT):
        row = []
        for x in range(MAP_WIDTH):
            # Sample noise and adjust based on planet properties
            noise_val = biome_noise([x / MAP_WIDTH, y / MAP_HEIGHT])
            # Adjust noise based on water percentage and climate
            if planet.water_percentage > 0.5:
                noise_val += 0.2  # More likely to be water
            if planet.climate == "Hot":
                noise_val -= 0.1  # More likely to be desert
            elif planet.climate == "Cold":
                noise_val += 0.1  # More likely to be tundra

            # Determine biome type based on adjusted noise value
            if noise_val < -0.2 and planet.water_percentage > 0.1:
                biome = "W" # Water
            elif noise_val < 0:
                if planet.climate == "Cold":
                    biome = "T" # Tundra
                else:
                    biome = "D" # Desert
            elif noise_val < 0.2 and planet.habitable:
                biome = "P" # Plains
            elif noise_val < 0.4 and planet.habitable:
                biome = "F" # Forest
            elif noise_val < 0.6:
                biome = "M" # Mountains
            else:
                if planet.climate == "Cold":
                    biome = "T" # Tundra
                else:
                    biome = "D" # Desert

            row.append(biome)
        map_data.append(row)
    
    # Save the map to a file in /data/maps/ with the planet name
    with open(f"data/maps/{planet.name}_map.txt", "w") as f:
        for row in map_data:
            f.write("".join(row) + "\n")