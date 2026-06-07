# --- Simulation: contact ---
TRIBE_CONTACT_DISTANCE = 350        # map units; kingdoms have grown and can reach one another across far greater distances than tribes once could
TRIBE_ELIMINATION_THRESHOLD = 0.1   # tribe is eliminated when strength drops below this

# --- Simulation: climate events ---
CATASTROPHIC_EVENT_CHANCE = 0.07    # lower than the ancient world — established kingdoms are better prepared for disaster
WEATHER_EVENT_CHANCE = 0.25         # slightly lower than the ancient world for the same reason
CATASTROPHIC_EVENT_RADIUS_MIN = 200 # larger radii reflect the greater size of middle-age territories
CATASTROPHIC_EVENT_RADIUS_MAX = 450
WEATHER_EVENT_RADIUS_MIN = 80
WEATHER_EVENT_RADIUS_MAX = 200

# --- Simulation: societal events ---
SOCIETAL_EVENT_CHANCE = 0.3         # higher than the ancient world — feudal society is more politically and socially complex
POOR_STRENGTH_THRESHOLD = 0.5       # strength below this triggers negative events for non-POOR tribes
RICH_STRENGTH_THRESHOLD = 0.75      # strength at or above this (+ RICH trait) triggers positive events
HIGH_RELIGION_THRESHOLD = 0.5       # religion_scale above this triggers religious events
LOW_RELIGION_THRESHOLD = -0.5       # religion_scale below this triggers secular events
HIGH_SOCIAL_THRESHOLD = 0.5         # social_scale above this triggers collective events

# --- Simulation: conflict ---
RESOURCE_CONFLICT_CHANCE = 0.45     # lower than the ancient world — established trade networks blunt raw resource conflict
RELIGIOUS_CONFLICT_CHANCE = 0.6     # higher than the ancient world — organized faiths and crusades take center stage
RELIGIOUS_CONFLICT_THRESHOLD = 0.35 # lower than the ancient world — institutionalized religion makes doctrinal gaps easier to ignite

# --- Simulation: merging ---
MERGE_CHANCE = 0.3                  # lower than the ancient world — kingdoms unify deliberately (marriage, treaty) rather than spontaneously
MERGE_SOCIAL_THRESHOLD = 0.25       # max social_scale difference for tribes to be merge-eligible

# --- Simulation: ancient -> middle age transition ---
SURVIVOR_SIZE_GROWTH_MIN = 1.5       # surviving tribes swell into kingdoms across the gap between ages
SURVIVOR_SIZE_GROWTH_MAX = 3.0
SURVIVOR_STRENGTH_GROWTH_MIN = 1.1   # consolidation leaves them sturdier than they were as scattered tribes
SURVIVOR_STRENGTH_GROWTH_MAX = 1.4
SURVIVOR_TECHNOLOGY_GROWTH_MIN = 1.2 # generations of progress carry their know-how forward
SURVIVOR_TECHNOLOGY_GROWTH_MAX = 1.6
