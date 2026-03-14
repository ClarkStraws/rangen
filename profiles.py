import random
from entities import Star, BinaryStarSystem, BinaryOrbitType, BinaryArchetype, ZoneProfile, PlanetGenerationProfile
from typing import Union, Optional
# ── Single star ────────────────────────────────────────────────────────────────

def _generate_zone_profile(star: Star, orbit_start_au: float = 0.1, orbit_end_au: Optional[float] = None) -> ZoneProfile:
    """
    Generates a ZoneProfile for a single main-sequence star.
    orbit_start_au / orbit_end_au allow callers to clamp the zone
    for binary stability cutoffs — if orbit_end_au is None, the
    star's natural outer boundary is used.
    """
    spectral_class = star.classification

    profiles = {
        'O': dict(frost_line_au=50,  inner_zone_end_au=20,  outer_zone_end_au=200, min_planets=0, max_planets=2,
                  inner_type_weights={"Rocky": 0.1,  "SuperEarth": 0.1,  "GasGiant": 0.5,  "IceGiant": 0.3},
                  outer_type_weights={"GasGiant": 0.7, "IceGiant": 0.3}),

        'B': dict(frost_line_au=20,  inner_zone_end_au=15,  outer_zone_end_au=150, min_planets=1, max_planets=3,
                  inner_type_weights={"Rocky": 0.15, "SuperEarth": 0.15, "GasGiant": 0.4,  "IceGiant": 0.3},
                  outer_type_weights={"GasGiant": 0.6, "IceGiant": 0.4}),

        'A': dict(frost_line_au=5,   inner_zone_end_au=5,   outer_zone_end_au=80,  min_planets=3, max_planets=5,
                  inner_type_weights={"Rocky": 0.2,  "SuperEarth": 0.2,  "GasGiant": 0.4,  "IceGiant": 0.2},
                  outer_type_weights={"GasGiant": 0.6, "IceGiant": 0.4}),

        'F': dict(frost_line_au=3,   inner_zone_end_au=4,   outer_zone_end_au=50,  min_planets=4, max_planets=7,
                  inner_type_weights={"Rocky": 0.3,  "SuperEarth": 0.3,  "GasGiant": 0.3,  "IceGiant": 0.1},
                  outer_type_weights={"GasGiant": 0.5, "IceGiant": 0.5}),

        'G': dict(frost_line_au=2,   inner_zone_end_au=4,   outer_zone_end_au=40,  min_planets=5, max_planets=8,
                  inner_type_weights={"Rocky": 0.4,  "SuperEarth": 0.4,  "GasGiant": 0.15, "IceGiant": 0.05},
                  outer_type_weights={"GasGiant": 0.4, "IceGiant": 0.6}),

        'K': dict(frost_line_au=1.5, inner_zone_end_au=3,   outer_zone_end_au=30,  min_planets=3, max_planets=7,
                  inner_type_weights={"Rocky": 0.5,  "SuperEarth": 0.4,  "GasGiant": 0.08, "IceGiant": 0.02},
                  outer_type_weights={"GasGiant": 0.3, "IceGiant": 0.7}),

        'M': dict(frost_line_au=0.5, inner_zone_end_au=1.5, outer_zone_end_au=10,  min_planets=2, max_planets=5,
                  inner_type_weights={"Rocky": 0.6,  "SuperEarth": 0.3,  "GasGiant": 0.08, "IceGiant": 0.02},
                  outer_type_weights={"GasGiant": 0.2, "IceGiant": 0.8}),
    }

    p = profiles.get(spectral_class, profiles['M'])

    return ZoneProfile(
        min_planets=p['min_planets'],
        max_planets=p['max_planets'],
        orbit_start_au=orbit_start_au,
        orbit_end_au=orbit_end_au if orbit_end_au is not None else p['outer_zone_end_au'],
        frost_line_au=p['frost_line_au'],
        inner_zone_end_au=p['inner_zone_end_au'],
        outer_zone_end_au=p['outer_zone_end_au'],
        inner_type_weights=p['inner_type_weights'],
        outer_type_weights=p['outer_type_weights'],
    )


# ── Binary zone factories ──────────────────────────────────────────────────────

def _binary_twin_main_sequence(system: BinaryStarSystem) -> list[ZoneProfile]:
    sep = system.separation_au

    if system.orbit_type == BinaryOrbitType.WIDE:
        # Fully independent — each star gets its natural profile unclamped
        return [
            _generate_zone_profile(system.primary),
            _generate_zone_profile(system.secondary),
        ]

    if system.orbit_type == BinaryOrbitType.S_TYPE:
        # Each star's outer edge is clamped to 1/3 separation
        outer_clamp = sep / 3
        return [
            _generate_zone_profile(system.primary,   orbit_end_au=outer_clamp),
            _generate_zone_profile(system.secondary, orbit_end_au=outer_clamp),
        ]

    # P-type: one shared zone orbiting both stars; inner edge is 3x separation
    return [
        ZoneProfile(
            min_planets=3, max_planets=7,
            orbit_start_au=sep * 3,
            orbit_end_au=80,
            frost_line_au=3,           # combined ~G+G luminosity approximation
            inner_zone_end_au=5,
            outer_zone_end_au=80,
            inner_type_weights={"Rocky": 0.4, "SuperEarth": 0.3, "GasGiant": 0.2, "IceGiant": 0.1},
            outer_type_weights={"GasGiant": 0.5, "IceGiant": 0.5},
        )
    ]


def _binary_unequal_main_sequence(system: BinaryStarSystem) -> list[ZoneProfile]:
    sep = system.separation_au

    if system.orbit_type == BinaryOrbitType.WIDE:
        return [
            _generate_zone_profile(system.primary),    # hot star, sparse
            _generate_zone_profile(system.secondary),  # companion, normal
        ]

    if system.orbit_type == BinaryOrbitType.S_TYPE:
        outer_clamp = sep / 3
        return [
            _generate_zone_profile(system.primary,   orbit_end_au=outer_clamp),   # hot, few planets
            _generate_zone_profile(system.secondary, orbit_end_au=outer_clamp),   # normal companion
        ]

    # P-type: hot primary dominates; everything pushed far out
    return [
        ZoneProfile(
            min_planets=1, max_planets=3,
            orbit_start_au=sep * 3,
            orbit_end_au=200,
            frost_line_au=40,
            inner_zone_end_au=20,
            outer_zone_end_au=200,
            inner_type_weights={"Rocky": 0.1, "SuperEarth": 0.1, "GasGiant": 0.5, "IceGiant": 0.3},
            outer_type_weights={"GasGiant": 0.6, "IceGiant": 0.4},
        )
    ]


def _binary_giant_main_sequence(system: BinaryStarSystem) -> list[ZoneProfile]:
    sep = system.separation_au

    # Giant side: no inner zone, only distant cold survivors
    giant_zone = ZoneProfile(
        min_planets=0, max_planets=2,
        orbit_start_au=10,
        orbit_end_au=min(100, sep / 3) if system.orbit_type == BinaryOrbitType.S_TYPE else 100,
        frost_line_au=10,
        inner_zone_end_au=10,
        outer_zone_end_au=100,
        inner_type_weights={"Rocky": 0.3, "SuperEarth": 0.3, "GasGiant": 0.2, "IceGiant": 0.2},
        outer_type_weights={"GasGiant": 0.3, "IceGiant": 0.7},
    )

    if system.orbit_type == BinaryOrbitType.P_TYPE:
        # One shared cold outer zone only
        return [giant_zone]

    # S-type: companion also gets a normal clamped profile
    return [
        giant_zone,
        _generate_zone_profile(system.secondary, orbit_end_au=sep / 3),
    ]


def _binary_white_dwarf_main_sequence(system: BinaryStarSystem) -> list[ZoneProfile]:
    sep = system.separation_au

    # WD side: dim and mostly barren; small chance of a close rocky survivor
    wd_zone = ZoneProfile(
        min_planets=0, max_planets=1,
        orbit_start_au=0.1,
        orbit_end_au=sep / 3 if system.orbit_type == BinaryOrbitType.S_TYPE else 5,
        frost_line_au=1,
        inner_zone_end_au=2,
        outer_zone_end_au=5,
        inner_type_weights={"Rocky": 0.8, "SuperEarth": 0.2, "GasGiant": 0.0, "IceGiant": 0.0},
        outer_type_weights={"GasGiant": 0.2, "IceGiant": 0.8},
    )

    if system.orbit_type == BinaryOrbitType.WIDE:
        return [
            wd_zone,
            _generate_zone_profile(system.secondary),  # fully independent
        ]

    return [
        wd_zone,
        _generate_zone_profile(system.secondary, orbit_end_au=sep / 3),
    ]


def _binary_contact(system: BinaryStarSystem) -> list[ZoneProfile]:
    # Nothing close survived; one shared distant zone only
    return [
        ZoneProfile(
            min_planets=0, max_planets=2,
            orbit_start_au=10,
            orbit_end_au=60,
            frost_line_au=10,
            inner_zone_end_au=10,
            outer_zone_end_au=60,
            inner_type_weights={"Rocky": 0.3, "SuperEarth": 0.3, "GasGiant": 0.2, "IceGiant": 0.2},
            outer_type_weights={"GasGiant": 0.2, "IceGiant": 0.8},
        )
    ]


def _binary_compact_object(system: BinaryStarSystem) -> list[ZoneProfile]:
    # 70% chance of no planets at all
    if random.random() < 0.7:
        return []
    return [
        ZoneProfile(
            min_planets=0, max_planets=1,
            orbit_start_au=15,
            orbit_end_au=80,
            frost_line_au=15,
            inner_zone_end_au=15,
            outer_zone_end_au=80,
            inner_type_weights={"Rocky": 0.5, "SuperEarth": 0.3, "GasGiant": 0.1, "IceGiant": 0.1},
            outer_type_weights={"GasGiant": 0.1, "IceGiant": 0.9},
        )
    ]


# ── Dispatch ───────────────────────────────────────────────────────────────────

_BINARY_PROFILE_BUILDERS = {
    BinaryArchetype.TWIN_MAIN_SEQUENCE:       _binary_twin_main_sequence,
    BinaryArchetype.UNEQUAL_MAIN_SEQUENCE:    _binary_unequal_main_sequence,
    BinaryArchetype.GIANT_MAIN_SEQUENCE:      _binary_giant_main_sequence,
    BinaryArchetype.WHITE_DWARF_MAIN_SEQUENCE: _binary_white_dwarf_main_sequence,
    BinaryArchetype.CONTACT_BINARY:           _binary_contact,
    BinaryArchetype.COMPACT_OBJECT:           _binary_compact_object,
}

def generate_planet_profile(star_system: Union[Star, BinaryStarSystem]) -> PlanetGenerationProfile:
    if isinstance(star_system, Star):
        return PlanetGenerationProfile(
            zones=[_generate_zone_profile(star_system)],
            binary_separation_au=None,
        )

    builder = _BINARY_PROFILE_BUILDERS[star_system.archetype]
    return PlanetGenerationProfile(
        zones=builder(star_system),
        binary_separation_au=star_system.separation_au,
    )