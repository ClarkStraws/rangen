import random

CLIMATE_PLANET_TEMPLATES = {
    "Meteor": [
        "A meteor struck {planet}, sending shockwaves across the land.",
        "Fire rained from the sky as a meteor crashed into {planet}.",
        "A blazing rock fell from the heavens and struck {planet} with terrible force.",
        "The sky split open above {planet} as a meteor carved a path of destruction below.",
    ],
    "Volcano": [
        "A great volcano erupted on {planet}, blanketing the region in ash and fire.",
        "The earth split open on {planet} as a massive volcanic eruption tore through the land.",
        "Lava and ash poured from a volcano on {planet}, devastating everything nearby.",
        "The mountain awoke on {planet}, spewing fire and ruin across the surrounding lands.",
    ],
    "Earthquake": [
        "The ground shook without warning on {planet} as a powerful earthquake struck.",
        "A devastating earthquake split the land of {planet}, toppling everything in its path.",
        "Tremors rippled across {planet} as a catastrophic earthquake struck.",
        "The earth beneath {planet} heaved and cracked, leveling all that stood upon it.",
    ],
    "Tsunami": [
        "A great wave rose from the sea and crashed upon the shores of {planet}.",
        "The ocean rose up against {planet} as a massive tsunami destroyed the coastline.",
        "Without warning, a wall of water swept inland across {planet}.",
        "The seas turned against {planet}, sending a catastrophic tsunami crashing ashore.",
    ],
    "Hurricane": [
        "A violent hurricane tore across {planet}, destroying everything in its path.",
        "Howling winds and driving rain battered {planet} as a hurricane made landfall.",
        "The storm season brought a devastating hurricane to {planet}.",
        "A great storm descended upon {planet}, raging with terrible fury.",
    ],
    "Drought": [
        "A relentless drought gripped {planet}, drying up rivers and withering crops.",
        "The rains failed to come on {planet}, and drought spread across the land.",
        "Sun-baked and parched, {planet} suffered a devastating drought.",
        "The wells ran dry and the soil cracked as drought strangled {planet}.",
    ],
    "Flood": [
        "Rivers overflowed their banks on {planet} as a great flood swept through the lowlands.",
        "Torrential rains turned rivers into monsters on {planet}, flooding entire regions.",
        "A catastrophic flood drowned the lowlands of {planet}.",
        "The waters rose on {planet}, swallowing settlements and driving people from their homes.",
    ],
}

CLIMATE_TRIBE_TEMPLATES = {
    "destroyed": [
        "{tribe} was swept away entirely, leaving nothing behind.",
        "The last members of {tribe} perished in the disaster.",
        "{tribe} was obliterated — no survivors remained.",
        "Nothing was left of {tribe} after the catastrophe.",
    ],
    "affected": [
        "{tribe} was battered but survived the catastrophe.",
        "The people of {tribe} suffered greatly but endured.",
        "{tribe} bore the brunt of the disaster, though some survived.",
        "{tribe} emerged from the disaster weakened but alive.",
    ],
}

SOCIETAL_TEMPLATES = {
    "Famine": [
        "A devastating famine swept through {tribe}, leaving many to starve.",
        "Crops failed across {tribe}'s territory, and starvation claimed many lives.",
        "The granaries of {tribe} ran empty as famine gripped the land.",
        "Hunger stalked {tribe} as a terrible famine took hold.",
    ],
    "Plague": [
        "A terrible plague swept through {tribe}, culling the weak and frightening the strong.",
        "Disease spread like wildfire through {tribe}, and death followed close behind.",
        "An unknown sickness claimed many lives in {tribe}, weakening the tribe.",
        "{tribe} was ravaged by a plague that no healer could stop.",
    ],
    "Rebellion": [
        "Discontent boiled over in {tribe} as the people rose against their leaders.",
        "The streets of {tribe} ran with unrest as a rebellion tore through the tribe.",
        "A rebellion shook {tribe} to its core, leaving the leadership scrambling to restore order.",
        "Driven by hunger and injustice, the people of {tribe} staged a violent uprising.",
    ],
    "Technological Breakthrough": [
        "Clever minds within {tribe} unlocked new techniques that changed everything.",
        "An inventor in {tribe} made a discovery that transformed the way the tribe lived.",
        "{tribe} achieved a technological leap that gave them a decisive edge.",
        "A new invention born in {tribe} reshaped the tribe's way of life.",
    ],
    "Cultural Renaissance": [
        "A golden age of art and culture blossomed in {tribe}.",
        "Artists, poets, and thinkers flourished in {tribe}, sparking a cultural awakening.",
        "{tribe} entered a period of great cultural flourishing.",
        "The spirit of creativity seized {tribe}, ushering in a renaissance.",
    ],
    "Religious Schism": [
        "A bitter theological dispute split {tribe} into rival factions.",
        "The priests of {tribe} turned on one another as a schism divided the faith.",
        "Long-simmering religious tensions erupted in {tribe}, fracturing the tribe.",
        "Holy war threatened to consume {tribe} from within as religious schism tore the tribe apart.",
    ],
    "New Religion Founded": [
        "A prophet rose among {tribe}, proclaiming a new faith that spread rapidly.",
        "A visionary in {tribe} founded a new religion that reshaped the tribe's worldview.",
        "The old gods were challenged in {tribe} as a new religion took root.",
        "Sacred fire lit the hearts of {tribe}'s people as a new faith was born.",
    ],
    "Secular Uprising": [
        "The people of {tribe} revolted against religious authority, demanding a secular order.",
        "Priests were driven from power in {tribe} as a secular uprising took hold.",
        "In {tribe}, the old religious order crumbled before a wave of secular sentiment.",
        "A rebellion of reason swept through {tribe}, pushing the clergy from their thrones.",
    ],
    "Philosophical Breakthrough": [
        "A great thinker in {tribe} challenged ancient assumptions and changed how the tribe saw the world.",
        "Philosophers in {tribe} made a conceptual leap that reshaped the tribe's understanding of existence.",
        "New ideas born in {tribe} spread through the tribe like wildfire, transforming everything.",
        "The mind of {tribe} was opened by a philosophical revelation that none had dared voice before.",
    ],
    "Collective Movement": [
        "A powerful sense of shared purpose swept through {tribe}, uniting the people.",
        "The people of {tribe} organized around a common cause, growing stronger together.",
        "{tribe} was gripped by a movement that brought the community together as never before.",
        "A wave of solidarity passed through {tribe}, forging the tribe into one.",
    ],
    "Social Reform": [
        "Leaders in {tribe} enacted sweeping reforms that changed the structure of society.",
        "{tribe} underwent significant social changes as reformers reshaped the old order.",
        "The old ways were challenged in {tribe} as reformers pushed for a new social order.",
        "Change swept through {tribe} as the people demanded — and won — a new way of living.",
    ],
    "Civil War": [
        "{tribe} descended into civil war as factions fought for control.",
        "The tribe of {tribe} tore itself apart in a brutal civil war.",
        "Brothers turned against brothers in {tribe} as civil war erupted.",
        "Internal conflict consumed {tribe} as competing factions waged war on one another.",
    ],
}

SOCIETAL_DESTROYED_TEMPLATES = [
    "{tribe} did not survive the chaos — the tribe was shattered beyond recovery.",
    "The upheaval proved fatal for {tribe}, who collapsed entirely.",
    "{tribe} crumbled under the weight of the crisis and was lost forever.",
    "What began as strife ended in annihilation — {tribe} ceased to exist.",
]

CONFLICT_RESOURCE_WON_TEMPLATES = [
    "{tribe} crushed {enemy} in a brutal struggle for resources on {planet}.",
    "After fierce fighting, {tribe} drove {enemy} from the resource-rich lands of {planet}.",
    "{tribe} emerged victorious from a bitter conflict with {enemy} over the resources of {planet}.",
    "The warriors of {tribe} overwhelmed {enemy} and claimed their lands on {planet}.",
]

CONFLICT_RESOURCE_DEFENDED_TEMPLATES = [
    "{tribe} held firm against the assault of {enemy}, repelling the invaders on {planet}.",
    "Against the odds, {tribe} drove back {enemy}'s forces on {planet}.",
    "{tribe} repelled the attack from {enemy}, defending their lands on {planet}.",
    "The defenders of {tribe} stood their ground and sent {enemy} fleeing on {planet}.",
]

CONFLICT_RELIGIOUS_WON_TEMPLATES = [
    "{tribe} waged a holy war against {enemy} on {planet} and emerged triumphant.",
    "In a clash of faiths, {tribe} overwhelmed {enemy} on {planet}.",
    "{tribe} crushed {enemy} in a religious conflict that shook {planet}.",
    "The righteous fury of {tribe} brought {enemy} to its knees on {planet}.",
]

CONFLICT_RELIGIOUS_DEFENDED_TEMPLATES = [
    "{tribe} held its ground against the religious crusade of {enemy} on {planet}.",
    "The faith of {tribe} proved stronger than the armies of {enemy} on {planet}.",
    "{tribe} repelled the religious onslaught of {enemy} on {planet}.",
    "The devotion of {tribe}'s people turned back the holy warriors of {enemy} on {planet}.",
]

CONFLICT_LOSER_DESTROYED_TEMPLATES = [
    "{tribe} was utterly destroyed — their culture and people lost forever.",
    "Nothing remained of {tribe} after the conflict; the tribe was no more.",
    "{tribe} fell completely, its people absorbed or annihilated.",
    "The defeat was absolute — {tribe} ceased to exist.",
]

CONFLICT_LOSER_WEAKENED_TEMPLATES = [
    "{tribe} limped away from the conflict, badly diminished.",
    "The defeat left {tribe} weakened and struggling to recover.",
    "{tribe} survived the conflict, but only barely.",
    "Battered and broken, {tribe} retreated to lick its wounds.",
]

MERGE_TEMPLATES = [
    "{tribe} and {enemy} found common cause and merged into a single people on {planet}.",
    "After years of proximity, {tribe} absorbed {enemy} on {planet}, growing stronger for it.",
    "The tribes of {tribe} and {enemy} united on {planet}, pooling their strength.",
    "{tribe} welcomed {enemy} into the fold on {planet}, and the two became one.",
]


def render_event(event) -> str:
    ctx = dict(tribe=event.tribe, enemy=event.enemy, planet=event.planet)

    if event.category == "tick":
        return f"\n=== Age {event.tick} ==="

    elif event.category == "climate":
        templates = CLIMATE_PLANET_TEMPLATES.get(event.event_type, [f"A {{event.event_type}} occurred on {{planet}}."])
        return random.choice(templates).format(**ctx)

    elif event.category == "climate_tribe":
        templates = CLIMATE_TRIBE_TEMPLATES.get(event.outcome, ["{tribe} was affected."])
        return random.choice(templates).format(**ctx)

    elif event.category == "societal":
        if event.outcome == "destroyed":
            templates = SOCIETAL_DESTROYED_TEMPLATES
        else:
            templates = SOCIETAL_TEMPLATES.get(event.event_type, [f"{{tribe}} experienced {event.event_type}."])
        return random.choice(templates).format(**ctx)

    elif event.category == "conflict":
        if event.event_type == "resource":
            templates = CONFLICT_RESOURCE_WON_TEMPLATES if event.outcome == "won" else CONFLICT_RESOURCE_DEFENDED_TEMPLATES
        else:
            templates = CONFLICT_RELIGIOUS_WON_TEMPLATES if event.outcome == "won" else CONFLICT_RELIGIOUS_DEFENDED_TEMPLATES
        return random.choice(templates).format(**ctx)

    elif event.category == "conflict_result":
        templates = CONFLICT_LOSER_DESTROYED_TEMPLATES if event.outcome == "destroyed" else CONFLICT_LOSER_WEAKENED_TEMPLATES
        return random.choice(templates).format(**ctx)

    elif event.category == "merge":
        return random.choice(MERGE_TEMPLATES).format(**ctx)

    return ""
