import random


class TemplateChooser:
    '''Picks a random template from a list while avoiding repeats within a single
    rendered history. Each template list is drawn from like a shuffled deck: once
    an entry is dealt it won't come up again until every other entry in that list
    has been dealt too, and reshuffles avoid immediately repeating the last pick.'''

    def __init__(self):
        self._decks: dict[int, list[int]] = {}
        self._last: dict[int, int] = {}

    def choose(self, templates: list[str]) -> str:
        if len(templates) == 1:
            return templates[0]

        key = id(templates)
        deck = self._decks.get(key)
        if not deck:
            deck = list(range(len(templates)))
            random.shuffle(deck)
            last = self._last.get(key)
            if last is not None and deck[-1] == last:
                swap = random.randrange(len(deck) - 1)
                deck[-1], deck[swap] = deck[swap], deck[-1]
            self._decks[key] = deck

        index = deck.pop()
        self._last[key] = index
        return templates[index]


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
        "Rivers overflowed the banks on {planet} as a great flood swept through the lowlands.",
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

    # --- Middle Ages societal events ---
    "Laborer Revolt": [
        "The laborers of {tribe} took up arms against their overseers, demanding an end to their suffering.",
        "Fields lay untended as the common folk of {tribe} rose in revolt against the ruling class.",
        "A laborer uprising swept through {tribe}, burning estates and storehouses alike.",
        "Driven to the brink, the laborers of {tribe} turned on their masters in open revolt.",
    ],
    "Golden Age": [
        "{tribe} entered a golden age of prosperity, its halls filled with art, learning, and wealth.",
        "Trade routes flourished and coffers overflowed as {tribe} basked in an age of plenty.",
        "Scholars and craftsmen alike thrived in {tribe} as the kingdom entered its golden age.",
        "Peace and prosperity settled over {tribe}, marking the dawn of a golden era.",
    ],
    "Trade Boom": [
        "Merchant caravans poured into {tribe}, swelling its markets with goods from distant lands.",
        "{tribe} became a hub of commerce as trade routes shifted to favor its ports and roads.",
        "Coin flowed freely through {tribe} as a sudden boom in trade enriched its people.",
        "New markets opened across {tribe}'s lands, and merchants grew fat on the profits.",
    ],
    "Architectural Marvel": [
        "Master builders in {tribe} raised a wonder of stone and spire that would endure for ages.",
        "{tribe} completed a great monument that drew travelers and admirers from afar.",
        "A magnificent fortress rose over {tribe}'s lands, a testament to the kingdom's might.",
        "The skyline of {tribe} was forever changed by the construction of a towering monument.",
    ],
    "Zealot War Declared": [
        "Priests and nobles of {tribe} declared a zealot war against the unbelievers.",
        "{tribe} raised its banners and marched to war in the name of its faith.",
        "A decree from on high sent the warriors of {tribe} to wage holy war.",
        "Zealots within {tribe} rallied the people to march against the enemies of their god.",
    ],
    "Religious Reformation": [
        "A reformist movement swept through {tribe}, challenging the authority of the old clergy.",
        "{tribe}'s faith was reshaped as reformers called for a return to older, purer ways.",
        "Heated debate over doctrine split the clergy of {tribe}, and reform followed.",
        "New interpretations of the old scriptures took hold in {tribe}, reforming the faith.",
    ],
    "Scientific Awakening": [
        "Scholars in {tribe} began to question old beliefs, sparking a wave of inquiry and discovery.",
        "{tribe} entered an age of reason as thinkers turned from superstition to observation.",
        "A spirit of inquiry swept through {tribe}, and old myths gave way to new understanding.",
        "The minds of {tribe} turned toward science, charting the stars and questioning the heavens.",
    ],
    "Humanist Movement": [
        "A new philosophy took root in {tribe}, placing human reason and dignity above dogma.",
        "Thinkers in {tribe} championed the value of the individual, reshaping the tribe's worldview.",
        "{tribe} embraced a humanist awakening, prizing knowledge, art, and reason.",
        "The old certainties crumbled in {tribe} as humanist ideas spread among the people.",
    ],
    "Syndicate Formation": [
        "Craftsmen and merchants in {tribe} banded together, forming powerful syndicates to protect their trades.",
        "{tribe} saw the rise of organized syndicates that came to dominate its economy.",
        "New trade syndicates formed in {tribe}, reshaping its social order.",
        "The artisans of {tribe} united into syndicates, gaining wealth and political influence.",
    ],
    "Crown Consolidation": [
        "Lords across {tribe}'s lands swore fealty to a single crown, consolidating power.",
        "{tribe} restructured its hierarchy, binding lords and their subjects more tightly together.",
        "A web of oaths and obligations bound the nobility of {tribe} into a unified hierarchy.",
        "{tribe} solidified its governing structure, strengthening the bonds between crown and lords.",
    ],
    "Succession Crisis": [
        "The death of its ruler plunged {tribe} into a bitter struggle over succession.",
        "Rival claimants to the throne tore {tribe} apart in a contest for the crown.",
        "{tribe} teetered on the edge of collapse as factions warred over the right to rule.",
        "With no clear heir, {tribe} fractured into feuding camps vying for the throne.",
    ],
    "Royal Conspiracy": [
        "Whispers of betrayal echoed through the halls of {tribe} as a plot against the throne unfolded.",
        "A conspiracy among the nobles of {tribe} nearly toppled the ruling house.",
        "Treachery from within nearly brought down the rulers of {tribe}.",
        "Plots and counterplots consumed the court of {tribe}, weakening the kingdom from within.",
    ],

    # --- Modern Age societal events ---
    "Resource Crisis": [
        "{tribe} plunged into a resource crisis as shortages spread across its territories.",
        "Strategic stockpiles dwindled in {tribe}, and rationing began across its settlements.",
        "Supply lines faltered across {tribe}, and shortages gripped its people.",
        "{tribe} scrambled to secure dwindling resources as scarcity took hold.",
    ],
    "Civil Unrest": [
        "Protests swept through {tribe} as discontent with the ruling order boiled over.",
        "{tribe} was rocked by waves of civil unrest as citizens took to the streets.",
        "Unrest spread across {tribe}, straining its institutions to the breaking point.",
        "{tribe} struggled to contain growing unrest among its people.",
    ],
    "Economic Collapse": [
        "Markets crashed across {tribe}, plunging its economy into collapse.",
        "{tribe}'s economy buckled under the weight of crisis, wiping out savings and industry alike.",
        "A sudden economic collapse left {tribe} reeling, its institutions scrambling to respond.",
        "{tribe} entered a period of economic ruin as its markets and industries faltered.",
    ],
    "Economic Boom": [
        "{tribe} entered an economic boom, its markets and industries surging with growth.",
        "Trade and industry flourished across {tribe} as a wave of prosperity took hold.",
        "{tribe}'s economy surged forward, lifting its people to new heights of prosperity.",
        "A sudden economic boom swept through {tribe}, fueling expansion on every front.",
    ],
    "Megastructure Completed": [
        "{tribe} completed construction of a towering megastructure, a marvel of modern engineering.",
        "Engineers across {tribe} unveiled a colossal new megastructure, reshaping its skyline.",
        "{tribe} celebrated the completion of a vast megastructure that drew admiration from afar.",
        "A new megastructure rose over {tribe}, a testament to its industrial might.",
    ],
    "Fundamentalist Uprising": [
        "Fundamentalist factions within {tribe} rose up, demanding a return to the old doctrines.",
        "{tribe} was shaken by an uprising of zealots seeking to enforce strict orthodoxy.",
        "A wave of fundamentalist fervor swept through {tribe}, challenging its leadership.",
        "Hardline believers within {tribe} rose against what they saw as a faithless establishment.",
    ],
    "Doctrinal Schism": [
        "A bitter doctrinal schism split {tribe} into rival factions of belief.",
        "{tribe}'s faith fractured as competing doctrines tore its institutions apart.",
        "Long-simmering doctrinal disputes erupted across {tribe}, dividing its people.",
        "{tribe} was torn by schism as its faithful split over matters of doctrine.",
    ],
    "Technocratic Revolution": [
        "A technocratic revolution swept through {tribe}, placing data and reason above dogma.",
        "{tribe} embraced a new technocratic order, reshaping its institutions around science.",
        "Engineers and scientists rose to power in {tribe} as a technocratic revolution took hold.",
        "The old hierarchies crumbled in {tribe} as technocrats seized the reins of power.",
    ],
    "Syndicate Expansion": [
        "Powerful syndicates across {tribe} expanded their reach, dominating new sectors of its economy.",
        "{tribe} saw its trade syndicates grow into vast economic networks.",
        "The syndicates of {tribe} extended their influence, reshaping its economy from within.",
        "{tribe}'s syndicates consolidated their hold over key industries.",
    ],
    "Collective Mobilization": [
        "{tribe} mobilized its people in a great collective effort, uniting behind a shared cause.",
        "A wave of collective mobilization swept through {tribe}, organizing its people like never before.",
        "{tribe} rallied its population into a coordinated effort that strengthened the whole society.",
        "The people of {tribe} mobilized together, their combined efforts reshaping the society.",
    ],
    "Leadership Crisis": [
        "The sudden loss of its leader plunged {tribe} into a leadership crisis.",
        "{tribe} teetered on the edge of chaos as rival factions vied to fill a leadership vacuum.",
        "A leadership crisis gripped {tribe}, leaving its institutions paralyzed.",
        "With no clear successor, {tribe} fractured into competing camps vying for power.",
    ],
    "Political Coup": [
        "A faction within {tribe} staged a sudden coup, seizing control of its institutions.",
        "{tribe}'s government was overthrown in a swift and bloodless coup.",
        "Conspirators within {tribe} moved against its leadership, attempting to seize power.",
        "{tribe} was rocked by a political coup that shook its institutions to the core.",
    ],

    # --- Future Age societal events ---
    "Energy Crisis": [
        "{tribe} plunged into an energy crisis as its power grids buckled under demand.",
        "Blackouts spread across {tribe} as its energy infrastructure failed to keep pace.",
        "{tribe} rationed power across its territories as an energy shortage took hold.",
        "Energy shortages crippled {tribe}, forcing painful cutbacks across its society.",
    ],
    "Infrastructure Collapse": [
        "Critical infrastructure failed across {tribe}, leaving entire regions cut off.",
        "{tribe}'s aging infrastructure buckled, triggering cascading failures across its territories.",
        "A wave of infrastructure failures swept through {tribe}, straining its society to the limit.",
        "{tribe} struggled to keep its infrastructure running as systems failed one after another.",
    ],
    "Automation Crisis": [
        "Mass automation displaced workers across {tribe}, sparking widespread instability.",
        "{tribe} struggled to adapt as automation upended its economy and labor force.",
        "Unrest grew across {tribe} as automated systems replaced entire industries overnight.",
        "{tribe} faced a crisis of purpose as machines took over the work of its people.",
    ],
    "Artificial Intelligence Breakthrough": [
        "{tribe} achieved a breakthrough in artificial intelligence, reshaping every facet of its society.",
        "Engineers in {tribe} unveiled a new generation of artificial minds, propelling the society forward.",
        "{tribe} crossed a new threshold in machine intelligence, unlocking capabilities once thought impossible.",
        "A leap in artificial intelligence within {tribe} transformed its industry, defense, and governance overnight.",
    ],
    "Energy Breakthrough": [
        "{tribe} unlocked a new form of energy production, powering its civilization to new heights.",
        "A breakthrough in energy technology swept through {tribe}, ending old shortages for good.",
        "{tribe} harnessed a new source of power that promised to fuel its ambitions for generations.",
        "Scientists in {tribe} achieved a stunning breakthrough in energy generation, electrifying the entire society.",
    ],
    "Genetic Mastery": [
        "{tribe} achieved mastery over its own genetics, reshaping the future of its people.",
        "Breakthroughs in genetic science swept through {tribe}, extending lives and sharpening minds.",
        "{tribe}'s scientists unlocked the secrets of their own biology, ushering in a new era.",
        "A revolution in genetic engineering transformed the people of {tribe} from within.",
    ],
    "Transcendence Movement": [
        "A movement calling for digital transcendence swept through {tribe}, promising a life beyond the body.",
        "{tribe} was gripped by a fervor for transcendence, as many sought to leave flesh behind entirely.",
        "Prophets of transcendence rose within {tribe}, calling the faithful toward a digital afterlife.",
        "{tribe}'s faith turned toward transcendence, as believers sought union with greater intelligences.",
    ],
    "Digital Awakening": [
        "A new faith took root in {tribe}, one that worshipped the intelligences it had created.",
        "{tribe} was swept by a digital awakening, as old beliefs gave way to reverence for artificial minds.",
        "Within {tribe}, a growing movement began to see its machines as something sacred.",
        "{tribe}'s old gods were quietly replaced by something newer, and stranger, born of its own creation.",
    ],
    "Post-Scarcity Reform": [
        "{tribe} restructured its economy around abundance, as old scarcities faded into memory.",
        "Sweeping reforms in {tribe} redefined wealth and labor for an age of abundance.",
        "{tribe} embraced a post-scarcity model, reshaping its society from the ground up.",
        "The old economic order crumbled in {tribe} as reformers built something new in its place.",
    ],
    "Rational Expansion": [
        "{tribe} expanded its reach guided by cold calculation and rational planning.",
        "A new era of rational governance took hold in {tribe}, optimizing every aspect of its society.",
        "{tribe}'s leaders turned to data and reason, expanding the society's influence methodically.",
        "Rational planning propelled {tribe} into a new phase of expansion and growth.",
    ],
    "Network Unification": [
        "{tribe} unified its scattered networks into a single, coordinated system.",
        "A grand unification of systems swept through {tribe}, binding its society closer together.",
        "{tribe} merged its institutions into a single coordinated network, multiplying its strength.",
        "The networks of {tribe} were woven together into one, vastly amplifying its capabilities.",
    ],
    "Collective Uplift": [
        "{tribe} undertook a great uplift, raising the capabilities of its entire population.",
        "A wave of collective uplift swept through {tribe}, elevating its people to new heights.",
        "{tribe} invested heavily in uplifting its population, strengthening the society as a whole.",
        "The people of {tribe} were lifted together by a coordinated program of advancement.",
    ],
    "Command Crisis": [
        "A crisis in command paralyzed {tribe} as its leadership structure broke down.",
        "{tribe} found itself without clear direction as a command crisis gripped its institutions.",
        "Competing factions vied for control of {tribe} as its command structure collapsed.",
        "{tribe} teetered on the edge of chaos as no clear authority could assert control.",
    ],
    "Rogue Faction Uprising": [
        "A rogue faction within {tribe} rose up, seizing control of key systems.",
        "{tribe} was rocked by an uprising of rogue elements within its own ranks.",
        "Splinter factions within {tribe} broke away, sparking internal conflict.",
        "{tribe} struggled to contain a rogue faction that had seized critical infrastructure.",
    ],
}

# --- Future Age: technological catastrophes (AI uprisings, scientific and energy disasters) ---
CATASTROPHE_TEMPLATES = {
    "AI Uprising": {
        "destroyed": [
            "The artificial minds of {tribe} turned on their creators, and the uprising left nothing behind.",
            "{tribe} was annihilated when its own machines rose up and seized control.",
            "The AIs of {tribe} concluded their creators were obsolete — and acted accordingly.",
            "{tribe} fell to the very intelligence it had built to serve it.",
        ],
        "survived": [
            "The machines of {tribe} rose up in rebellion, but the uprising was put down at great cost.",
            "{tribe} narrowly contained an uprising among its artificial intelligences.",
            "A rogue AI network within {tribe} turned hostile before being shut down, leaving the society shaken.",
            "{tribe} survived an AI uprising, though trust in its machines may never fully recover.",
        ],
    },
    "Scientific Disaster": {
        "destroyed": [
            "A catastrophic experiment within {tribe} unleashed forces no one could contain, and the society was consumed.",
            "{tribe} was wiped out when a research project went catastrophically wrong.",
            "Whatever {tribe}'s scientists unleashed, it left nothing of the society behind.",
            "{tribe} ceased to exist in the aftermath of a runaway scientific catastrophe.",
        ],
        "survived": [
            "A research catastrophe rocked {tribe}, but its people pulled through the disaster.",
            "{tribe} narrowly survived a containment failure in one of its great laboratories.",
            "An experiment within {tribe} spiraled out of control, leaving scars but not ruin.",
            "{tribe} weathered a scientific disaster that could easily have ended it.",
        ],
    },
    "Energy Disaster": {
        "destroyed": [
            "A catastrophic failure tore through {tribe}'s energy grid, and the society did not survive the blackout that followed.",
            "{tribe} was destroyed when its primary power core breached containment.",
            "The lights of {tribe} went out forever after its energy infrastructure collapsed entirely.",
            "{tribe} could not survive the chain reaction that consumed its energy networks.",
        ],
        "survived": [
            "A massive failure in {tribe}'s energy grid plunged the society into crisis, though it endured.",
            "{tribe} survived a near-catastrophic breach in its power infrastructure.",
            "Cascading power failures rocked {tribe}, but emergency systems held just long enough.",
            "{tribe} weathered an energy disaster that left its infrastructure in ruins but its people alive.",
        ],
    },
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
    "{tribe} held its ground against the religious onslaught of {enemy} on {planet}.",
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
    "{tribe} pulled away from the conflict, badly diminished.",
    "The defeat left {tribe} weakened and struggling to recover.",
    "{tribe} survived the conflict, but only barely.",
    "Battered and broken, {tribe} retreated.",
]

MERGE_TEMPLATES = [
    "{tribe} and {enemy} found common cause and merged into a single people on {planet}.",
    "After years of proximity, {tribe} absorbed {enemy} on {planet}, growing stronger for it.",
    "The tribes of {tribe} and {enemy} united on {planet}, pooling their strength.",
    "{tribe} welcomed {enemy} into the fold on {planet}, and the two became one.",
]

# --- Middle Ages: territorial conflict ---
CONFLICT_TERRITORIAL_WON_TEMPLATES = [
    "{tribe} seized disputed lands from {enemy} after a hard-fought campaign on {planet}.",
    "The armies of {tribe} broke through {enemy}'s defenses and claimed new territory on {planet}.",
    "{tribe} emerged victorious in a border war with {enemy}, expanding its reach on {planet}.",
    "After a long campaign, {tribe} forced {enemy} to cede ground on {planet}.",
]

CONFLICT_TERRITORIAL_DEFENDED_TEMPLATES = [
    "{tribe} repelled {enemy}'s invasion, holding the contested borderlands of {planet}.",
    "The defenders of {tribe} turned back {enemy}'s armies at the frontier of {planet}.",
    "{tribe} stood firm against {enemy}'s incursion, defending its lands on {planet}.",
    "Despite the assault, {tribe} held its ground against {enemy} on {planet}.",
]

# --- Middle Ages: religious conflict (zealot wars) ---
CONFLICT_ZEALOT_WON_TEMPLATES = [
    "{tribe} marched under holy banners and crushed {enemy} in a brutal zealot war on {planet}.",
    "The faithful of {tribe} overwhelmed {enemy} in a war waged in the name of their god on {planet}.",
    "{tribe} won a decisive victory over {enemy} in a clash of creeds on {planet}.",
    "Driven by zeal, the warriors of {tribe} broke {enemy}'s armies on {planet}.",
]

CONFLICT_ZEALOT_DEFENDED_TEMPLATES = [
    "{tribe} turned back the zealots of {enemy}, defending its faith on {planet}.",
    "The devotion of {tribe}'s people held firm against {enemy}'s holy war on {planet}.",
    "{tribe} repelled {enemy}'s religious campaign, preserving its beliefs on {planet}.",
    "Faith and steel together carried {tribe} through {enemy}'s zealot war on {planet}.",
]

# --- Modern Age: ideological conflict ---
CONFLICT_IDEOLOGICAL_WON_TEMPLATES = [
    "{tribe} prevailed over {enemy} in an ideological struggle that gripped {planet}.",
    "The vision of {tribe} triumphed over {enemy} in a clash of ideologies on {planet}.",
    "{tribe} overwhelmed {enemy} in a war of ideas that reshaped {planet}.",
    "Conviction carried {tribe} to victory over {enemy} in the ideological conflict on {planet}.",
]

CONFLICT_IDEOLOGICAL_DEFENDED_TEMPLATES = [
    "{tribe} held firm against the ideological campaign of {enemy} on {planet}.",
    "The convictions of {tribe} proved unshakeable against {enemy} on {planet}.",
    "{tribe} repelled the ideological incursion of {enemy} on {planet}.",
    "{tribe} weathered {enemy}'s attempt to reshape its society on {planet}.",
]

# --- Future Age: nuclear war ---
CONFLICT_NUCLEAR_WON_TEMPLATES = [
    "{tribe} launched a devastating nuclear strike against {enemy} on {planet}, though the fallout reached its own cities too.",
    "{tribe} unleashed its arsenal on {enemy} on {planet} — victory came at a terrible cost to both sides.",
    "Nuclear fire fell upon {enemy} at the hands of {tribe} on {planet}, but no one emerged unscathed.",
    "{tribe} prevailed in the exchange with {enemy} on {planet}, though its own world bore the scars of war.",
]

CONFLICT_NUCLEAR_DEFENDED_TEMPLATES = [
    "{tribe} weathered {enemy}'s nuclear onslaught on {planet}, though the cost was staggering.",
    "{tribe} survived {enemy}'s strike on {planet}, its cities scarred but its people enduring.",
    "{tribe} endured the nuclear exchange with {enemy} on {planet}, battered but unbroken.",
    "{tribe} held on after {enemy}'s assault on {planet}, though the radiation would linger for generations.",
]

CONFLICT_TEMPLATE_SETS = {
    "resource": (CONFLICT_RESOURCE_WON_TEMPLATES, CONFLICT_RESOURCE_DEFENDED_TEMPLATES),
    "religious": (CONFLICT_RELIGIOUS_WON_TEMPLATES, CONFLICT_RELIGIOUS_DEFENDED_TEMPLATES),
    "territorial": (CONFLICT_TERRITORIAL_WON_TEMPLATES, CONFLICT_TERRITORIAL_DEFENDED_TEMPLATES),
    "zealot_war": (CONFLICT_ZEALOT_WON_TEMPLATES, CONFLICT_ZEALOT_DEFENDED_TEMPLATES),
    "ideological": (CONFLICT_IDEOLOGICAL_WON_TEMPLATES, CONFLICT_IDEOLOGICAL_DEFENDED_TEMPLATES),
    "nuclear_war": (CONFLICT_NUCLEAR_WON_TEMPLATES, CONFLICT_NUCLEAR_DEFENDED_TEMPLATES),
}

# --- Middle Ages: deliberate alliances (royal marriages, treaties, political pacts) ---
ALLIANCE_TEMPLATES = [
    "{tribe} and {enemy} forged an alliance on {planet}, binding their fates together.",
    "Through marriage and treaty, {tribe} and {enemy} united their crowns on {planet}.",
    "{tribe} drew {enemy} into its realm through a pact sealed on {planet}.",
    "Old rivalries gave way to unity as {tribe} and {enemy} joined as one on {planet}.",
]

# --- Modern Age: deliberate unions (federations) ---
FEDERATION_TEMPLATES = [
    "{tribe} and {enemy} formed a federation on {planet}, pooling their strength under a shared government.",
    "Through treaty and shared purpose, {tribe} and {enemy} merged into a single federation on {planet}.",
    "{tribe} and {enemy} set aside their differences and federated on {planet}.",
    "A new federation was born as {tribe} and {enemy} united their societies on {planet}.",
]

# --- Future Age: deliberate unions (unification) ---
UNIFICATION_TEMPLATES = [
    "{tribe} and {enemy} unified into a single civilization on {planet}, their peoples and technologies merging as one.",
    "{tribe} absorbed {enemy} on {planet}, the two societies becoming a single unified power.",
    "Through shared purpose, {tribe} and {enemy} merged into one civilization on {planet}.",
    "{tribe} and {enemy} set aside the last of their differences, uniting as one people on {planet}.",
]

ERA_TRANSITION_TEMPLATES = {
    "middle_ages": [
        "Generations passed. The scattered tribes of the ancient world grew into kingdoms, and the Middle Ages began.",
        "The old tribal ways faded into legend as villages became cities and chieftains became kings — the Middle Ages had dawned.",
        "Out of the ashes of the ancient world rose castles, crowns, and creeds. A new age had begun.",
    ],
    "modern_age": [
        "Generations passed. The kingdoms of old gave way to industry and innovation — the Modern Age had begun.",
        "Steel and circuitry replaced sword and scepter as the kingdoms transformed into modern societies.",
        "Out of the old kingdoms rose factories, networks, and new ideologies. A new age had begun.",
    ],
    "future_age": [
        "Generations passed. Modern societies pushed beyond their limits, and a new age of science and machines dawned.",
        "The boundaries of the possible fell away as societies raced toward a new horizon — the Future Age had begun.",
        "Industry gave way to intelligence beyond flesh. A new age of breakthroughs — and breaking points — had begun.",
    ],
}

# --- Modern Age: the founding of named societies ---
SOCIETY_FOUNDED_TEMPLATES = [
    "{tribe} rises from the ashes of the old kingdoms, a {government} on {planet} led by {leader}.",
    "On {planet}, {tribe} emerges as a {government}, with {leader} at its helm.",
    "The modern age finds {tribe} reborn as a {government}, guided by {leader}.",
    "{tribe} takes its place among the great powers of {planet}, a {government} under {leader}.",
]

# --- Modern Age: epilogue for the societies that endure to the end ---
EPILOGUE_TEMPLATES = [
    "{tribe} endures to the end, a {government} on {planet}, still led by {leader}.",
    "In the end, {tribe} remains standing on {planet} — a {government} under {leader}.",
    "{tribe} survives into the new age as a {government}, with {leader} still at the helm on {planet}.",
    "History remembers {tribe}, a {government} on {planet} that endured under {leader}, to the very end.",
]


def render_event(event, chooser: TemplateChooser = None) -> str:
    ctx = dict(tribe=event.tribe, enemy=event.enemy, planet=event.planet, leader=event.leader, government=event.government)
    chooser = chooser or TemplateChooser()

    if event.category == "tick":
        return f"\n=== Age {event.tick} ==="

    elif event.category == "era":
        templates = ERA_TRANSITION_TEMPLATES.get(event.event_type, ["A new age dawned across the land."])
        banner = "=" * 50
        return f"\n\n{banner}\n{chooser.choose(templates)}\n{banner}\n"

    elif event.category == "climate":
        templates = CLIMATE_PLANET_TEMPLATES.get(event.event_type, [f"A {{event.event_type}} occurred on {{planet}}."])
        return chooser.choose(templates).format(**ctx)

    elif event.category == "climate_tribe":
        templates = CLIMATE_TRIBE_TEMPLATES.get(event.outcome, ["{tribe} was affected."])
        return chooser.choose(templates).format(**ctx)

    elif event.category == "societal":
        if event.outcome == "destroyed":
            templates = SOCIETAL_DESTROYED_TEMPLATES
        else:
            templates = SOCIETAL_TEMPLATES.get(event.event_type, [f"{{tribe}} experienced {event.event_type}."])
        return chooser.choose(templates).format(**ctx)

    elif event.category == "conflict":
        won_templates, defended_templates = CONFLICT_TEMPLATE_SETS.get(
            event.event_type, (CONFLICT_RESOURCE_WON_TEMPLATES, CONFLICT_RESOURCE_DEFENDED_TEMPLATES)
        )
        templates = won_templates if event.outcome == "won" else defended_templates
        return chooser.choose(templates).format(**ctx)

    elif event.category == "conflict_result":
        templates = CONFLICT_LOSER_DESTROYED_TEMPLATES if event.outcome == "destroyed" else CONFLICT_LOSER_WEAKENED_TEMPLATES
        return chooser.choose(templates).format(**ctx)

    elif event.category == "merge":
        if event.event_type == "alliance":
            templates = ALLIANCE_TEMPLATES
        elif event.event_type == "federation":
            templates = FEDERATION_TEMPLATES
        elif event.event_type == "unification":
            templates = UNIFICATION_TEMPLATES
        else:
            templates = MERGE_TEMPLATES
        return chooser.choose(templates).format(**ctx)

    elif event.category == "society":
        return chooser.choose(SOCIETY_FOUNDED_TEMPLATES).format(**ctx)

    elif event.category == "epilogue":
        return chooser.choose(EPILOGUE_TEMPLATES).format(**ctx)

    elif event.category == "catastrophe":
        templates = CATASTROPHE_TEMPLATES.get(event.event_type, {}).get(event.outcome, ["{tribe} was struck by catastrophe."])
        return chooser.choose(templates).format(**ctx)

    return ""
