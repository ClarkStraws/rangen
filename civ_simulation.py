from math import sqrt
import random
from typing import Tuple
from entities import LifeForm, Tribe, Planet
from simulation_entities import AncientHistoryPhase

def simulate_history(tribes: list[Tribe], ticks: int) -> None:

    ancient_history = AncientHistoryPhase()
    result = ancient_history.run(tribes, ticks=10)
    print("Ancient History Simulation Result:")
    for event in result.history:
        if event:
            print(event)

    print("\nFinal Tribe States:")
    for tribe in result.tribes:
        print(f" - {tribe.name}: Strength={tribe.strength:.2f}, Size={tribe.size:.2f}")
        print(f"   Resource Trait: {tribe.resource_trait}, Social Scale: {tribe.social_scale:.2f}, Technology: {tribe.technology:.2f}, Religion Scale: {tribe.religion_scale:.2f}")