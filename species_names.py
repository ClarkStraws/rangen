import json
import random

SPECIES_NAME_FILES = {
    "Reptile": "data/names/reptile/reptile_names.txt",
    "Insectoid": "data/names/insectoid/insectoid_names.txt",
    "Arthropod": "data/names/insectoid/insectoid_names.txt",  # reusing insectoid names for arthropods
    "Avian": "data/names/avian/avian_names.txt",
    "Plant": "data/names/plantoid/plantoid_names.txt",
    "Fish": "data/names/fish/fish_names.txt",
    "Mollusk": "data/names/mollusk/mollusk_names.txt",
    "Coral": "data/names/coral/coral_names.txt",
    "Amphibian": "data/names/amphibian/amphibian_names.txt",
    "Fungal": "data/names/fungal/fungal_names.txt",
    "Mammal": "data/names/mammal/mammal_names.txt",
}

SPECIES_TERMS_FILES = {
    "Reptile": "data/names/reptile/terms.json",
    "Insectoid": "data/names/insectoid/terms.json",
    "Arthropod": "data/names/insectoid/terms.json",
    "Avian": "data/names/avian/terms.json",
    "Plant": "data/names/plantoid/terms.json",
    "Fish": "data/names/fish/terms.json",
    "Mollusk": "data/names/mollusk/terms.json",
    "Coral": "data/names/coral/terms.json",
    "Amphibian": "data/names/amphibian/terms.json",
    "Fungal": "data/names/fungal/terms.json",
    "Mammal": "data/names/mammal/terms.json",
}

GENERIC_TERMS = {
    "nouns": [
        {"singular": "Collective", "plural": "Collectives"},
        {"singular": "Concord", "plural": "Concords"},
        {"singular": "Assembly", "plural": "Assemblies"},
        {"singular": "Conclave", "plural": "Conclaves"},
        {"singular": "Union", "plural": "Unions"},
        {"singular": "Compact", "plural": "Compacts"},
        {"singular": "Dominion", "plural": "Dominions"},
        {"singular": "Order", "plural": "Orders"},
    ],
    "adjectives": [
        "Ascendant", "Resilient", "Unified", "Emergent", "Vast",
        "Boundless", "Enduring", "Indomitable",
    ],
}


def get_name_list(species: str) -> list[str]:
    file = SPECIES_NAME_FILES.get(species)
    if not file:
        return []
    with open(file, "r") as f:
        return [line.strip() for line in f.readlines()]


def random_species_name(species: str, fallback: str) -> str:
    names = get_name_list(species)
    if not names:
        return fallback
    return random.choice(names)


def get_terms(species: str) -> dict:
    file = SPECIES_TERMS_FILES.get(species)
    if not file:
        return GENERIC_TERMS
    with open(file, "r") as f:
        return json.load(f)
