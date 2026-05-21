from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum, auto
from abc import ABC, abstractmethod
from settings import MAP_WIDTH, MAP_HEIGHT
from ancient_phase_settings import (
    TRIBE_CONTACT_DISTANCE, TRIBE_ELIMINATION_THRESHOLD,
    CATASTROPHIC_EVENT_CHANCE, WEATHER_EVENT_CHANCE,
    CATASTROPHIC_EVENT_RADIUS_MIN, CATASTROPHIC_EVENT_RADIUS_MAX,
    WEATHER_EVENT_RADIUS_MIN, WEATHER_EVENT_RADIUS_MAX,
    SOCIETAL_EVENT_CHANCE,
    POOR_STRENGTH_THRESHOLD, RICH_STRENGTH_THRESHOLD,
    HIGH_RELIGION_THRESHOLD, LOW_RELIGION_THRESHOLD, HIGH_SOCIAL_THRESHOLD,
    RESOURCE_CONFLICT_CHANCE, RELIGIOUS_CONFLICT_CHANCE, RELIGIOUS_CONFLICT_THRESHOLD,
    MERGE_CHANCE, MERGE_SOCIAL_THRESHOLD,
)
from entities import Tribe, Planet, ResourceTrait, HistoryEvent, SimulationPhase, SimulationResult
from math import sqrt
import random


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
                    if distance < TRIBE_CONTACT_DISTANCE:
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
                if random.random() < CATASTROPHIC_EVENT_CHANCE:
                    events.append(HistoryEvent(category="climate", event_type=event_type, tick=tick, planet=planet.name))
                    radius = random.randint(CATASTROPHIC_EVENT_RADIUS_MIN, CATASTROPHIC_EVENT_RADIUS_MAX)
                    for tribe in tribes:
                        distance = sqrt((tribe.location[0] - location_xy[0]) ** 2 + (tribe.location[1] - location_xy[1]) ** 2)
                        if distance < radius and tribe.home_planet == planet:
                            tribe.strength *= random.uniform(0.25, 0.5)
                            if tribe.strength < TRIBE_ELIMINATION_THRESHOLD:
                                tribe.is_eliminated = True
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.name, planet=planet.name, outcome="destroyed"))
                            else:
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.name, planet=planet.name, outcome="affected"))

            elif event_type in ["Hurricane", "Drought", "Flood"]:
                if random.random() < WEATHER_EVENT_CHANCE:
                    events.append(HistoryEvent(category="climate", event_type=event_type, tick=tick, planet=planet.name))
                    radius = random.randint(WEATHER_EVENT_RADIUS_MIN, WEATHER_EVENT_RADIUS_MAX)
                    for tribe in tribes:
                        distance = sqrt((tribe.location[0] - location_xy[0]) ** 2 + (tribe.location[1] - location_xy[1]) ** 2)
                        if distance < radius and tribe.home_planet == planet:
                            tribe.strength *= random.uniform(0.5, 0.9)
                            if tribe.strength < TRIBE_ELIMINATION_THRESHOLD:
                                tribe.is_eliminated = True
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.name, planet=planet.name, outcome="destroyed"))
                            else:
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.name, planet=planet.name, outcome="affected"))
        return events

    def create_societal_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        events = []
        if random.random() < SOCIETAL_EVENT_CHANCE:
            for tribe in tribes:
                if tribe.resource_trait == ResourceTrait.POOR or tribe.strength < POOR_STRENGTH_THRESHOLD:
                    event_type = random.choice(["Famine", "Plague", "Rebellion"])
                    tribe.strength *= random.uniform(0.5, 0.9)

                elif tribe.resource_trait == ResourceTrait.RICH and tribe.strength >= RICH_STRENGTH_THRESHOLD:
                    event_type = random.choice(["Technological Breakthrough", "Cultural Renaissance"])
                    tribe.technology *= random.uniform(1.1, 1.5)
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.05, 1.2)
                    tribe.size *= random.uniform(1.05, 1.2)

                elif tribe.religion_scale > HIGH_RELIGION_THRESHOLD:
                    event_type = random.choice(["Religious Schism", "New Religion Founded"])
                    tribe.religion_scale += random.uniform(-0.2, 0.2)
                    tribe.social_scale += random.uniform(-0.1, 0.1)

                elif tribe.religion_scale < LOW_RELIGION_THRESHOLD:
                    event_type = random.choice(["Secular Uprising", "Philosophical Breakthrough"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.technology *= random.uniform(1.05, 1.2)

                elif tribe.social_scale > HIGH_SOCIAL_THRESHOLD:
                    event_type = random.choice(["Collective Movement", "Social Reform"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.05, 1.2)

                else:
                    event_type = "Civil War"
                    tribe.social_scale += random.uniform(-0.2, 0.2)
                    tribe.strength *= random.uniform(0.1, 0.5)

                if tribe.strength < TRIBE_ELIMINATION_THRESHOLD:
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
                if random.random() < RESOURCE_CONFLICT_CHANCE:
                    stronger = tribe1 if tribe1.strength > tribe2.strength else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    strength_diff = abs(tribe1.strength - tribe2.strength)
                    win_chance = 0.5 + (strength_diff / 2)

                    if random.random() < win_chance:
                        events.append(HistoryEvent(category="conflict", event_type="resource", tick=tick, tribe=stronger.name, enemy=weaker.name, planet=stronger.home_planet.name, outcome="won"))
                        weaker.strength *= random.uniform(0.1, 0.9)
                        stronger.resource_trait = ResourceTrait.RICH
                        weaker.resource_trait = ResourceTrait.POOR
                        if weaker.strength < TRIBE_ELIMINATION_THRESHOLD:
                            weaker.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=weaker.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=weaker.name, outcome="weakened"))
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="resource", tick=tick, tribe=weaker.name, enemy=stronger.name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(0.1, 0.9)
                        weaker.resource_trait = ResourceTrait.RICH
                        stronger.resource_trait = ResourceTrait.POOR
                        if stronger.strength < TRIBE_ELIMINATION_THRESHOLD:
                            stronger.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=stronger.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=stronger.name, outcome="weakened"))
                continue

            if abs(tribe1.religion_scale - tribe2.religion_scale) > RELIGIOUS_CONFLICT_THRESHOLD:
                if random.random() < RELIGIOUS_CONFLICT_CHANCE:
                    stronger = tribe1 if tribe1.strength > tribe2.strength else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    religion_diff = abs(tribe1.religion_scale - tribe2.religion_scale)
                    win_chance = 0.5 + (religion_diff / 2)

                    weaker.resource_trait = ResourceTrait.AVERAGE
                    stronger.resource_trait = ResourceTrait.AVERAGE

                    if random.random() < win_chance:
                        events.append(HistoryEvent(category="conflict", event_type="religious", tick=tick, tribe=stronger.name, enemy=weaker.name, planet=stronger.home_planet.name, outcome="won"))
                        weaker.strength *= random.uniform(0.1, 0.9)
                        if weaker.strength < TRIBE_ELIMINATION_THRESHOLD:
                            weaker.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="religious", tick=tick, tribe=weaker.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="religious", tick=tick, tribe=weaker.name, outcome="weakened"))
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="religious", tick=tick, tribe=weaker.name, enemy=stronger.name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(0.1, 0.9)
                        if stronger.strength < TRIBE_ELIMINATION_THRESHOLD:
                            stronger.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="religious", tick=tick, tribe=stronger.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="religious", tick=tick, tribe=stronger.name, outcome="weakened"))
                continue

            if abs(tribe1.social_scale - tribe2.social_scale) < MERGE_SOCIAL_THRESHOLD and tribe1.resource_trait == tribe2.resource_trait:
                if random.random() < MERGE_CHANCE:
                    stronger = tribe1 if tribe1.size > tribe2.size else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    stronger.size += weaker.size
                    stronger.strength += weaker.strength
                    stronger.technology += weaker.technology

                    weaker.is_eliminated = True
                    events.append(HistoryEvent(category="merge", event_type="merge", tick=tick, tribe=stronger.name, enemy=weaker.name, planet=stronger.home_planet.name))
                continue

        return events