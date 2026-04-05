import random
from entities import LifeForm, Tribe, LocationTrait, ResourceTrait
from settings import MAP_HEIGHT, MAP_WIDTH

def generate_tribe_name(life: LifeForm) -> str:
    if life.type == "Reptile":
        file = "data/names/reptile/reptile_names.txt"
    elif life.type == "Insectoid":
        file = "data/names/insectoid/insectoid_names.txt"
    elif life.type == "Arthropod":
        file = "data/names/insectoid/insectoid_names.txt" # reusing insectoid names for arthropods
    elif life.type == "Avian":
        file = "data/names/avian/avian_names.txt"
    elif life.type == "Plant":
        file = "data/names/plantoid/plantoid_names.txt"
    else:
        return f"{life.type} Tribe {random.randint(1, 1000)}"
    
    with open(file, "r") as f:
        names = [line.strip() for line in f.readlines()]

    return random.choice(names) + " (" + life.type + ")"



def generate_tribes(life_forms: list[LifeForm], map_data: dict) -> list[Tribe]:
    tribes = []
    for life in life_forms:
        num_tribes = random.randint(1, 5)
        for _ in range(num_tribes):
            tribe_name = generate_tribe_name(life)
            
            map = map_data.get(life.planet.name, "")
            random_location_xy = (int(random.uniform(0, MAP_WIDTH)), int(random.uniform(0, MAP_HEIGHT)))
            starting_tile = map[random_location_xy[0] + random_location_xy[1] * MAP_WIDTH]
            
            location_trait = LocationTrait.UNDEFINED

            if starting_tile == "W":
                location_trait = LocationTrait.WATER
            elif starting_tile == "D":
                location_trait = LocationTrait.DESERT
            elif starting_tile == "M":
                location_trait = LocationTrait.MOUNTAINS
            elif starting_tile == "P":
                location_trait = LocationTrait.PLAINS
            elif starting_tile == "F":
                location_trait = LocationTrait.FOREST
            elif starting_tile == "T":
                location_trait = LocationTrait.TUNDRA
            
            resource_trait = random.choice([ResourceTrait.AVERAGE, ResourceTrait.RICH, ResourceTrait.POOR])

            religion_scale = random.uniform(-1.0, 1.0)
            social_scale = random.uniform(-1.0, 1.0)
            size = 0.5
            strength = 0.5
            technology = 0.5

            tribe = Tribe(
                name=tribe_name,
                home_planet=life.planet,
                location=random_location_xy,
                location_trait=location_trait,
                resource_trait=resource_trait,
                religion_scale=religion_scale,
                social_scale=social_scale,
                size=size,
                strength=strength,
                technology=technology
            )

            tribes.append(tribe)
            print(f"Generated tribe: {tribe.name} on {tribe.home_planet.name} at location {tribe.location} with traits {tribe.location_trait}, {tribe.resource_trait}")

    return tribes