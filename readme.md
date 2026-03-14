# rangen

Procedural content generator for a forthcoming sci-fi space exploration and dungeon crawler RPG.

This system pre-generates all game content: star systems, planets, surface maps, life forms and histories. The output is consumed by the game itself at [ClarkStraws/TEXT_BASED_EXPERIMENT](https://github.com/ClarkStraws/TEXT_BASED_EXPERIMENT).

---

## What it generates

### Star Systems
- Single stars or binary pairs, weighted by real spectral class distributions (M-class most common at ~76%, O-class rarest at ~0.00003%)
- Binary systems are classified into six archetypes based on the actual stars generated:

| Archetype | Description |
|---|---|
| Twin Main Sequence | Two similar-class stars |
| Unequal Main Sequence | Two main sequence stars with a significant mass gap |
| Giant + Main Sequence | One luminous/hot star paired with a cooler companion |
| White Dwarf + Main Sequence | An A-type evolved star with a main sequence companion |
| Contact Binary | Stars so close they are physically touching |
| Compact Object | An O/B-class massive star that may host a neutron star or black hole |

- Orbit type (S-type, P-type, Wide) is derived from binary separation distance

### Planets
- Placed per zone using a frost line model: rocky/terrestrial planets form closer to the star, gas and ice giants further out
- Each planet gets: type, size, water percentage, climate, atmosphere, gravity, and habitability
- Four types: `Rocky`, `SuperEarth`, `GasGiant`, `IceGiant`

### Surface Maps
- Perlin noise terrain generation for each planet (800×400 grid)
- Biomes: Water, Desert, Forest, Mountains, Plains, Tundra
- Map output respects the planet's water percentage and climate

### Life Forms
- Generated for every habitable planet
- Habitat (Aquatic, Terrestrial, Subterranean) is determined by water percentage and atmospheric conditions
- Life form type (Mammal, Fish, Plant, etc.) is influenced by climate

---

## Project structure

```
rangen/
├── main.py                   # Entry point
├── entities.py               # Core data structures and enums
├── profiles.py               # Zone profiles per spectral class and binary archetype
├── solar_system_generation.py
├── map_generation.py
├── life_generation.py
└── data/
    └── solar_system.json     # Generated output
```

---

## Generation pipeline

```
generate_solar_system()
    └── generate_star_system()          # Single star or binary pair
    └── generate_planet_profile()       # Zone definitions based on star type(s)
    └── generate_planets_in_zone()      # Planet placement, typing, and properties
    └── save_solar_system()             # Write to data/solar_system.json

generate_maps_for_planets()             # Surface biome maps (Perlin noise)
generate_life()                         # Life forms for habitable planets
```

---

## Running it

```bash
python main.py
```

Output is written to `data/solar_system.json` and individual `*_map.txt` files per planet.

---

## Related

**[TEXT_BASED_EXPERIMENT](https://github.com/ClarkStraws/TEXT_BASED_EXPERIMENT)** — The game that consumes this generated content. A text-based sci-fi space exploration and dungeon crawler RPG. This generator is intended to pre-generate all persistent world content before or alongside game startup.