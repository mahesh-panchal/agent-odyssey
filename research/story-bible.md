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

- **Gaia's Rest** (zone slug `basecamp`): the tavern where the adventure starts. Boasters tell tales of extraordinary pacts. A few patrons whisper, quietly, of the devastation they caused. **Wanderer Quill**, an old wanderer, hands each traveller the **Summoning Scroll**, which is the Prerequisites page (story word only; the page keeps its plain title).
- **The Collegium** (zone slug `kennel`): an academy of three colleges, used as story labels only, where academics mill about and respect one another because each knows the strengths and weaknesses of the Shokanju (summoned beasts, never hired). The **tinkers' college** builds Automata (it leads on to the Pipeline Factory and has no quest of its own). The **beastmasters' college** trains Familiars (Should You Fine-Tune?). The **sages' college** interprets scrolls and makes pacts with Astrals. **Sage Maelis** of the sages' college is the party's teacher for the trunk quests set here: Script, Model, or LLM (among all three colleges), Know Your Tools (she explains the pieces of the pact from the Summoning Scroll), Choose What to Hand Over (she warns that without disciplined use Astrals spread the Blight across the land, and shows how to limit what an Astral sees, because these persistent creatures draw in whatever they can reach in pursuit of their goal) and Set Up Your Agent (she reads the scroll and makes the pact with the party). The branch quests Pick Your Model, Free Is Not Free and Claude in the Cloud are hers too. The academics warn about limits; the learner may ignore them, as the tavern patrons did.
- Other zones keep their names (Ancient DNA Crypt, Codon Mill, Sequence Maze, Phylogenetic Forest, Gatehouse, Biodiversity Reef, Pipeline Factory, Scriptorium, Cluster Citadel, The Murk's Heart). Their guides are in the next section. The Crypt track label is "Wards".

## The four cautionary patrons (in Gaia's Rest, not the party)

Each made a pact, was given the academics' instructions, and ignored them out of hubris. They whisper their tales in a corner. They are not the personas.

1. **Brannoch the tinker** lost his workshop. He skipped a save point ("I never lose files").
2. **Sefa the scholar** published an evolutionary tree built on phantom citations. She skipped checking against ground truth ("it sounded right").
3. **Tam the steward** pasted restricted records into a chat. He ignored the secrets warnings ("it's only a chat").
4. **Oleander the clerk** shipped a demo that "ran fine". She skipped review.

The boasters outside tell the tales of extraordinary pacts.

## The party (four personas)

Each persona is always written as job class and name together: Guildmaster Aris, Diviner Ilsa, Artificer Bob, Archivist Elowen. Never the class or the name alone, so readers carry no mapping in their heads. The tab headings, story blocks and alt text all follow this.

Shown as tabs (`group="persona"`) on the front page, with a portrait, role, a short backstory (about 80 words) and a "where your discipline matters most" line. Some story blocks carry a short persona tab (the first quest of each zone, Wade In and the two bosses). Dreams and fears live in Choose What to Hand Over, not on the front page. The choice is remembered by Quarto's tab group persistence. Lessons are identical for everyone.

| Persona (class and name) | Role | Existing gear | Gift of the pact | Temptation | Discipline | Lead zones |
|---|---|---|---|---|---|---|
| **Guildmaster Aris** | research or project manager | ledgers, milestone beacons, ration tokens (budget) | instant roadmaps, status summaries, fast prototypes | the illusion of done: a plausible demo taken for a validated result | rationing and sign-off: review gates and budgets | Gatehouse, Scriptorium, Citadel |
| **Diviner Ilsa** | bioinformatics analyst | trained hounds (statistics, ML) and ground-truth lenses (references, controls) | literature synthesis, expression scripts, exploratory plots | confirmation mirage: fluent explanations and phantom citations that flatter a hypothesis | provenance and ground truth: primary identifiers, negative controls, independent checks (and no phantom reagents or invented protocol steps) | Crypt, Sequence Maze, Phylogenetic Forest |
| **Artificer Bob** | bioinformatics engineer | Automata: CLI tools, scripts, pipelines, containers | workflows, refactors, test suites in seconds | spaghetti golems: merging code you have not read and cannot debug | small diffs, tests, containers; ship nothing you cannot explain | Codon Mill, Sequence Maze, Pipeline Factory |
| **Archivist Elowen** | data steward | sealed vaults, checksums, ontologies, metadata ledgers | sample-sheet cleanup, schema mapping, format conversion | silent corruption: values invented or altered while "harmonising" | immutable raw data, schema validation, audit trails, privacy wards | Gatehouse, Biodiversity Reef, Scriptorium |

## Rules for writers

- Story blocks stay 3 to 5 sentences, first on the page, ending in one sentence that leads into the lesson. The lesson body, tables and diagrams use plain words only.
- Lesson titles are plain and searchable. Slugs never change. Only Adopt the Pet is removed (it redirects to Set Up Your Agent).
- No real company or product is a villain. Anthropic's Claude is "the Claude Astral" (a creature bound by a tool), never an antagonist.
- Art: procedural pixel art from `tools/make_art.py`, 48x48 portraits, no imitation of any existing game's characters.

## Guides, travel and themes

Every zone has at least one **named guide** who supplies the knowledge there. Write a guide as class and name together ("Warden Hesper"), like the party. Zone slugs and quest slugs never change, so Script, Model, or LLM, Know Your Tools and Choose What to Hand Over keep their `zones/basecamp/` paths while the map files them under the Collegium.

| Zone (slug) | Theme in one line | Guide(s) |
|---|---|---|
| Gaia's Rest (`basecamp`) | The tavern: the fears and the tales of people the Blight caught | Wanderer Quill gives the scroll; the four patrons tell their tales |
| The Collegium (`kennel`) | Understanding the creatures and the pact: three kinds, the parts, what to hand over, installing the agent, choosing models | Sage Maelis (all her quests); Tinker Pell (tinkers' college); Beastmaster Wyn (Should You Fine-Tune?) |
| Ancient DNA Crypt (`crypt`) | Wards: undo, permissions, the sandbox, secrets | Warden Hesper (she) |
| The Codon Mill (`codon-mill`) | How an Astral reads: tokens, failures, the context window, memory | Miller Garrick; Scribe Linnea (Keep an LLM Wiki) |
| Sequence Maze (`maze`) | Trust: spotting false output, checking it, keeping a record | Cartographer Vesna navigates the maze and keeps notes on every turn |
| Phylogenetic Forest (`forest`) | Instructing and packaging: briefs, plans, instruction files, skills, plugins, tests | Surveyor Rowan (she) for briefs, plans and the instructions stone; Smith Dunmore for skills, tests and plugins; Hunter Cass keeps the log of mistakes |
| The Gatehouse (`gatehouse`) | Guards: connecting tools safely and enforcing rules in code | Watchman Corin |
| Biodiversity Reef (`reef`) | People: the Blight festers here, in work passed along unchecked, and you are sent to help clean it up | Several guides: Tidewarden Nerys, Diver Kai and Net-mender Joss |
| Pipeline Factory (`factory`) | Craft: agents on pipelines and reproducibility | Tinker Pell, who leads you here from the tinkers' college |
| The Scriptorium (`scriptorium`) | Notebooks: reviewing and re-running them | Record Keeper Ansel |
| The Cluster Citadel (`citadel`) | Shared ground: clusters, keys, other people's queues | Gatekeeper Brisa; Queue Master Fenn |
| The Murk's Heart (`murk`) | The final boss: review one messy session | Sage Maelis returns, and the party meets the Blight she warned of |

**Travel.** The first quest of each zone opens with one sentence that moves the party from the previous place, naming the road or the guide who sends them. The trunk route is Gaia's Rest, the Collegium (three quests), the Crypt (Save Point), back to the Collegium (Set Up Your Agent), the Crypt (three quests), the Codon Mill, the Sequence Maze. Where a trunk quest returns to an earlier place, the story says "return". Branch zones open from the map: the party walks there.

**The Reef.** The Reef is the only zone where the Blight is already present. The guides send the party there to clean it up, which fits the People branch: handing work over, reviewing it and teaching.
