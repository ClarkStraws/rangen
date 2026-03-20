from math import sqrt
import random
from typing import Tuple
from entities import LifeForm, Tribe, Planet
from settings import MAP_HEIGHT, MAP_WIDTH

events = ["Contact", "Conflict_Resources", "Conflict_Religions", "Merge", "Climate", "Societal"]


def calculate_event_result(tribe1: Tribe, tribe2: Tribe, event_type: str) -> Tuple[Tribe, Tribe, str]:
    if event_type == "Contact":
        if sqrt(abs(tribe1.location[0] - tribe2.location[0]) ** 2 + abs(tribe1.location[1] - tribe2.location[1]) ** 2) < 50:
                    # Simulate contact event between tribe i and tribe j
                    event = f"{tribe1.name} made contact with {tribe2.name} on {tribe1.home_planet.name}"
        else:
            event = ""
        return tribe1, tribe2, event
    
    elif event_type == "Conflict_Resources":
        ### weighted so richer soceities are more likely to succeed
        winner = tribe1 if random.random() < (tribe1.resource_trait.value / (tribe1.resource_trait.value + tribe2.resource_trait.value)) else tribe2
        loser = tribe2 if winner == tribe1 else tribe1

        event = f"{tribe1.name} and {tribe2.name} had a conflict over resources on {tribe1.home_planet.name} and {winner.name} won"
        return winner, loser, event
    
    elif event_type == "Conflict_Religions":
        ### no weight, just random
        winner = tribe1 if random.random() < .5 else tribe2
        loser = tribe2 if winner == tribe1 else tribe1

        event = f"{tribe1.name} and {tribe2.name} had a conflict over religion on {tribe1.home_planet.name} and {winner.name} won"
        return winner, loser, event
    
    elif event_type == "Merge":
        winner = tribe1 if random.random() < (0.5 + (0.25 * (1 - abs(tribe1.social_scale - tribe2.social_scale)))) else tribe2

        loser = tribe2 if winner == tribe1 else tribe1

        return winner, loser, f"{tribe1.name} and {tribe2.name} merged on {tribe1.home_planet.name} to form {winner.name}"
    
    elif event_type == "Climate":
        return tribe1, tribe2, f"{tribe1.name} experienced a climate event on {tribe1.home_planet.name}"

    elif event_type == "Societal":
        return tribe1, tribe2, f"{tribe1.name} experienced a societal event on {tribe1.home_planet.name}"

    else:
        raise ValueError(f"Unknown event type: {event_type}")


def create_climate_event(tribes: list[Tribe], planet: Planet) -> Tuple[list[Tribe], list[Tribe], str]:
    event_type = random.choice(["Meteor", "Volcano", "Earthquake", "Tsunami", "Hurricane", "Drought", "Flood"])
    event_str = ""
    location_xy = (int(random.uniform(0, MAP_WIDTH)), int(random.uniform(0, MAP_HEIGHT)))
    tribes_destroyed = []
    tribes_affected = []
    ### weighted so that more severe events are less likely
    if event_type in ["Meteor", "Volcano", "Earthquake", "Tsunami"]:
        if random.random() < 0.1:
            event_str = f"A {event_type} occurred on {planet.name}, causing widespread devastation"
            radius = random.randint(10, 350)
            for tribe in tribes:
                if sqrt((tribe.location[0] - location_xy[0]) ** 2 + (tribe.location[1] - location_xy[1]) ** 2) < radius:
                    tribe.strength *= random.uniform(0.5, 0.9) # reduce strength of affected tribes
                    if tribe.strength < 0.1:
                        tribes_destroyed.append(tribe)
                        event_str += f" and {tribe.name} was destroyed"
                    else:
                        event_str += f" and {tribe.name} was affected"
                        tribes_affected.append(tribe)

    elif event_type in ["Hurricane", "Drought", "Flood"]:
        if random.random() < 0.3:
            event_str = f"A {event_type} occurred on {planet.name}, causing significant disruption"
            radius = random.randint(10, 120)
            for tribe in tribes:
                if sqrt((tribe.location[0] - location_xy[0]) ** 2 + (tribe.location[1] - location_xy[1]) ** 2) < radius:
                    tribe.strength *= random.uniform(0.25, 0.75) # reduce strength of affected tribes
                    if tribe.strength < 0.1:
                        tribes_destroyed.append(tribe)
                        event_str += f" and {tribe.name} was destroyed"
                    else:
                        event_str += f" and {tribe.name} was affected"
                        tribes_affected.append(tribe)

    return tribes_destroyed, tribes_affected, event_str
    
def ancient_history_simulation(tribes: list[Tribe]) -> None:
    ancient_history = []
    connected_tribes = []
    to_remove = []
    ### Contact Events
    for i in tribes:
        for j in tribes:
            if i != j:
                result = calculate_event_result(i, j, "Contact")
                if result and result[2] != "" and (i, j) not in connected_tribes and (j, i) not in connected_tribes:
                    ancient_history.append(result)
                    connected_tribes.append((i, j))
    ### Conflict Events (for connnected tribes)
    if len(connected_tribes) > 0:
        for i in connected_tribes:
            if i[0].resource_trait != i[1].resource_trait:
                result = calculate_event_result(i[0], i[1], "Conflict_Resources")
                if result:
                    ancient_history.append(result)
                    if result[0] == i[0]: # if tribe1 won
                        i[0].strength *= 1.1
                        i[1].strength *= 0.9
                    else:
                        i[1].strength *= 1.1
                        i[0].strength *= 0.9
                        

            if abs(i[0].religion_scale - i[1].religion_scale) > 0.5:
                result = calculate_event_result(i[0], i[1], "Conflict_Religions")
                if result:
                    ancient_history.append(result)
                    if result[0] == i[0]: # if tribe1 won
                        i[0].strength *= 1.1
                        i[1].strength *= 0.9
                    else:
                        i[1].strength *= 1.1
                        i[0].strength *= 0.9

    ### Merge Events
    for i in connected_tribes:
        if i[0].resource_trait == i[1].resource_trait and abs(i[0].social_scale - i[1].social_scale) < 0.25:
            result = calculate_event_result(i[0], i[1], "Merge")
            if result:
                ancient_history.append(result)
                if result[0] == i[0]: # if tribe1 won
                    if result[1].social_scale < result[0].social_scale:
                        to_remove.append(i[1]) # remove the merged tribe

                else:
                    if result[0].social_scale < result[1].social_scale:
                        to_remove.append(i[0]) # remove the merged tribe
    ### Climate Events
    planets = []
    for tribe in tribes:
        if tribe.home_planet not in planets:
            planets.append(tribe.home_planet)

    for planet in planets:
        climate_event = create_climate_event(tribes, planet)
        to_remove.extend(climate_event[0])
        ancient_history.append(climate_event)
    ### Societal Events
    ### TODO: Finish societal events - could be things like plagues, technological breakthroughs, etc. that randomly affect tribes

    ### Remove merged tribes
    for tribe in to_remove:
        if tribe in tribes:
            tribes.remove(tribe)
    print("Ancient History Simulation Results:")
    for event in ancient_history:
        if event[2] != "":
            print(event[2])

    for tribe in tribes:
        print(f"{tribe.name} on {tribe.home_planet.name} has strength {tribe.strength:.2f}")