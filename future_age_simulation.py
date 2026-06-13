from typing import List, Tuple
from future_phase_settings import (
    TRIBE_CONTACT_DISTANCE, TRIBE_ELIMINATION_THRESHOLD,
    CATASTROPHIC_EVENT_CHANCE, WEATHER_EVENT_CHANCE,
    CATASTROPHIC_EVENT_RADIUS_MIN, CATASTROPHIC_EVENT_RADIUS_MAX,
    WEATHER_EVENT_RADIUS_MIN, WEATHER_EVENT_RADIUS_MAX,
    SOCIETAL_EVENT_CHANCE,
    POOR_STRENGTH_THRESHOLD, RICH_STRENGTH_THRESHOLD,
    HIGH_RELIGION_THRESHOLD, LOW_RELIGION_THRESHOLD,
    HIGH_SOCIAL_THRESHOLD,
    BASE_CATASTROPHE_CHANCE, MAX_CATASTROPHE_CHANCE,
    CATASTROPHE_SEVERITY_MIN, CATASTROPHE_SEVERITY_MAX,
    RESOURCE_CONFLICT_CHANCE, NUCLEAR_CONFLICT_CHANCE,
    NUCLEAR_SEVERITY_MIN, NUCLEAR_SEVERITY_MAX,
    UNIFICATION_CHANCE, UNIFICATION_SOCIAL_THRESHOLD,
    SURVIVOR_SIZE_GROWTH_MIN, SURVIVOR_SIZE_GROWTH_MAX,
    SURVIVOR_STRENGTH_GROWTH_MIN, SURVIVOR_STRENGTH_GROWTH_MAX, SURVIVOR_STRENGTH_RECOVERY_FLOOR,
    SURVIVOR_TECHNOLOGY_GROWTH_MIN, SURVIVOR_TECHNOLOGY_GROWTH_MAX,
)
from entities import Tribe, ResourceTrait, HistoryEvent, SimulationPhase
from settings import MAP_WIDTH, MAP_HEIGHT
from math import sqrt
import random


def advance_surviving_societies(tribes: list[Tribe]) -> list[Tribe]:
    '''Carries modern-age survivors into the future age: the generations between ages bring
    one final leap forward — larger populations, sturdier defenses, and a surge in technology
    that opens the door to the breakthroughs (and the dangers) of this final age.'''
    for tribe in tribes:
        tribe.size *= random.uniform(SURVIVOR_SIZE_GROWTH_MIN, SURVIVOR_SIZE_GROWTH_MAX)
        tribe.strength = max(tribe.strength, SURVIVOR_STRENGTH_RECOVERY_FLOOR) * random.uniform(SURVIVOR_STRENGTH_GROWTH_MIN, SURVIVOR_STRENGTH_GROWTH_MAX)
        tribe.technology *= random.uniform(SURVIVOR_TECHNOLOGY_GROWTH_MIN, SURVIVOR_TECHNOLOGY_GROWTH_MAX)
    return tribes


'''The Future History Phase should have:
- The lowest chance of catastrophic climate events of any age, since planet-spanning
  societies have the means to predict and shield against natural disaster
- A high chance of societal events, split between two extremes: societies on the rise
  unlock breakthroughs in artificial intelligence, energy, and genetics, while societies
  in decline fall into energy crises, infrastructure collapse, and rogue factions
- A new, independent risk that scales with a society's own technology: the more a society
  pushes the frontier, the more likely it is to suffer an AI uprising, a scientific disaster,
  or an energy disaster — any of which can easily destroy it outright
- Conflicts between societies with differing governments risk nuclear war, which devastates
  both sides — even the "winner" suffers heavy losses
- The lowest chance of spontaneous unions of any age; societies instead unify deliberately
  when their outlooks and resources align
'''
class FutureHistoryPhase(SimulationPhase):

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
                    event_type = random.choice(["Energy Crisis", "Infrastructure Collapse", "Automation Crisis"])
                    tribe.strength *= random.uniform(0.5, 0.9)

                elif tribe.resource_trait == ResourceTrait.RICH and tribe.strength >= RICH_STRENGTH_THRESHOLD:
                    event_type = random.choice(["Artificial Intelligence Breakthrough", "Energy Breakthrough", "Genetic Mastery"])
                    tribe.technology *= random.uniform(1.3, 2.0)
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.1, 1.3)
                    tribe.size *= random.uniform(1.05, 1.3)

                elif tribe.religion_scale > HIGH_RELIGION_THRESHOLD:
                    event_type = random.choice(["Transcendence Movement", "Digital Awakening"])
                    tribe.religion_scale += random.uniform(-0.2, 0.2)
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(0.95, 1.15)

                elif tribe.religion_scale < LOW_RELIGION_THRESHOLD:
                    event_type = random.choice(["Post-Scarcity Reform", "Rational Expansion"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.technology *= random.uniform(1.1, 1.4)

                elif tribe.social_scale > HIGH_SOCIAL_THRESHOLD:
                    event_type = random.choice(["Network Unification", "Collective Uplift"])
                    tribe.social_scale += random.uniform(-0.1, 0.1)
                    tribe.strength *= random.uniform(1.05, 1.2)
                    tribe.size *= random.uniform(1.0, 1.15)

                else:
                    event_type = random.choice(["Command Crisis", "Rogue Faction Uprising"])
                    tribe.social_scale += random.uniform(-0.2, 0.2)
                    tribe.strength *= random.uniform(0.5, 0.9)

                if tribe.strength < TRIBE_ELIMINATION_THRESHOLD:
                    tribe.is_eliminated = True
                    events.append(HistoryEvent(category="societal", event_type=event_type, tick=tick, tribe=tribe.society_name, outcome="destroyed"))
                else:
                    events.append(HistoryEvent(category="societal", event_type=event_type, tick=tick, tribe=tribe.society_name, outcome="survived"))

        return events

    def create_catastrophe_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        events = []
        for tribe in tribes:
            if tribe.is_eliminated:
                continue
            catastrophe_chance = min(MAX_CATASTROPHE_CHANCE, BASE_CATASTROPHE_CHANCE * tribe.technology)
            if random.random() < catastrophe_chance:
                event_type = random.choice(["AI Uprising", "Scientific Disaster", "Energy Disaster"])
                tribe.strength *= random.uniform(CATASTROPHE_SEVERITY_MIN, CATASTROPHE_SEVERITY_MAX)
                if tribe.strength < TRIBE_ELIMINATION_THRESHOLD:
                    tribe.is_eliminated = True
                    events.append(HistoryEvent(category="catastrophe", event_type=event_type, tick=tick, tribe=tribe.society_name, outcome="destroyed"))
                else:
                    events.append(HistoryEvent(category="catastrophe", event_type=event_type, tick=tick, tribe=tribe.society_name, outcome="survived"))
        return events

    def apply_passive_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        return self.create_climate_events(tribes, tick) + self.create_societal_events(tribes, tick) + self.create_catastrophe_events(tribes, tick)

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
                        weaker.strength *= random.uniform(0.3, 0.9)
                        stronger.resource_trait = ResourceTrait.RICH
                        weaker.resource_trait = ResourceTrait.POOR
                        if weaker.strength < TRIBE_ELIMINATION_THRESHOLD:
                            weaker.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=weaker.society_name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=weaker.society_name, outcome="weakened"))
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="resource", tick=tick, tribe=weaker.society_name, enemy=stronger.society_name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(0.3, 0.9)
                        weaker.resource_trait = ResourceTrait.RICH
                        stronger.resource_trait = ResourceTrait.POOR
                        if stronger.strength < TRIBE_ELIMINATION_THRESHOLD:
                            stronger.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=stronger.society_name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="resource", tick=tick, tribe=stronger.society_name, outcome="weakened"))
                continue

            if tribe1.government_type != tribe2.government_type:
                if random.random() < NUCLEAR_CONFLICT_CHANCE:
                    stronger = tribe1 if tribe1.strength > tribe2.strength else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    strength_diff = abs(tribe1.strength - tribe2.strength)
                    win_chance = 0.5 + (strength_diff / 2)

                    # Nuclear war devastates both sides: the loser bears the worst of it,
                    # but even the side that comes out ahead suffers heavy fallout losses.
                    if random.random() < win_chance:
                        events.append(HistoryEvent(category="conflict", event_type="nuclear_war", tick=tick, tribe=stronger.society_name, enemy=weaker.society_name, planet=stronger.home_planet.name, outcome="won"))
                        weaker.strength *= random.uniform(NUCLEAR_SEVERITY_MIN, NUCLEAR_SEVERITY_MAX)
                        stronger.strength *= random.uniform(0.6, 0.95)
                    else:
                        events.append(HistoryEvent(category="conflict", event_type="nuclear_war", tick=tick, tribe=weaker.society_name, enemy=stronger.society_name, planet=weaker.home_planet.name, outcome="defended"))
                        stronger.strength *= random.uniform(NUCLEAR_SEVERITY_MIN, NUCLEAR_SEVERITY_MAX)
                        weaker.strength *= random.uniform(0.6, 0.95)

                    for tribe in (tribe1, tribe2):
                        if tribe.is_eliminated:
                            continue
                        if tribe.strength < TRIBE_ELIMINATION_THRESHOLD:
                            tribe.is_eliminated = True
                            events.append(HistoryEvent(category="conflict_result", event_type="nuclear_war", tick=tick, tribe=tribe.society_name, outcome="destroyed"))
                        else:
                            events.append(HistoryEvent(category="conflict_result", event_type="nuclear_war", tick=tick, tribe=tribe.society_name, outcome="weakened"))
                continue

            if abs(tribe1.social_scale - tribe2.social_scale) < UNIFICATION_SOCIAL_THRESHOLD and tribe1.resource_trait == tribe2.resource_trait:
                if random.random() < UNIFICATION_CHANCE:
                    stronger = tribe1 if tribe1.size > tribe2.size else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    stronger.size += weaker.size
                    stronger.strength += weaker.strength
                    stronger.technology += weaker.technology

                    weaker.is_eliminated = True
                    events.append(HistoryEvent(category="merge", event_type="unification", tick=tick, tribe=stronger.society_name, enemy=weaker.society_name, planet=stronger.home_planet.name))
                continue

        return events
