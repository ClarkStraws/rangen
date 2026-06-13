from solar_system_generation import generate_solar_system
from map_generation import generate_maps_for_planets
from life_generation import generate_life
from entities import Planet, Tribe
from civ_simulation import simulate_history
from civ_generation import generate_tribes
from event_log import process_event_log
import json
import os


def main() -> None:
    generate_solar_system()
    planets = json.load(open("data/solar_system.json", "r"))["planets"]
    planets = [Planet(**planet) for planet in planets]

    # clear out maps and histories from any previous run
    for filename in os.listdir("data/maps/"):
        if filename.endswith("_map.txt"):
            os.remove(os.path.join("data/maps/", filename))
    for filename in os.listdir("data/histories/"):
        if filename.endswith("_history.txt"):
            os.remove(os.path.join("data/histories/", filename))

    generate_maps_for_planets(planets)

    life = generate_life(planets)

    planet_maps = {}
    for planet in planets:
        with open(f"data/maps/{planet.name}_map.txt", "r") as f:
            planet_maps[planet.name] = f.read()

    tribes = generate_tribes(life, planet_maps)

    # group tribes by their home planet so each life-bearing planet gets its own
    # independent history
    tribes_by_planet: dict[str, list[Tribe]] = {}
    for tribe in tribes:
        tribes_by_planet.setdefault(tribe.home_planet.name, []).append(tribe)

    if not tribes_by_planet:
        print("\nNo life-bearing planets this run — nothing to simulate.")
        return

    print(f"\nSimulating history for {len(tribes_by_planet)} life-bearing planet(s)...")
    for planet_name, planet_tribes in tribes_by_planet.items():
        print(f"\n=== {planet_name} ({len(planet_tribes)} starting tribes) ===")
        result = simulate_history(planet_tribes, ticks=10)
        process_event_log(result.history, output_file=f"data/histories/{planet_name}_history.txt")

        if result.survivors:
            print(f"{planet_name}: {len(result.survivors)} society(ies) survived to the Future Age:")
            for survivor in result.survivors:
                print(f"  - {survivor.society_name}: a {survivor.government_type} led by {survivor.leader_title} {survivor.leader_name}")
        else:
            print(f"{planet_name}: no societies survived to the Future Age.")


if __name__ == "__main__":
    main()
