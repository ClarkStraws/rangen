from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum, auto
from abc import ABC, abstractmethod
from settings import MAP_WIDTH, MAP_HEIGHT
from middle_phase_settings import (
    TRIBE_CONTACT_DISTANCE, TRIBE_ELIMINATION_THRESHOLD,
    CATASTROPHIC_EVENT_CHANCE, WEATHER_EVENT_CHANCE,
    CATASTROPHIC_EVENT_RADIUS_MIN, CATASTROPHIC_EVENT_RADIUS_MAX,
    WEATHER_EVENT_RADIUS_MIN, WEATHER_EVENT_RADIUS_MAX,
    SOCIETAL_EVENT_CHANCE,
    POOR_STRENGTH_THRESHOLD, RICH_STRENGTH_THRESHOLD,
    HIGH_RELIGION_THRESHOLD, LOW_RELIGION_THRESHOLD, HIGH_SOCIAL_THRESHOLD,
    RESOURCE_CONFLICT_CHANCE, RELIGIOUS_CONFLICT_CHANCE, RELIGIOUS_CONFLICT_THRESHOLD,
    MERGE_CHANCE, MERGE_SOCIAL_THRESHOLD,
    SURVIVOR_SIZE_GROWTH_MIN, SURVIVOR_SIZE_GROWTH_MAX,
    SURVIVOR_STRENGTH_GROWTH_MIN, SURVIVOR_STRENGTH_GROWTH_MAX,
    SURVIVOR_TECHNOLOGY_GROWTH_MIN, SURVIVOR_TECHNOLOGY_GROWTH_MAX,
)
from entities import Tribe, Planet, ResourceTrait, HistoryEvent, SimulationPhase, SimulationResult
from math import sqrt
import random


def grow_surviving_tribes(tribes: list[Tribe]) -> list[Tribe]:
    '''Carries ancient-phase survivors into the middle ages: the generations between ages
    let them swell into kingdoms — larger, sturdier, more advanced, and able to make contact
    across the longer distances modeled by MIDDLE_PHASE_SETTINGS.TRIBE_CONTACT_DISTANCE.'''
    for tribe in tribes:
        tribe.size *= random.uniform(SURVIVOR_SIZE_GROWTH_MIN, SURVIVOR_SIZE_GROWTH_MAX)
        tribe.strength *= random.uniform(SURVIVOR_STRENGTH_GROWTH_MIN, SURVIVOR_STRENGTH_GROWTH_MAX)
        tribe.technology *= random.uniform(SURVIVOR_TECHNOLOGY_GROWTH_MIN, SURVIVOR_TECHNOLOGY_GROWTH_MAX)
    return tribes


'''The Middle History Phase should have:
- A lower chance of catastrophic climate events than the ancient world, since kingdoms have
  the infrastructure to better prepare for and recover from disaster — though their larger
  territories mean any event that does strike touches more land and more people
- A higher chance of societal events than the ancient world, reflecting the complexity of
  feudal life: golden ages and trade booms, crusades and reformations, peasant revolts and
  succession crises
- Conflicts between kingdoms in contact lean toward territorial disputes and crusades rather
  than raw survival struggles, and are rarely existential — the defeated are weakened far
  more often than annihilated outright
- A lower chance of spontaneous mergers than tribal society; unions between kingdoms instead
  come through deliberate alliances — royal marriages, treaties, and vassalage pacts
'''
class MiddleHistoryPhase(SimulationPhase):

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
                            tribe.strength *= random.uniform(0.4, 0.7)
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
                            tribe.strength *= random.uniform(0.65, 0.95)
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
                    event_type = random.choice(["Famine", "Plague", "Peasant Revolt"])
                    tribe.strength *= random.uniform(0.5, 0.9)

                elif tribe.resource_trait == ResourceTrait.RICH and tribe.strength >= RICH_STRENGTH_THRESHOLD:
                    event_type = random.choice(["Golden Age", "Trade Boom", "Architectural Marvel"])
                    tribe.technology *= random.uniform(1.1, 1.5)
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.05, 1.2)
                    tribe.size *= random.uniform(1.05, 1.25)

                elif tribe.religion_scale > HIGH_RELIGION_THRESHOLD:
                    event_type = random.choice(["Crusade Declared", "Religious Reformation"])
                    tribe.religion_scale += random.uniform(-0.2, 0.2)
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(0.95, 1.15)

                elif tribe.religion_scale < LOW_RELIGION_THRESHOLD:
                    event_type = random.choice(["Scientific Awakening", "Humanist Movement"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.technology *= random.uniform(1.1, 1.3)

                elif tribe.social_scale > HIGH_SOCIAL_THRESHOLD:
                    event_type = random.choice(["Guild Formation", "Feudal Consolidation"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.05, 1.2)
                    tribe.size *= random.uniform(1.0, 1.15)

                else:
                    event_type = random.choice(["Succession Crisis", "Royal Conspiracy"])
                    tribe.social_scale += random.uniform(-0.2, 0.2)
                    tribe.strength *= random.uniform(0.5, 0.9)

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
                        events.append(HistoryEvent(category="conflict", event_type="territorial", tick=tick, tribe=stronger.name, enemy=weaker.name, planet=stronger.home_planet.name, outcome="won"))
                        weaker.strength *= random.uniform(0.3, 0.9)
                        stronger.resource_trait = ResourceTrait.RICH
                        weaker.resource_trait = ResourceTrait.POOR
                        if weaker.strength < TRIBE_ELIMINATION_THRESHOLD:
                            weaker.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="territorial", tick=tick, tribe=weaker.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="territorial", tick=tick, tribe=weaker.name, outcome="weakened"))
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="territorial", tick=tick, tribe=weaker.name, enemy=stronger.name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(0.3, 0.9)
                        weaker.resource_trait = ResourceTrait.RICH
                        stronger.resource_trait = ResourceTrait.POOR
                        if stronger.strength < TRIBE_ELIMINATION_THRESHOLD:
                            stronger.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="territorial", tick=tick, tribe=stronger.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="territorial", tick=tick, tribe=stronger.name, outcome="weakened"))
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
                        events.append(HistoryEvent(category="conflict", event_type="crusade", tick=tick, tribe=stronger.name, enemy=weaker.name, planet=stronger.home_planet.name, outcome="won"))
                        weaker.strength *= random.uniform(0.3, 0.9)
                        if weaker.strength < TRIBE_ELIMINATION_THRESHOLD:
                            weaker.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="crusade", tick=tick, tribe=weaker.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="crusade", tick=tick, tribe=weaker.name, outcome="weakened"))
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="crusade", tick=tick, tribe=weaker.name, enemy=stronger.name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(0.3, 0.9)
                        if stronger.strength < TRIBE_ELIMINATION_THRESHOLD:
                            stronger.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="crusade", tick=tick, tribe=stronger.name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="crusade", tick=tick, tribe=stronger.name, outcome="weakened"))
                continue

            if abs(tribe1.social_scale - tribe2.social_scale) < MERGE_SOCIAL_THRESHOLD and tribe1.resource_trait == tribe2.resource_trait:
                if random.random() < MERGE_CHANCE:
                    stronger = tribe1 if tribe1.size > tribe2.size else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    stronger.size += weaker.size
                    stronger.strength += weaker.strength
                    stronger.technology += weaker.technology

                    weaker.is_eliminated = True
                    events.append(HistoryEvent(category="merge", event_type="alliance", tick=tick, tribe=stronger.name, enemy=weaker.name, planet=stronger.home_planet.name))
                continue

        return events
