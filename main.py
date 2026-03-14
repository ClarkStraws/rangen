from solar_system_generation import generate_solar_system
from map_generation import generate_maps_for_planets
from life_generation import generate_life
from entities import Planet
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

if __name__ == "__main__":
    main()