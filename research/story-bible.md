# Story bible

The single source for the story layer. Read it before you write or edit any `::: {.ao-story}` block, persona text or art. Settled with the maintainer on 2026-11-26 after a grilling round. The lesson body never uses story words (see AGENTS.md).

## Premise

A Blight spreads across the realm: plausible but false knowledge, grown wherever a traveller accepts power without checking it. Travellers gather at **Gaia's Rest**, a tavern at the root of the great tree, to make pacts with **Astrals** that let them do extraordinary things. The party learns the disciplines of the pact so the power does not turn into Blight.

The Blight is not a monster from outside. It is what happens when a pact-bearer accepts gifts unexamined.

## Creatures (all are **Shokanju**, the umbrella word for summoned creatures, same form for one or many; they are summoned, never hired)

| Kind | Real thing | Nature |
|---|---|---|
| **Automata** | scripts, pipelines, Nextflow, Snakemake | clockwork, obedient, no imagination, no Blight risk, brittle when the road changes |
| **Familiars** | classical ML models | trained by beastmasters for one quarry; fast and trustworthy there, useless elsewhere |
| **Astrals** | LLMs | masters of many tongues and tasks; generous, fast, and unbound from physical reality, so they invent when unchecked |

- The **Claude Astral** is bound with Claude Code. **Lesser Astrals** (local models, less powerful) are bound with OpenCode and Ollama.
- Retired story words: kennel master, the Beast, pet, tongue-spirit, armour, carapace, shield, "companion" as the word for the agent. The tab group named `companion` in code and saved state keeps its name.

## The harness vocabulary (story words only)

| Story | Lesson word |
|---|---|
| binding circle | the harness (tools, boundary) |
| making the pact | installing and starting the agent |
| terms of the pact | the instructions file |
| wards | permission rules and the sandbox |
| trials | tests and checks |

## Places

- **Gaia's Rest** (chapter folder `worries`): the tavern at the foot of a great tree, where the adventure starts. Boasters tell tales of extraordinary pacts. A few patrons sit sullen in a corner, drowning their sorrows in drink or staring at cold food. **Wanderer Quill**, an old wanderer, greets the party, recounts the four patrons' tales (Name the Fears) and sends them to the Sages at the Collegium with the other worries patrons have carried through the door. The **Summoning Scroll** is the Prerequisites page (story word only; the page keeps its plain title). The sages' college keeps it: Sage Maelis shows it in Know Your Tools and reads it aloud in Set Up Your Agent.
- **The Collegium** (chapter folder `agents-and-models`): an academy of three colleges, used as story labels only, where academics mill about and respect one another because each knows the strengths and weaknesses of the Shokanju (summoned beasts, never hired). The **tinkers' college** builds Automata (it leads on to the Automata Factory and has no quest of its own). The **beastmasters' college** trains Familiars (no quest of its own). The **sages' college** interprets scrolls and makes pacts with Astrals. **Sage Maelis** of the sages' college is the party's teacher for the trunk quests set here: Script, Model, or LLM (among all three colleges), Know Your Tools (she explains the pieces of the pact from the Summoning Scroll), Choose What to Hand Over (she warns that without disciplined use Astrals spread the Blight across the land, and shows how to limit what an Astral sees, because these persistent creatures draw in whatever they can reach in pursuit of their goal) and Set Up Your Agent (she reads the scroll and makes the pact with the party). The branch quests Pick Your Model, Free Is Not Free and Claude in the Cloud are hers too. The Sages warn about limits; the learner may ignore them, as the tavern patrons did.
- **Adventurers' Training Grounds** (`safe-editing`): Warden Hesper drills novices on a practice field marked with chalk lines (save points), gates and boundaries (permissions) and an armoury of locked chests (secrets). Quests: Save Point, Test Permissions and the Sandbox, Write Permission Rules, Keep Secrets Out of Reach, Plan Before You Edit.
- **The Quern Mill** (`prompts-and-context`): a hand mill with a great hopper (the context window). Miller Garrick and Scribe Linnea. When the Astral proves too unruly for the mill's chores, Garrick sends the party on to the Guild Hall.
- **Artisans' Row** (`instructions-skills-and-hooks`): a street of guilds. **Hallmaster Cass** keeps the Guild Hall and takes no apprentice who cannot check an Astral's work, which sends the party to the Swamp before they return as apprentices. The skillsmiths (Smith Dunmore) keep Skills, the gate-wardens (Watchman Corin) guard the door to outside tools (MCP), the hookwrights write rules in code (Corin), and Surveyor Rowan keeps the instructions stone in the Charter Hall.
- **The Swamp of Illusions** (`checking-output`): marsh gas makes illusions and casts the light in strange ways. Cartographer Vesna walks the party through it and notes every turn.
- **Tidewrack** (`collaboration`): a village on the reef whose people and creatures are hurt by the Blight, in work passed along unchecked. Tidewarden Nerys, Diver Kai and Net-mender Joss.
- **The Automata Factory** (`pipelines`): Tinker Pell leads the party here from the tinkers' college. Side quests.
- **Haven Quay** (`shared-clusters`): an industrious port town where people gather from all over. Gatekeeper Brisa and Queue Master Fenn. Side quests.
- **The Cave Beneath the Reef** (`final-review`): the finale. In Tidewrack the party hears whispers of a monster in a sunken cavern and presumes it a corrupted Astral poisoning the waters. Sage Maelis joins them at the cave mouth. They overcome it, then realise it was an Astral left free without bounds, and that the Blight will never truly go away while people are careless and abandon their Shokanju. The quest is Boss: Review a Messy Session. The fog over uncleared places on the overworld map is still called the Murk.

## The four cautionary patrons (in Gaia's Rest, not the party)

Each made a pact, was given the Sages' instructions, and ignored them out of hubris. They sit sullen in a corner until Wanderer Quill recounts their tales to the party. They are not the personas.

1. **Brannoch the tinker** lost his workshop when his Astral rewrote it and nothing could be restored. He skipped a save point ("I never lose files").
2. **Sefa the scholar** published an evolutionary tree that her Astral built on phantom citations. She skipped checking against ground truth ("it sounded right").
3. **Tam the steward** had his Astral copy restricted records onto a public poster. He ignored the secrets warnings ("it's only a poster").
4. **Oleander the clerk** had an Astral merge forty changed files on its own summary, and never noticed it had deleted the failing tests. She skipped review.

The boasters outside tell the tales of extraordinary pacts.

## The party (four personas)

Each persona is always written as job class and name together: Quartermaster Aris, Diviner Ilsa, Artificer Bob, Archivist Elowen. Never the class or the name alone, so readers carry no mapping in their heads. The tab headings, story blocks and alt text all follow this.

Shown as tabs (`group="persona"`) on the front page, with a portrait, role, a short backstory (about 80 words) and a "where your discipline matters most" line. Some story blocks carry a short persona tab (the first quest of each zone, Wade In and the two bosses). Dreams and fears live in Choose What to Hand Over, not on the front page. The choice is remembered by Quarto's tab group persistence. Lessons are identical for everyone.

| Persona (class and name) | Role | Existing gear | Gift of the pact | Temptation | Discipline | Lead zones |
|---|---|---|---|---|---|---|
| **Quartermaster Aris** | research or project manager | ledgers, milestone beacons, ration tokens (budget) | instant roadmaps, status summaries, fast prototypes | the illusion of done: a plausible demo taken for a validated result | rationing and sign-off: review gates and budgets | Gatehouse, Scriptorium, Citadel |
| **Diviner Ilsa** | bioinformatics analyst | trained hounds (statistics, ML) and ground-truth lenses (references, controls) | literature synthesis, expression scripts, exploratory plots | confirmation mirage: fluent explanations and phantom citations that flatter a hypothesis | provenance and ground truth: primary identifiers, negative controls, independent checks (and no phantom reagents or invented protocol steps) | Crypt, Sequence Maze, Phylogenetic Forest |
| **Artificer Bob** | bioinformatics engineer | Automata: CLI tools, scripts, pipelines, containers | workflows, refactors, test suites in seconds | spaghetti golems: merging code you have not read and cannot debug | small diffs, tests, containers; ship nothing you cannot explain | Codon Mill, Sequence Maze, Pipeline Factory |
| **Archivist Elowen** | data steward | sealed vaults, checksums, ontologies, metadata ledgers | sample-sheet cleanup, schema mapping, format conversion | silent corruption: values invented or altered while "harmonising" | immutable raw data, schema validation, audit trails, privacy wards | Gatehouse, Biodiversity Reef, Scriptorium |

## Rules for writers

- After any story change run `pixi run story` and re-read the chain it prints (place, guide, travel, what each character knows, where the Summoning Scroll is).
- Story blocks stay 3 to 5 sentences, first on the page, ending in one sentence that leads into the lesson. The lesson body, tables and diagrams use plain words only.
- Lesson titles are plain and searchable. Chapter folders and quest slugs follow what each chapter and quest teach, and any rename updates every link by hand (no redirects).
- No real company or product is a villain. Anthropic's Claude is "the Claude Astral" (a creature bound by a tool), never an antagonist.
- Art: procedural pixel art from `tools/make_art.py`, 48x48 portraits, no imitation of any existing game's characters.

## Guides, travel and themes

Every place has at least one **named guide** who supplies the knowledge there. Write a guide as class and name together ("Warden Hesper"), like the party. Each chapter folder under `zones/` is named after what it teaches, and one place covers one chapter.

| Place (chapter folder) | Theme in one line | Guide(s) |
|---|---|---|
| Gaia's Rest (`worries`) | The tavern at the foot of a great tree: the fears and the tales of people the Blight caught | Wanderer Quill gives the scroll; the four patrons tell their tales |
| The Collegium (`agents-and-models`) | Understanding the creatures and the pact: three kinds, the parts, what to hand over, installing the agent, choosing models | Sage Maelis (all her quests); Tinker Pell (tinkers' college); Beastmaster Wyn (beastmasters' college) |
| Adventurers' Training Grounds (`safe-editing`) | Undo, permissions, the sandbox, secrets, plans | Warden Hesper (she) |
| The Quern Mill (`prompts-and-context`) | How an Astral reads: tokens, failures, the context window, briefs, sessions and memory | Miller Garrick; Scribe Linnea (notes and the LLM wiki) |
| The Swamp of Illusions (`checking-output`) | Trust: spotting false output, checking it, keeping a record | Cartographer Vesna |
| Artisans' Row (`instructions-skills-and-hooks`) | The guilds: instruction files, Skills, MCP servers, hooks and evals | Hallmaster Cass (Guild Hall, mistakes log); Surveyor Rowan (instructions stone); Smith Dunmore (skills, tests, plugins); Watchman Corin (MCP gate, hooks) |
| Tidewrack (`collaboration`) | People: the Blight festers here, in work passed along unchecked | Tidewarden Nerys, Diver Kai and Net-mender Joss |
| The Automata Factory (`pipelines`) | Agents on pipelines and reproducibility | Tinker Pell, who leads you here from the tinkers' college |
| Haven Quay (`shared-clusters`) | Clusters, keys, other people's queues | Gatekeeper Brisa; Queue Master Fenn |
| The Cave Beneath the Reef (`final-review`) | The finale: review one messy session | Sage Maelis joins the party at the cave mouth |

**Travel.** The first quest of each place opens with one sentence that moves the party from the previous place, naming the road or the guide who sends them. The trunk route is Gaia's Rest, the Collegium (three quests), the Training Grounds (Save Point, while Sage Maelis prepares the pacts), back to the Collegium (Set Up Your Agent), the Training Grounds (four quests), the Quern Mill, the Guild Hall on Artisans' Row (Miller Garrick sends the party because the Astral is too unruly for the mill), the Swamp of Illusions (Hallmaster Cass sends them to learn to check an Astral's work), back to Artisans' Row as apprentices, Tidewrack, and the cave beneath the reef. Where a trunk quest returns to an earlier place, the story says "return". Side-quest chapters open from the map: the party walks there.

**Tidewrack.** Tidewrack is the only place where the Blight is already present. The guides send the party there to clean it up: handing work over, reviewing it and teaching.
