from entities import Tribe
from simulation_entities import AncientHistoryPhase, SimulationResult


def simulate_history(tribes: list[Tribe], ticks: int) -> SimulationResult:
    ancient_history = AncientHistoryPhase()
    result = ancient_history.run(tribes, ticks=ticks)

    print("\nFinal Tribe States:")
    for tribe in result.tribes:
        print(f" - {tribe.name}: Strength={tribe.strength:.2f}, Size={tribe.size:.2f}")
        print(f"   Resource Trait: {tribe.resource_trait}, Social Scale: {tribe.social_scale:.2f}, Technology: {tribe.technology:.2f}, Religion Scale: {tribe.religion_scale:.2f}")

    return result
