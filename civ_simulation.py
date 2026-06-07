from entities import Tribe, HistoryEvent, SimulationResult
from ancient_simulation import AncientHistoryPhase
from middle_age_simulation import MiddleHistoryPhase, grow_surviving_tribes


def print_tribe_states(label: str, tribes: list[Tribe]) -> None:
    print(f"\n{label}:")
    for tribe in tribes:
        print(f" - {tribe.name}: Strength={tribe.strength:.2f}, Size={tribe.size:.2f}")
        print(f"   Resource Trait: {tribe.resource_trait}, Social Scale: {tribe.social_scale:.2f}, Technology: {tribe.technology:.2f}, Religion Scale: {tribe.religion_scale:.2f}")


def simulate_history(tribes: list[Tribe], ticks: int) -> SimulationResult:
    ancient_history = AncientHistoryPhase()
    ancient_result = ancient_history.run(tribes, ticks=ticks)
    print_tribe_states("Final Tribe States (Ancient Phase)", ancient_result.tribes)

    # Tribes that survived the ancient world grow into kingdoms — larger, stronger, and able
    # to make contact across the longer distances the middle ages call for — before their
    # history continues into the next phase.
    middle_age_tribes = grow_surviving_tribes(ancient_result.survivors)
    era_transition = HistoryEvent(category="era", event_type="middle_ages", tick=0)

    middle_history = MiddleHistoryPhase()
    middle_result = middle_history.run(middle_age_tribes, ticks=ticks)
    print_tribe_states("Final Tribe States (Middle Ages)", middle_result.tribes)

    return SimulationResult(
        tribes=middle_result.tribes,
        history=ancient_result.history + [era_transition] + middle_result.history,
        survivors=middle_result.survivors,
        eliminated=ancient_result.eliminated + middle_result.eliminated,
    )
