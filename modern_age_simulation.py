from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum, auto
from abc import ABC, abstractmethod
from settings import MAP_WIDTH, MAP_HEIGHT
from modern_phase_settings import (
    TRIBE_CONTACT_DISTANCE, TRIBE_ELIMINATION_THRESHOLD,
    CATASTROPHIC_EVENT_CHANCE, WEATHER_EVENT_CHANCE,
    CATASTROPHIC_EVENT_RADIUS_MIN, CATASTROPHIC_EVENT_RADIUS_MAX,
    WEATHER_EVENT_RADIUS_MIN, WEATHER_EVENT_RADIUS_MAX,
    SOCIETAL_EVENT_CHANCE,
    POOR_STRENGTH_THRESHOLD, RICH_STRENGTH_THRESHOLD,
    HIGH_RELIGION_THRESHOLD, LOW_RELIGION_THRESHOLD,
    HIGH_SOCIAL_THRESHOLD, LOW_SOCIAL_THRESHOLD,
    RESOURCE_CONFLICT_CHANCE, IDEOLOGICAL_CONFLICT_CHANCE,
    FEDERATION_CHANCE, FEDERATION_SOCIAL_THRESHOLD,
    SURVIVOR_SIZE_GROWTH_MIN, SURVIVOR_SIZE_GROWTH_MAX,
    SURVIVOR_STRENGTH_GROWTH_MIN, SURVIVOR_STRENGTH_GROWTH_MAX, SURVIVOR_STRENGTH_RECOVERY_FLOOR,
    SURVIVOR_TECHNOLOGY_GROWTH_MIN, SURVIVOR_TECHNOLOGY_GROWTH_MAX,
    HEGEMONY_STRENGTH_THRESHOLD,
)
from entities import Tribe, Planet, ResourceTrait, HistoryEvent, SimulationPhase, SimulationResult
from species_names import get_terms, random_species_name
from math import sqrt
import random
import re


def industrialize_surviving_tribes(tribes: list[Tribe]) -> list[Tribe]:
    '''Carries middle-age survivors into the modern age: the generations between ages bring
    industrialization — larger populations, sturdier economies and militaries, and a leap in
    technology, with reach across an entire planet as modeled by
    MODERN_PHASE_SETTINGS.TRIBE_CONTACT_DISTANCE.'''
    for tribe in tribes:
        tribe.size *= random.uniform(SURVIVOR_SIZE_GROWTH_MIN, SURVIVOR_SIZE_GROWTH_MAX)
        tribe.strength = max(tribe.strength, SURVIVOR_STRENGTH_RECOVERY_FLOOR) * random.uniform(SURVIVOR_STRENGTH_GROWTH_MIN, SURVIVOR_STRENGTH_GROWTH_MAX)
        tribe.technology *= random.uniform(SURVIVOR_TECHNOLOGY_GROWTH_MIN, SURVIVOR_TECHNOLOGY_GROWTH_MAX)
    return tribes


def _strip_species_suffix(name: str) -> str:
    return re.sub(r"\s*\([^)]*\)\s*$", "", name)


def _determine_government(tribe: Tribe) -> Tuple[str, str]:
    '''Maps a society's stats onto a government type and a title for its leader.'''
    if tribe.strength >= HEGEMONY_STRENGTH_THRESHOLD:
        return "Hegemony", "Overlord"
    if tribe.religion_scale > HIGH_RELIGION_THRESHOLD:
        return "Theocracy", "High Oracle"
    if tribe.religion_scale < LOW_RELIGION_THRESHOLD:
        return "Technocracy", "Chief Technocrat"
    if tribe.social_scale > HIGH_SOCIAL_THRESHOLD:
        return "Collective", "Speaker"
    if tribe.social_scale < LOW_SOCIAL_THRESHOLD:
        return "Autocracy", "Sovereign"
    return "Republic", "Chancellor"


def found_societies(tribes: list[Tribe]) -> list[Tribe]:
    '''Marks the dawn of the Modern Age: each surviving kingdom is reborn as a named society
    with its own leader and government, drawn from its species' naming conventions and stats.'''
    for tribe in tribes:
        terms = get_terms(tribe.species)
        adjective = random.choice(terms["adjectives"])
        noun = random.choice(terms["nouns"])["singular"]
        base_name = _strip_species_suffix(tribe.name)

        tribe.society_name = f"The {adjective} {noun} of {base_name}"
        tribe.leader_name = random_species_name(tribe.species, fallback=f"{tribe.species} Leader")
        tribe.government_type, tribe.leader_title = _determine_government(tribe)
    return tribes


'''The Modern History Phase should have:
- The lowest chance of catastrophic climate events of any age, since modern societies have
  the technology to predict, withstand, and recover from disaster — though their planet-spanning
  reach means any event that does strike touches more land and more people
- The highest chance of societal events of any age, reflecting the speed of change in modern
  society: economic booms and megastructures, doctrinal schisms and technocratic revolutions,
  civil unrest and leadership crises
- Conflicts between societies in contact are driven less by raw resources and more by
  ideology — clashing government types spark conflicts that weaken rather than annihilate
- The lowest chance of spontaneous unions of any age; societies instead merge through
  deliberate federation when their governments and outlooks align
'''
class ModernHistoryPhase(SimulationPhase):

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
                            tribe.strength *= random.uniform(0.5, 0.8)
                            if tribe.strength < TRIBE_ELIMINATION_THRESHOLD:
                                tribe.is_eliminated = True
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.society_name, planet=planet.name, outcome="destroyed"))
                            else:
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.society_name, planet=planet.name, outcome="affected"))

            elif event_type in ["Hurricane", "Drought", "Flood"]:
                if random.random() < WEATHER_EVENT_CHANCE:
                    events.append(HistoryEvent(category="climate", event_type=event_type, tick=tick, planet=planet.name))
                    radius = random.randint(WEATHER_EVENT_RADIUS_MIN, WEATHER_EVENT_RADIUS_MAX)
                    for tribe in tribes:
                        distance = sqrt((tribe.location[0] - location_xy[0]) ** 2 + (tribe.location[1] - location_xy[1]) ** 2)
                        if distance < radius and tribe.home_planet == planet:
                            tribe.strength *= random.uniform(0.75, 0.97)
                            if tribe.strength < TRIBE_ELIMINATION_THRESHOLD:
                                tribe.is_eliminated = True
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.society_name, planet=planet.name, outcome="destroyed"))
                            else:
                                events.append(HistoryEvent(category="climate_tribe", event_type=event_type, tick=tick, tribe=tribe.society_name, planet=planet.name, outcome="affected"))
        return events

    def create_societal_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        events = []
        if random.random() < SOCIETAL_EVENT_CHANCE:
            for tribe in tribes:
                if tribe.resource_trait == ResourceTrait.POOR or tribe.strength < POOR_STRENGTH_THRESHOLD:
                    event_type = random.choice(["Resource Crisis", "Civil Unrest", "Economic Collapse"])
                    tribe.strength *= random.uniform(0.5, 0.9)

                elif tribe.resource_trait == ResourceTrait.RICH and tribe.strength >= RICH_STRENGTH_THRESHOLD:
                    event_type = random.choice(["Technological Breakthrough", "Economic Boom", "Megastructure Completed"])
                    tribe.technology *= random.uniform(1.1, 1.5)
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.05, 1.2)
                    tribe.size *= random.uniform(1.05, 1.25)

                elif tribe.religion_scale > HIGH_RELIGION_THRESHOLD:
                    event_type = random.choice(["Fundamentalist Uprising", "Doctrinal Schism"])
                    tribe.religion_scale += random.uniform(-0.2, 0.2)
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(0.95, 1.15)

                elif tribe.religion_scale < LOW_RELIGION_THRESHOLD:
                    event_type = random.choice(["Technocratic Revolution", "Secular Uprising"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.technology *= random.uniform(1.1, 1.3)

                elif tribe.social_scale > HIGH_SOCIAL_THRESHOLD:
                    event_type = random.choice(["Syndicate Expansion", "Collective Mobilization"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.05, 1.2)
                    tribe.size *= random.uniform(1.0, 1.15)

                else:
                    event_type = random.choice(["Leadership Crisis", "Political Coup"])
                    tribe.social_scale += random.uniform(-0.2, 0.2)
                    tribe.strength *= random.uniform(0.5, 0.9)

                if tribe.strength < TRIBE_ELIMINATION_THRESHOLD:
                    tribe.is_eliminated = True
                    events.append(HistoryEvent(category="societal", event_type=event_type, tick=tick, tribe=tribe.society_name, outcome="destroyed"))
                else:
                    events.append(HistoryEvent(category="societal", event_type=event_type, tick=tick, tribe=tribe.society_name, outcome="survived"))

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
                        events.append(HistoryEvent(category="conflict", event_type="resource", tick=tick, tribe=stronger.society_name, enemy=weaker.society_name, planet=stronger.home_planet.name, outcome="won"))
                        weaker.strength *= random.uniform(0.4, 0.9)
                        stronger.resource_trait = ResourceTrait.RICH
                        weaker.resource_trait = ResourceTrait.POOR
                        if weaker.strength < TRIBE_ELIMINATION_THRESHOLD:
                            weaker.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=weaker.society_name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=weaker.society_name, outcome="weakened"))
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="resource", tick=tick, tribe=weaker.society_name, enemy=stronger.society_name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(0.4, 0.9)
                        weaker.resource_trait = ResourceTrait.RICH
                        stronger.resource_trait = ResourceTrait.POOR
                        if stronger.strength < TRIBE_ELIMINATION_THRESHOLD:
                            stronger.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=stronger.society_name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=stronger.society_name, outcome="weakened"))
                continue

            if tribe1.government_type != tribe2.government_type:
                if random.random() < IDEOLOGICAL_CONFLICT_CHANCE:
                    stronger = tribe1 if tribe1.strength > tribe2.strength else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    strength_diff = abs(tribe1.strength - tribe2.strength)
                    win_chance = 0.5 + (strength_diff / 2)

                    if random.random() < win_chance:
                        events.append(HistoryEvent(category="conflict", event_type="ideological", tick=tick, tribe=stronger.society_name, enemy=weaker.society_name, planet=stronger.home_planet.name, outcome="won"))
                        weaker.strength *= random.uniform(0.4, 0.9)
                        if weaker.strength < TRIBE_ELIMINATION_THRESHOLD:
                            weaker.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="ideological", tick=tick, tribe=weaker.society_name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="ideological", tick=tick, tribe=weaker.society_name, outcome="weakened"))
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="ideological", tick=tick, tribe=weaker.society_name, enemy=stronger.society_name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(0.4, 0.9)
                        if stronger.strength < TRIBE_ELIMINATION_THRESHOLD:
                            stronger.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="ideological", tick=tick, tribe=stronger.society_name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="ideological", tick=tick, tribe=stronger.society_name, outcome="weakened"))
                continue

            if abs(tribe1.social_scale - tribe2.social_scale) < FEDERATION_SOCIAL_THRESHOLD and tribe1.resource_trait == tribe2.resource_trait:
                if random.random() < FEDERATION_CHANCE:
                    stronger = tribe1 if tribe1.size > tribe2.size else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    stronger.size += weaker.size
                    stronger.strength += weaker.strength
                    stronger.technology += weaker.technology

                    weaker.is_eliminated = True
                    events.append(HistoryEvent(category="merge", event_type="federation", tick=tick, tribe=stronger.society_name, enemy=weaker.society_name, planet=stronger.home_planet.name))
                continue

        return events
