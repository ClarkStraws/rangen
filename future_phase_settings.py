# --- Simulation: contact ---
TRIBE_CONTACT_DISTANCE = 1000       # map units; future societies span entire worlds, so any two on the same planet are effectively in contact
TRIBE_ELIMINATION_THRESHOLD = 0.05  # society is eliminated when strength drops below this

# --- Simulation: climate events ---
CATASTROPHIC_EVENT_CHANCE = 0.04    # lower than the modern age — megastructures and planetary defenses blunt natural disaster further
WEATHER_EVENT_CHANCE = 0.12
CATASTROPHIC_EVENT_RADIUS_MIN = 300
CATASTROPHIC_EVENT_RADIUS_MAX = 600
WEATHER_EVENT_RADIUS_MIN = 120
WEATHER_EVENT_RADIUS_MAX = 300

# --- Simulation: societal events ---
SOCIETAL_EVENT_CHANCE = 0.4         # rapid change continues to define this age — breakthroughs and crises alike
POOR_STRENGTH_THRESHOLD = 0.5       # strength below this triggers negative events for non-POOR societies
RICH_STRENGTH_THRESHOLD = 0.75      # strength at or above this (+ RICH trait) triggers breakthrough events
HIGH_RELIGION_THRESHOLD = 0.5       # religion_scale above this triggers transcendence/digital-faith events
LOW_RELIGION_THRESHOLD = -0.5       # religion_scale below this triggers rationalist/post-scarcity events
HIGH_SOCIAL_THRESHOLD = 0.5         # social_scale above this triggers unification/uplift events
LOW_SOCIAL_THRESHOLD = -0.5         # social_scale below this triggers command crisis/rogue faction events

# --- Simulation: technological catastrophes ---
# Unlike other event types, catastrophe chance scales with a society's own technology —
# the further a society pushes the frontier, the more likely it courts disaster. The chance
# is capped so that even the most advanced societies aren't doomed to near-certain disaster
# every tick.
BASE_CATASTROPHE_CHANCE = 0.015     # multiplied by tribe.technology each tick to get the actual chance
MAX_CATASTROPHE_CHANCE = 0.15       # upper bound on the per-tick catastrophe chance, regardless of technology
CATASTROPHE_SEVERITY_MIN = 0.35     # catastrophes are still far more lethal than ordinary societal setbacks
CATASTROPHE_SEVERITY_MAX = 0.85

# --- Simulation: conflict ---
RESOURCE_CONFLICT_CHANCE = 0.3      # lower than the modern age — post-scarcity technology eases resource disputes
NUCLEAR_CONFLICT_CHANCE = 0.2       # societies with differing governments risk nuclear war
NUCLEAR_SEVERITY_MIN = 0.2          # nuclear war devastates both sides, the loser most of all
NUCLEAR_SEVERITY_MAX = 0.6

# --- Simulation: unification (merging) ---
UNIFICATION_CHANCE = 0.2            # societies unify deliberately when their outlooks and resources align
UNIFICATION_SOCIAL_THRESHOLD = 0.25 # max social_scale difference for societies to be unification-eligible

# --- Simulation: modern age -> future age transition ---
SURVIVOR_SIZE_GROWTH_MIN = 1.2      # surviving societies advance into the future age across the gap between ages
SURVIVOR_SIZE_GROWTH_MAX = 2.5
SURVIVOR_STRENGTH_GROWTH_MIN = 1.1  # advancement leaves them sturdier than they were as modern societies
SURVIVOR_STRENGTH_GROWTH_MAX = 1.4
SURVIVOR_STRENGTH_RECOVERY_FLOOR = 0.4 # societies that limped through the modern age rebuild to at least this strength
                                        # before the growth multiplier is applied
SURVIVOR_TECHNOLOGY_GROWTH_MIN = 1.4 # a final leap in technology — the foundation for breakthroughs to come
SURVIVOR_TECHNOLOGY_GROWTH_MAX = 2.2
