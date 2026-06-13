from entities import Tribe, HistoryEvent, SimulationResult
from ancient_simulation import AncientHistoryPhase
from middle_age_simulation import MiddleHistoryPhase, grow_surviving_tribes
from modern_age_simulation import ModernHistoryPhase, industrialize_surviving_tribes, found_societies
from future_age_simulation import FutureHistoryPhase, advance_surviving_societies


def print_tribe_states(label: str, tribes: list[Tribe]) -> None:
    print(f"\n{label}:")
    for tribe in tribes:
        print(f" - {tribe.name}: Strength={tribe.strength:.2f}, Size={tribe.size:.2f}")
        print(f"   Resource Trait: {tribe.resource_trait}, Social Scale: {tribe.social_scale:.2f}, Technology: {tribe.technology:.2f}, Religion Scale: {tribe.religion_scale:.2f}")


def print_society_states(label: str, tribes: list[Tribe]) -> None:
    print(f"\n{label}:")
    for tribe in tribes:
        print(f" - {tribe.society_name}: {tribe.government_type} led by {tribe.leader_title} {tribe.leader_name}")
        print(f"   Strength={tribe.strength:.2f}, Size={tribe.size:.2f}, Technology={tribe.technology:.2f}")


def simulate_history(tribes: list[Tribe], ticks: int) -> SimulationResult:
    ancient_history = AncientHistoryPhase()
    ancient_result = ancient_history.run(tribes, ticks=ticks)
    print_tribe_states("Final Tribe States (Ancient Phase)", ancient_result.tribes)

    # Tribes that survived the ancient world grow into kingdoms — larger, stronger, and able
    # to make contact across the longer distances the middle ages call for — before their
    # history continues into the next phase.
    middle_age_tribes = grow_surviving_tribes(ancient_result.survivors)
    middle_era_transition = HistoryEvent(category="era", event_type="middle_ages", tick=0)

    middle_history = MiddleHistoryPhase()
    middle_result = middle_history.run(middle_age_tribes, ticks=ticks)
    print_tribe_states("Final Tribe States (Middle Ages)", middle_result.tribes)

    # Kingdoms that survived the middle ages industrialize into modern societies, each founded
    # under a named leader and government before their history continues into the final phase.
    modern_tribes = industrialize_surviving_tribes(middle_result.survivors)
    found_societies(modern_tribes)
    modern_era_transition = HistoryEvent(category="era", event_type="modern_age", tick=0)
    founding_events = [
        HistoryEvent(category="society", event_type="founded", tick=0, tribe=t.society_name, planet=t.home_planet.name,
                      leader=f"{t.leader_title} {t.leader_name}", government=t.government_type)
        for t in modern_tribes
    ]

    modern_history = ModernHistoryPhase()
    modern_result = modern_history.run(modern_tribes, ticks=ticks)
    print_society_states("Final Society States (Modern Age)", modern_result.tribes)

    # Societies that survived the modern age push beyond it into the future age, where
    # breakthroughs in AI and science are within reach — along with the dangers they bring.
    future_tribes = advance_surviving_societies(modern_result.survivors)
    future_era_transition = HistoryEvent(category="era", event_type="future_age", tick=0)

    future_history = FutureHistoryPhase()
    future_result = future_history.run(future_tribes, ticks=ticks)
    print_society_states("Final Society States (Future Age)", future_result.tribes)

    epilogue_events = [
        HistoryEvent(category="epilogue", event_type="survivor", tick=0, tribe=t.society_name, planet=t.home_planet.name,
                      leader=f"{t.leader_title} {t.leader_name}", government=t.government_type)
        for t in future_result.survivors
    ]

    return SimulationResult(
        tribes=future_result.tribes,
        history=(
            ancient_result.history
            + [middle_era_transition] + middle_result.history
            + [modern_era_transition] + founding_events + modern_result.history
            + [future_era_transition] + future_result.history + epilogue_events
        ),
        survivors=future_result.survivors,
        eliminated=ancient_result.eliminated + middle_result.eliminated + modern_result.eliminated + future_result.eliminated,
    )
