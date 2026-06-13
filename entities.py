from dataclasses import dataclass
from random import random
from typing import List, Tuple, Dict, Optional
from enum import Enum, auto
from abc import ABC, abstractmethod
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
    species: str = ""  # life form type (e.g. "Reptile", "Insectoid") used for species-flavored naming
    location: Tuple[float, float] = (0.0, 0.0)
    location_trait: LocationTrait = LocationTrait.UNDEFINED
    resource_trait: ResourceTrait = ResourceTrait.UNDEFINED
    religion_scale: float = 0.0  # -1.0 (secular) to 1.0 (religious)
    social_scale: float = 0.0       # -1.0 (individualistic) to 1.0 (collectivist)
    size: float = 1.0  # relative size of the civilization (population, influence, etc.)
    strength: float = 1.0  # relative strength (military, economic, etc.)
    technology: float = 1.0  # relative technological level
    is_eliminated: bool = False
    society_name: str = ""     # set when the Modern Age phase founds a named society
    leader_name: str = ""
    leader_title: str = ""
    government_type: str = ""

@dataclass
class HistoryEvent:
    category: str   # "tick", "climate", "climate_tribe", "societal", "conflict", "conflict_result", "merge", "era", "society", "epilogue"
    event_type: str
    tick: int = 0
    tribe: str = ""
    enemy: str = ""
    planet: str = ""
    outcome: str = ""   # "destroyed", "affected", "won", "defended", "weakened", "merged"
    leader: str = ""    # leader title + name, used by "society"/"epilogue" events
    government: str = ""  # government type, used by "society"/"epilogue" events


@dataclass
class SimulationResult:
    tribes: list
    history: list          # list[HistoryEvent]
    survivors: list
    eliminated: list


class SimulationPhase(ABC):

    @abstractmethod
    def apply_passive_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        '''Apply passive events (e.g. climate, societal) to all tribes and return history events.'''
        ...

    @abstractmethod
    def run_interactions(self, tribes: list[Tuple[Tribe, Tribe]], tick: int) -> list[HistoryEvent]:
        '''Run interactions between tribes and return history events.'''
        ...

    @abstractmethod
    def generate_contact_events(self, tribes: list[Tribe]) -> list[Tuple[Tribe, Tribe]]:
        '''Generate contact events between tribes.'''
        ...

    def run(self, tribes: list[Tribe], ticks: int = 10) -> SimulationResult:
        """Shared simulation loop — identical across all phases."""
        history = []
        eliminated = []

        contacted_tribes = self.generate_contact_events(tribes)

        for tick in range(ticks):
            history.append(HistoryEvent(category="tick", event_type="marker", tick=tick + 1))
            history.extend(self.apply_passive_events(tribes, tick=tick + 1))
            history.extend(self.run_interactions(contacted_tribes, tick=tick + 1))
            tribes = [t for t in tribes if not t.is_eliminated]

        survivors = [t for t in tribes if not t.is_eliminated]
        return SimulationResult(tribes, history, survivors, eliminated)
    