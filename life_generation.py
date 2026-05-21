import json
import random
from entities import Planet, LifeForm
from generator_settings import MAX_LIFE_FORMS_PER_PLANET

life_types = ["Aquatic", "Terrestrial", "Subterranean"]
life_forms = ["Fish", "Mollusk", "Coral", "Plant", "Amphibian", "Arthropod", "Insectoid", "Fungal", "Avian", "Mammal", "Reptile"]

def save_life_forms(life_forms: list[LifeForm]) -> None:
    data = []
    for life in life_forms:
        data.append({
            "name": life.name,
            "planet": life.planet.name,
            "habitat": life.habitat,
            "type": life.type
        })
    with open("data/life_forms.json", "w") as f:
        json.dump({"life_forms": data}, f, indent=2)
        
def generate_life(planets: list[Planet]) -> list[LifeForm]:
    life_forms = []
    for planet in planets:
        num_life_forms = random.randint(1, MAX_LIFE_FORMS_PER_PLANET)
        for _ in range(num_life_forms):
            life = generate_life_form(planet)
            if life:
                life_forms.append(life)

    save_life_forms(life_forms)
    return life_forms

def generate_life_form(planet: Planet) -> LifeForm:
    if not planet.habitable:
        return None
    
    else:
        print(f"Generating life on {planet.name}...")
        if planet.water_percentage > 0.75:
            life_type = "Aquatic"
            if planet.climate == "Hot":
                life_form = random.choice(["Plant", "Coral", "Mollusk"])
            elif planet.climate == "Temperate":
                life_form = random.choice(["Plant", "Fish", "Amphibian"])
            else:
                life_form = random.choice(["Plant", "Arthropod"])
        
        elif planet.water_percentage > 0.25:
            life_type = "Terrestrial"
            if planet.climate == "Hot":
                life_form = random.choice(["Plant", "Insectoid", "Reptile", "Avian"])
            elif planet.climate == "Temperate":
                life_form = random.choice(["Plant", "Mammal", "Avian", "Amphibian", "Insectoid", "Reptile", "Fungal", "Arthropod"])
            else:
                life_form = random.choice(["Mammal", "Insectoid", "Arthropod"])

        else:
            life_type = "Subterranean"
            if planet.climate == "Hot":
                life_form = random.choice(["Fungal", "Arthropod"])
            elif planet.climate == "Temperate":
                life_form = random.choice(["Fungal", "Mammal", "Insectoid", "Arthropod"])
            else:
                life_form = random.choice(["Fungal", "Mammal", "Insectoid"])
        
        if planet.atmosphere in ["Thin", "Thick"] and (planet.gravity < 0.8 or planet.gravity > 1.5):
            life_type = "Subterranean"

        life = LifeForm(planet=planet, name=f"{life_form} of {planet.name}", habitat=life_type, type=life_form)
        print(f"  - {life.name} ({life.type}, {life.habitat})")
    return life