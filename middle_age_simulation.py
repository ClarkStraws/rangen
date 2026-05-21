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
)
from entities import Tribe, Planet, ResourceTrait, HistoryEvent, SimulationPhase, SimulationResult
from math import sqrt
import random


'''The Middle History Phase should have: 

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
        events = []
        return events

    def create_societal_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        events = []
        return events

    def apply_passive_events(self, tribes: list[Tribe], tick: int) -> list[HistoryEvent]:
        return self.create_climate_events(tribes, tick) + self.create_societal_events(tribes, tick)

    def run_interactions(self, tribes: list[Tuple[Tribe, Tribe]], tick: int) -> list[HistoryEvent]:
        events = []
        return events