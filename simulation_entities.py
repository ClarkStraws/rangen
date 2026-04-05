from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum, auto
from abc import ABC, abstractmethod
from settings import MAP_WIDTH, MAP_HEIGHT
from entities import Tribe, Planet, ResourceTrait
from math import sqrt
import random

@dataclass
class SimulationResult:
    tribes: list        # mutated tribe states
    history: list[str]  # event log for narrative
    survivors: list     # tribes that made it through
    eliminated: list    # tribes that didn't


class SimulationPhase(ABC):

    @abstractmethod
    def apply_passive_events(self, tribes: list[Tribe]) -> list[str]:
        '''Apply passive events (e.g. climate, societal) to all tribes and return event log entries.'''
        ...
    
    @abstractmethod
    def run_interactions(self, tribes: list[Tuple[Tribe, Tribe]]) -> list[str]:
        '''Run interactions between tribes and return event log entries.'''
        ...
    
    @abstractmethod
    def generate_contact_events(self, tribes: list[Tribe]) -> list[Tuple[Tribe, Tribe]]:
        '''Generate contact events between tribes and return event log entries.'''
        ...

    def run(self, tribes: list[Tribe], ticks: int = 10) -> SimulationResult:
        """Shared simulation loop — identical across all phases."""
        history = []
        eliminated = []

        contacted_tribes = self.generate_contact_events(tribes)
        for tribe1, tribe2 in contacted_tribes:
            print(f"Contact event: {tribe1.name} and {tribe2.name} on {tribe1.home_planet.name}")

        for tick in range(ticks):

            history.append(f"--- Tick {tick + 1} ---")

            events = self.apply_passive_events(tribes)
            history.extend(events)

            history.extend(self.run_interactions(contacted_tribes))
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
        
    def create_climate_events(self, tribes: list[Tribe]) -> list[str]:
        planets = []
        for tribe in tribes:
            if tribe.home_planet not in planets:
                planets.append(tribe.home_planet)
        
        event_log = []
        for planet in planets:
            event_type = random.choice(["Meteor", "Volcano", "Earthquake", "Tsunami", "Hurricane", "Drought", "Flood"])
            location_xy = (int(random.uniform(0, MAP_WIDTH)), int(random.uniform(0, MAP_HEIGHT)))

            if event_type in ["Meteor", "Volcano", "Earthquake", "Tsunami"]:
                if random.random() < 0.1:
                    event_log.append(f"A {event_type} occurred on {planet.name}, causing widespread devastation")
                    radius = random.randint(150, 350)
                    for tribe in tribes:
                        distance = sqrt((tribe.location[0] - location_xy[0]) ** 2 + (tribe.location[1] - location_xy[1]) ** 2)
                        if distance < radius and tribe.home_planet == planet:
                            tribe.strength *= random.uniform(0.25, 0.5) # reduce strength of affected tribes
                            if tribe.strength < 0.1:
                                tribe.is_eliminated = True
                                event_log.append(f"{tribe.name} was destroyed")
                            else:
                                event_log.append(f"{tribe.name} was affected")

            elif event_type in ["Hurricane", "Drought", "Flood"]:
                if random.random() < 0.3:
                    event_log.append(f"A {event_type} occurred on {planet.name}, causing significant disruption")
                    radius = random.randint(50, 120)
                    for tribe in tribes:
                        distance = sqrt((tribe.location[0] - location_xy[0]) ** 2 + (tribe.location[1] - location_xy[1]) ** 2)
                        if distance < radius and tribe.home_planet == planet:
                            tribe.strength *= random.uniform(0.5, 0.9) # reduce strength of affected tribes
                            if tribe.strength < 0.1:
                                tribe.is_eliminated = True
                                event_log.append(f"{tribe.name} was destroyed")
                            else:
                                event_log.append(f"{tribe.name} was affected")
        return event_log

    def create_societal_events(self, tribes: list[Tribe]) -> list[str]:
        event_log = []
        ### determine if anything happens
        if random.random() < 0.2:  # 20% chance of societal event each tick
            for tribe in tribes:
                if tribe.resource_trait == ResourceTrait.POOR or tribe.strength < 0.5:
                    event_type = random.choice(["Famine", "Plague", "Rebellion"])
                    tribe.strength *= random.uniform(0.5, 0.9) # reduce strength of affected tribe
                
                elif tribe.resource_trait == ResourceTrait.RICH and tribe.strength >= 0.75:
                    event_type = random.choice(["Technological Breakthrough", "Cultural Renaissance"])
                    tribe.technology *= random.uniform(1.1, 1.5) # increase technology of affected tribe
                    tribe.social_scale += random.uniform(-0.1, 0.1) # small random shift in social scale
                    tribe.strength *= random.uniform(1.05, 1.2) # increase strength of affected tribe
                    tribe.size *= random.uniform(1.05, 1.2) # increase size of affected tribe
                
                elif tribe.religion_scale > 0.5:
                    event_type = random.choice(["Religious Schism", "New Religion Founded"])
                    tribe.religion_scale += random.uniform(-0.2, 0.2) # shift religion scale in either direction
                    tribe.social_scale += random.uniform(-0.1, 0.1) # small random shift in social scale
                
                elif tribe.religion_scale < -0.5:
                    event_type = random.choice(["Secular Uprising", "Philosophical Breakthrough"])
                    tribe.social_scale += random.uniform(-0.1, 0.1) # small random shift in social scale
                    tribe.technology *= random.uniform(1.05, 1.2) # increase technology of affected tribe
                
                elif tribe.social_scale > 0.5:
                    event_type = random.choice(["Collective Movement", "Social Reform"])
                    tribe.social_scale += random.uniform(-0.1, 0.1) # small random shift in social scale
                    tribe.strength *= random.uniform(1.05, 1.2) # increase
                
                else:
                    event_type = "Civil War"
                    tribe.social_scale += random.uniform(-0.2, 0.2) # larger random shift in social scale
                    tribe.strength *= random.uniform(0.1, 0.5) # reduce significantly the strength of affected tribe
                
                if tribe.strength < 0.1:
                    tribe.is_eliminated = True
                    event_log.append(f"{tribe.name} was destroyed by {event_type}")
                else:
                    event_log.append(f"{tribe.name} experienced {event_type}")
                
        return event_log

    def apply_passive_events(self, tribes: list[Tribe]) -> list[str]:
        climate_event_log = self.create_climate_events(tribes)

        societal_event_log = self.create_societal_events(tribes)

        return climate_event_log + societal_event_log

    def run_interactions(self, tribes: list[Tuple[Tribe, Tribe]]) -> list[str]:
        
        ### First we'll do conflict events for connected tribes
        event_log = []
        for tribe1, tribe2 in tribes:
            if tribe1.is_eliminated or tribe2.is_eliminated:
                continue
            
            ### resource conflict if tribes have different resource traits
            if tribe1.resource_trait != tribe2.resource_trait:
                if random.random() < 0.6:  # 60% chance of conflict if resource traits differ
                    stronger = tribe1 if tribe1.strength > tribe2.strength else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    strength_diff = abs(tribe1.strength - tribe2.strength)
                    win_chance = 0.5 + (strength_diff / 2)  # stronger tribe has higher chance to win

                    if random.random() < win_chance:
                        event_log.append(f"{stronger.name} defeated {weaker.name} in a conflict over resources on {stronger.home_planet.name}")
                        weaker.strength *= random.uniform(0.1, 0.9) # reduce strength of weaker tribe significantly
                        stronger.resource_trait = ResourceTrait.RICH  # winner gains access to better resources
                        weaker.resource_trait = ResourceTrait.POOR  # loser loses access to resources
                        if weaker.strength < 0.1:
                            weaker.is_eliminated = True
                            event_log.append(f"{weaker.name} was destroyed in the conflict")
                        else:
                            event_log.append(f"{weaker.name} was weakened in the conflict")
                    else:
                        event_log.append(f"{weaker.name} defended against {stronger.name} in a conflict over resources on {weaker.home_planet.name}")
                        stronger.strength *= random.uniform(0.1, 0.9) # reduce strength of stronger tribe significantly
                        weaker.resource_trait = ResourceTrait.RICH  # defender gains access to better resources
                        stronger.resource_trait = ResourceTrait.POOR  # attacker loses access to resources
                        if stronger.strength < 0.1:
                            stronger.is_eliminated = True
                            event_log.append(f"{stronger.name} was destroyed in the conflict")
                        else:
                            event_log.append(f"{stronger.name} was weakened in the conflict")
                continue  # if they had a resource conflict, skip to next pair of tribes
                

            ### religious conflict if tribes have different religion scales
            if abs(tribe1.religion_scale - tribe2.religion_scale) > .45:  # arbitrary threshold for religious conflict  
                if random.random() < 0.5:  # 50% chance of conflict if religion scales differ
                    stronger = tribe1 if tribe1.strength > tribe2.strength else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    religion_diff = abs(tribe1.religion_scale - tribe2.religion_scale)
                    win_chance = 0.5 + (religion_diff / 2)  # stronger tribe has higher chance to win

                    # religious conflicts aren't about resources so they average out
                    weaker.resource_trait = ResourceTrait.AVERAGE
                    stronger.resource_trait = ResourceTrait.AVERAGE

                    if random.random() < win_chance:
                        event_log.append(f"{stronger.name} defeated {weaker.name} in a conflict over religion on {stronger.home_planet.name}")
                        weaker.strength *= random.uniform(0.1, 0.9) # reduce strength of weaker tribe significantly
                        if weaker.strength < 0.1:
                            weaker.is_eliminated = True
                            event_log.append(f"{weaker.name} was destroyed in the conflict")
                        else:
                            event_log.append(f"{weaker.name} was weakened in the conflict")
                    else:
                        event_log.append(f"{weaker.name} defended against {stronger.name} in a conflict over religion on {weaker.home_planet.name}")
                        stronger.strength *= random.uniform(0.1, 0.9) # reduce strength of stronger tribe significantly
                        if stronger.strength < 0.1:
                            stronger.is_eliminated = True
                            event_log.append(f"{stronger.name} was destroyed in the conflict")
                        else:
                            event_log.append(f"{stronger.name} was weakened in the conflict")
                continue  # if they had a religious conflict, skip to next pair of tribes

            ### merge if tribes have similar social scales and resource traits
            if abs(tribe1.social_scale - tribe2.social_scale) < 0.25 and tribe1.resource_trait == tribe2.resource_trait:
                if random.random() < 0.5:  # 50% chance of merge if social scales are similar
                    stronger = tribe1 if tribe1.size > tribe2.size else tribe2
                    weaker = tribe2 if stronger == tribe1 else tribe1

                    stronger.size += weaker.size
                    stronger.strength += weaker.strength
                    stronger.technology += weaker.technology

                    weaker.is_eliminated = True
                    event_log.append(f"{stronger.name} merged with {weaker.name} on {stronger.home_planet.name}")
                continue  # if they merged, skip to next pair of tribes
        
        return event_log