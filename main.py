from solar_system_generation import generate_solar_system
from map_generation import generate_maps_for_planets
from life_generation import generate_life
from entities import Planet
from civ_simulation import simulate_history
from civ_generation import generate_tribes
import json
import os

def main() -> None:
    #generate_solar_system()
    planets = json.load(open("data/solar_system.json", "r"))["planets"]
    planets = [Planet(**planet) for planet in planets]

    # # clear old planets out
    # for filename in os.listdir("data/maps/"):
    #     if filename.endswith("_map.txt"):
    #         os.remove(os.path.join("data/maps/", filename))
    #generate_maps_for_planets(planets)

    life = generate_life(planets)

    planet_maps = {}
    for planet in planets:
        with open(f"data/maps/{planet.name}_map.txt", "r") as f:
            planet_maps[planet.name] = f.read()
    
    
    tribes = generate_tribes(life, planet_maps)

    simulate_history(tribes, ticks=10)


if __name__ == "__main__":
    main()