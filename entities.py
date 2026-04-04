from dataclasses import dataclass
from random import random
from typing import List, Tuple, Dict, Optional
from enum import Enum, auto
from abc import ABC, abstractmethod
from settings import MAP_WIDTH, MAP_HEIGHT
import random
from math import sqrt

class BinaryArchetype(Enum):
    TWIN_MAIN_SEQUENCE = auto()
    UNEQUAL_MAIN_SEQUENCE = auto()
    GIANT_MAIN_SEQUENCE = auto()
    WHITE_DWARF_MAIN_SEQUENCE = auto()
    CONTACT_BINARY = auto()
    COMPACT_OBJECT = auto()

class BinaryOrbitType(Enum):
    S_TYPE = auto()
    P_TYPE = auto()
    WIDE = auto()

@dataclass
class Star:
    name: str
    x: float
    y: float
    classification: str  # O | B | A | F | G | K | M
    color: Tuple[int, int, int]

    def print(self) -> None:
        print(f"{self.name}: Class {self.classification} at ({self.x:.1f}, {self.y:.1f})")

@dataclass
class BinaryStarSystem:
    primary: Star
    secondary: Star
    archetype: BinaryArchetype
    orbit_type: BinaryOrbitType
    separation_au: float  # rough separation in AU

    def print(self) -> None:
        print(f"[Binary - {self.archetype.name}, {self.orbit_type.name}, {self.separation_au:.1f} AU]")
        print(f"  Primary:   {self.primary.name} (Class {self.primary.classification})")
        print(f"  Secondary: {self.secondary.name} (Class {self.secondary.classification})")

  
@dataclass
class ZoneProfile:
    min_planets: int
    max_planets: int
    frost_line_au: float        # rocky inside, giants outside
    inner_zone_end_au: float    # outer boundary of rocky planet formation
    outer_zone_end_au: float    # system edge
    inner_type_weights: dict    # e.g. {"Rocky": 0.7, "SuperEarth": 0.3}
    outer_type_weights: dict    # e.g. {"GasGiant": 0.6, "IceGiant": 0.4}
    orbit_start_au: float = 0.1 # closest possible orbit
    orbit_end_au: Optional[float] = None # if set, clamps the zone to this outer boundary

@dataclass
class PlanetGenerationProfile:
    zones: List[ZoneProfile]
    binary_separation_au: Optional[float] = None
  
@dataclass
class Planet:
    name: str
    x: float
    y: float
    type: str
    size: float
    habitable: bool
    water_percentage: float
    climate: str
    atmosphere: str
    gravity: float
    color: Tuple[int, int, int]


@dataclass
class LifeForm:
    planet: Planet
    name: str
    habitat: str     # Aquatic, Terrestrial, Aerial, Subsurface
    type: str        # Plant, Animal, Fungal, etc.

class LocationTrait(Enum):
    WATER = auto()
    FOREST = auto()
    MOUNTAINS = auto()
    PLAINS = auto()
    DESERT = auto()
    TUNDRA = auto()
    UNDEFINED = auto()

class ResourceTrait(Enum):
    POOR = auto()
    AVERAGE = auto()
    RICH = auto()
    UNDEFINED = auto()

@dataclass
class Tribe:
    name: str
    home_planet: Planet
    location: Tuple[float, float] = (0.0, 0.0)
    location_trait: LocationTrait = LocationTrait.UNDEFINED
    resource_trait: ResourceTrait = ResourceTrait.UNDEFINED
    religion_scale: float = 0.0  # -1.0 (secular) to 1.0 (religious)
    social_scale: float = 0.0       # -1.0 (individualistic) to 1.0 (collectivist)
    size: float = 1.0  # relative size of the civilization (population, influence, etc.)
    strength: float = 1.0  # relative strength (military, economic, etc.)
    technology: float = 1.0  # relative technological level
    is_eliminated: bool = False