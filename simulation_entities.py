from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum, auto
from abc import ABC, abstractmethod
from settings import MAP_WIDTH, MAP_HEIGHT
from entities import Tribe, Planet, ResourceTrait
from math import sqrt
import random

@dataclass
class HistoryEvent:
    category: str   # "tick", "climate", "climate_tribe", "societal", "conflict", "conflict_result", "merge"
    event_type: str
    tick: int = 0
    tribe: str = ""
    enemy: str = ""
    planet: str = ""
    outcome: str = ""   # "destroyed", "affected", "won", "defended", "weakened", "merged"


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
    

'''The Ancient History Phase should have: 
- relatively high chance of random climate events
- relatively high chance of random societal events
- relatively high chance of conflict events between tribes that come into contact, especially if they have different resource traits or religion scales
- relatively high chance of merge events between tribes that come into contact and have similar social scales and resource traits
'''
class AncientHistoryPhase(SimulationPhase):

    def generate_contact_events(self, tribes: list[Tribe]) -> list[Tuple[Tribe, Tribe]]:
        contacted_tribes = []
        for i in range(len(tribes)):
            for j in range(i + 1, len(tribes)):
                tribe1 = tribes[i]
                tribe2 = tribes[j]
                if tribe1.home_planet == tribe2.home_planet:
                    distance = sqrt((tribe1.location[0] - tribe2.location[0]) ** 2 + (tribe1.location[1] - tribe2.location[1]) ** 2)
                    if distance < 150:  # arbitrary contact distance threshold
                        contacted_tribes.append((tribe1, tribe2))
        return contacted_tribes
        
    def create_climate_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        planets = []
        for tribe in tribes:
            if tribe.home_planet not in planets:
                planets.append(tribe.home_planet)

        events = []
        for planet in planets:
            event_type = random.choice(["Meteor", "Volcano", "Earthquake", "Tsunami", "Hurricane", "Drought", "Flood"])
            location_xy = (int(random.uniform(0, MAP_WIDTH)), int(random.uniform(0, MAP_HEIGHT)))

            if event_type in ["Meteor", "Volcano", "Earthquake", "Tsunami"]:
                if random.random() < 0.1:
                    events.append(HistoryEvent(category="climate", event_type=event_type, tick=tick, planet=planet.name))
                    radius = random.randint(150, 350)
                    for tribe in tribes:
                        distance = sqrt((tribe.location[0] - location_xy[0]) ** 2 + (tribe.location[1] - location_xy[1]) ** 2)
                        if distance < radius and tribe.home_planet == planet:
                            tribe.strength *= random.uniform(0.25, 0.5)
                            if tribe.strength < 0.1:
                                tribe.is_eliminated = True
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.name, planet=planet.name, outcome="destroyed"))
                            else:
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.name, planet=planet.name, outcome="affected"))

            elif event_type in ["Hurricane", "Drought", "Flood"]:
                if random.random() < 0.3:
                    events.append(HistoryEvent(category="climate", event_type=event_type, tick=tick, planet=planet.name))
                    radius = random.randint(50, 120)
                    for tribe in tribes:
                        distance = sqrt((tribe.location[0] - location_xy[0]) ** 2 + (tribe.location[1] - location_xy[1]) ** 2)
                        if distance < radius and tribe.home_planet == planet:
                            tribe.strength *= random.uniform(0.5, 0.9)
                            if tribe.strength < 0.1:
                                tribe.is_eliminated = True
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.name, planet=planet.name, outcome="destroyed"))
                            else:
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.name, planet=planet.name, outcome="affected"))
        return events

    def create_societal_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        events = []
        if random.random() < 0.2:
            for tribe in tribes:
                if tribe.resource_trait == ResourceTrait.POOR or tribe.strength < 0.5:
                    event_type = random.choice(["Famine", "Plague", "Rebellion"])
                    tribe.strength *= random.uniform(0.5, 0.9)

                elif tribe.resource_trait == ResourceTrait.RICH and tribe.strength >= 0.75:
                    event_type = random.choice(["Technological Breakthrough", "Cultural Renaissance"])
                    tribe.technology *= random.uniform(1.1, 1.5)
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.05, 1.2)
                    tribe.size *= random.uniform(1.05, 1.2)

                elif tribe.religion_scale > 0.5:
                    event_type = random.choice(["Religious Schism", "New Religion Founded"])
                    tribe.religion_scale += random.uniform(-0.2, 0.2)
                    tribe.social_scale += random.uniform(-0.1, 0.1)

                elif tribe.religion_scale < -0.5:
                    event_type = random.choice(["Secular Uprising", "Philosophical Breakthrough"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.technology *= random.uniform(1.05, 1.2)

                elif tribe.social_scale > 0.5:
                    event_type = random.choice(["Collective Movement", "Social Reform"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.05, 1.2)

                else:
                    event_type = "Civil War"
                    tribe.social_scale += random.uniform(-0.2, 0.2)
                    tribe.strength *= random.uniform(0.1, 0.5)

                if tribe.strength < 0.1:
                    tribe.is_eliminated = True
                    events.append(HistoryEvent(category="societal", event_type=event_type, tick=tick, tribe=tribe.name, outcome="destroyed"))
                else:
                    events.append(HistoryEvent(category="societal", event_type=event_type, tick=tick, tribe=tribe.name, outcome="survived"))

        return events

    def apply_passive_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        return self.create_climate_events(tribes, tick) + self.create_societal_events(tribes, tick)

    def run_interactions(self, tribes: list[Tuple[Tribe, Tribe]], tick: int) -> list[HistoryEvent]:
        events = []
        for tribe1, tribe2 in tribes:
            if tribe1.is_eliminated or tribe2.is_eliminated:
                continue

            if tribe1.resource_trait != tribe2.resource_trait:
                if random.random() < 0.6:
                    stronger = tribe1 if tribe1.strength > tribe2.strength else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    strength_diff = abs(tribe1.strength - tribe2.strength)
                    win_chance = 0.5 + (strength_diff / 2)

                    if random.random() < win_chance:
                        events.append(HistoryEvent(category="conflict", event_type="resource", tick=tick, tribe=stronger.name, enemy=weaker.name, planet=stronger.home_planet.name, outcome="won"))
                        weaker.strength *= random.uniform(0.1, 0.9)
                        stronger.resource_trait = ResourceTrait.RICH
                        weaker.resource_trait = ResourceTrait.POOR
                        if weaker.strength < 0.1:
                            weaker.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=weaker.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=weaker.name, outcome="weakened"))
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="resource", tick=tick, tribe=weaker.name, enemy=stronger.name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(0.1, 0.9)
                        weaker.resource_trait = ResourceTrait.RICH
                        stronger.resource_trait = ResourceTrait.POOR
                        if stronger.strength < 0.1:
                            stronger.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=stronger.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=stronger.name, outcome="weakened"))
                continue

            if abs(tribe1.religion_scale - tribe2.religion_scale) > .45:
                if random.random() < 0.5:
                    stronger = tribe1 if tribe1.strength > tribe2.strength else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    religion_diff = abs(tribe1.religion_scale - tribe2.religion_scale)
                    win_chance = 0.5 + (religion_diff / 2)

                    weaker.resource_trait = ResourceTrait.AVERAGE
                    stronger.resource_trait = ResourceTrait.AVERAGE

                    if random.random() < win_chance:
                        events.append(HistoryEvent(category="conflict", event_type="religious", tick=tick, tribe=stronger.name, enemy=weaker.name, planet=stronger.home_planet.name, outcome="won"))
                        weaker.strength *= random.uniform(0.1, 0.9)
                        if weaker.strength < 0.1:
                            weaker.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="religious", tick=tick, tribe=weaker.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="religious", tick=tick, tribe=weaker.name, outcome="weakened"))
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="religious", tick=tick, tribe=weaker.name, enemy=stronger.name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(0.1, 0.9)
                        if stronger.strength < 0.1:
                            stronger.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="religious", tick=tick, tribe=stronger.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="religious", tick=tick, tribe=stronger.name, outcome="weakened"))
                continue

            if abs(tribe1.social_scale - tribe2.social_scale) < 0.25 and tribe1.resource_trait == tribe2.resource_trait:
                if random.random() < 0.5:
                    stronger = tribe1 if tribe1.size > tribe2.size else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    stronger.size += weaker.size
                    stronger.strength += weaker.strength
                    stronger.technology += weaker.technology

                    weaker.is_eliminated = True
                    events.append(HistoryEvent(category="merge", event_type="merge", tick=tick, tribe=stronger.name, enemy=weaker.name, planet=stronger.home_planet.name))
                continue

        return events