# --- Simulation: contact ---
TRIBE_CONTACT_DISTANCE = 350        # map units; tribes closer than this are "in contact"
TRIBE_ELIMINATION_THRESHOLD = 0.1   # tribe is eliminated when strength drops below this

# --- Simulation: climate events ---
CATASTROPHIC_EVENT_CHANCE = 0.1     # per-planet chance of meteor/volcano/earthquake/tsunami each tick
WEATHER_EVENT_CHANCE = 0.3          # per-planet chance of hurricane/drought/flood each tick
CATASTROPHIC_EVENT_RADIUS_MIN = 150 # map units
CATASTROPHIC_EVENT_RADIUS_MAX = 350
WEATHER_EVENT_RADIUS_MIN = 50
WEATHER_EVENT_RADIUS_MAX = 120

# --- Simulation: societal events ---
SOCIETAL_EVENT_CHANCE = 0.2         # chance any societal event fires in a given tick
POOR_STRENGTH_THRESHOLD = 0.5       # strength below this triggers negative events for non-POOR tribes
RICH_STRENGTH_THRESHOLD = 0.75      # strength at or above this (+ RICH trait) triggers positive events
HIGH_RELIGION_THRESHOLD = 0.5       # religion_scale above this triggers religious events
LOW_RELIGION_THRESHOLD = -0.5       # religion_scale below this triggers secular events
HIGH_SOCIAL_THRESHOLD = 0.5         # social_scale above this triggers collective events

# --- Simulation: conflict ---
RESOURCE_CONFLICT_CHANCE = 0.6      # chance of conflict when tribes have different resource traits
RELIGIOUS_CONFLICT_CHANCE = 0.5     # chance of conflict when religion scales diverge enough
RELIGIOUS_CONFLICT_THRESHOLD = 0.45 # min religion_scale difference to trigger religious conflict

# --- Simulation: merging ---
MERGE_CHANCE = 0.5                  # chance of merger when tribes are socially compatible
MERGE_SOCIAL_THRESHOLD = 0.25       # max social_scale difference for tribes to be merge-eligible
