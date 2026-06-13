# --- Simulation: contact ---
TRIBE_CONTACT_DISTANCE = 900        # map units; modern societies have planet-wide reach, so any two on the same planet are effectively in contact
TRIBE_ELIMINATION_THRESHOLD = 0.05  # society is eliminated when strength drops below this

# --- Simulation: climate events ---
CATASTROPHIC_EVENT_CHANCE = 0.05    # lower still than the middle ages — advanced infrastructure further blunts disaster
WEATHER_EVENT_CHANCE = 0.18
CATASTROPHIC_EVENT_RADIUS_MIN = 250 # larger radii reflect planet-spanning modern societies
CATASTROPHIC_EVENT_RADIUS_MAX = 500
WEATHER_EVENT_RADIUS_MIN = 100
WEATHER_EVENT_RADIUS_MAX = 250

# --- Simulation: societal events ---
SOCIETAL_EVENT_CHANCE = 0.3         # roughly on par with the middle ages — rapid change, balanced by sturdier institutions
POOR_STRENGTH_THRESHOLD = 0.5       # strength below this triggers negative events for non-POOR societies
RICH_STRENGTH_THRESHOLD = 0.75      # strength at or above this (+ RICH trait) triggers positive events
HIGH_RELIGION_THRESHOLD = 0.5       # religion_scale above this triggers doctrinal events
LOW_RELIGION_THRESHOLD = -0.5       # religion_scale below this triggers secular/technocratic events
HIGH_SOCIAL_THRESHOLD = 0.5         # social_scale above this triggers collectivist events
LOW_SOCIAL_THRESHOLD = -0.5         # social_scale below this triggers autocratic/individualist events

# --- Simulation: conflict ---
RESOURCE_CONFLICT_CHANCE = 0.3         # lower than the middle ages — global trade networks ease resource disputes
IDEOLOGICAL_CONFLICT_CHANCE = 0.35     # societies with differing government types clash over ideology, but planet-wide
                                        # contact means this fires often, so it's tuned below the middle ages' religious conflict chance

# --- Simulation: federation (merging) ---
FEDERATION_CHANCE = 0.25            # societies unify deliberately into federations rather than spontaneously
FEDERATION_SOCIAL_THRESHOLD = 0.25  # max social_scale difference for societies to be federation-eligible

# --- Simulation: middle ages -> modern age transition ---
SURVIVOR_SIZE_GROWTH_MIN = 1.5      # surviving kingdoms industrialize into modern societies across the gap between ages
SURVIVOR_SIZE_GROWTH_MAX = 3.5
SURVIVOR_STRENGTH_GROWTH_MIN = 1.1  # industrialization leaves them sturdier than they were as kingdoms
SURVIVOR_STRENGTH_GROWTH_MAX = 1.5
SURVIVOR_STRENGTH_RECOVERY_FLOOR = 0.4 # kingdoms that limped through the middle ages rebuild to at least this strength
                                        # before the growth multiplier is applied
SURVIVOR_TECHNOLOGY_GROWTH_MIN = 1.3 # generations of progress carry their know-how forward
SURVIVOR_TECHNOLOGY_GROWTH_MAX = 1.8

# --- Government & leadership ---
HEGEMONY_STRENGTH_THRESHOLD = 1.5   # strength at or above this overrides other traits, producing a dominant Hegemony
