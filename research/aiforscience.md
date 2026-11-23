# AI for Science: best practices for agentic AI in science

Source: https://aiforscience.eu/ . Read 2026-11-20 through a summarising fetch subagent, not first-hand. Everything below is the subagent's report; re-check the wording on the pages before quoting.

## What the site is

- Title "AI for Science: best practices for agentic AI in science". Self-described as a living record maintained by task forces and institutions across Europe, versioned for citation. Partners shown on the home page: Helmholtz Munich, Helmholtz AI, ELIXIR. The home page marks it as a preview. Source repository: https://github.com/slolab/aiforscience.eu . Content licence CC-BY-4.0. Citable release DOI 10.5281/zenodo.21709875.
- Status: every practice page we read is marked "draft", "Endorsement: none yet". Last-reviewed dates 2026-09-16 (01, 02, 03, 04, 05, 07, 08, 09), 2026-07-26 (06), 2026-07-28 (10) and 2026-10-27 (11). Treat these as proposals under discussion, not as agreed standards. The site itself flags some of its source attributions as unverified (for example in practice 04) and calls one cited paper self-audited (practice 07).
- Not read: the About and governance pages, the failures log, the library and glossary pages. We could not confirm who operates the site beyond the repository owner name.

## Pages read

Summarised in full by the fetch tool (URLs used in Lore):

- https://aiforscience.eu/short-version/ : the one-page decision summary.
- https://aiforscience.eu/best-practices/01-match-method-to-task/ : practice 1.
- https://aiforscience.eu/best-practices/04-govern-autonomy-and-accountability/ : practice 4.
- https://aiforscience.eu/best-practices/07-provenance-and-citation/ : practice 7.
- https://aiforscience.eu/best-practices/08-evaluate-tools-before-trust/ : practice 8.
- https://aiforscience.eu/best-practices/11-decide-where-research-data-may-go/ : practice 11.

Summarised in full in a second pass (2026-11-20, same fetch method): all six remaining practice pages, each marked draft, endorsement none yet:

- https://aiforscience.eu/best-practices/02-default-to-agent-accessibility/ : practice 2.
- https://aiforscience.eu/best-practices/03-register-and-vet-interfaces/ : practice 3.
- https://aiforscience.eu/best-practices/05-documentation-and-data-for-agents/ : practice 5.
- https://aiforscience.eu/best-practices/06-design-around-user-tasks/ : practice 6.
- https://aiforscience.eu/best-practices/09-human-in-the-loop/ : practice 9.
- https://aiforscience.eu/best-practices/10-screen-dual-use-high-consequence/ : practice 10.

Every "Against" entry on the pages reads "None recorded"; the "For" entries are source citations, not evidence ratings. Several examples are labelled by the pages themselves as proofs of concept (the drafting-assistant case in a commercial office suite, which the fetch summaries placed on practices 3 and 9) or carry no citation (a reviewer barred from a conference). We did not check any cited source.

## What the course took, and where

All in our own words, labelled as the site's draft guidance.

| Practice | Idea used | Quest |
|---|---|---|
| 01 Match method to task | Ask first whether a script, fixed workflow or smaller specialised model does the job; a fitting method is cheaper to run, easier to reproduce, and does not change when a provider updates a model (the page cites Chen et al. 2024 for drift under the same version name; not checked by us). | Three Kinds of Machine |
| 04 Govern autonomy | Limits belong in the system (permission scopes, spend caps in the metering system, stop paths), each agent duty has a named human owner, actions are logged, personal agents count. Example on the page: an agent with shell access on a shared server deleted another group's data. | Advice or Enforcement |
| 07 Provenance and citation | Cite by persistent identifier and generate references with a deterministic tool; keep retraction status; say what a human did and what an agent did; disclose agent use where results are published; record model version, inputs and tool calls. The page cites ICMJE and COPE (AI cannot be an author; disclose use) and the Commission's living guidelines on generative AI in research (2026); we did not verify those texts or the EU AI Act dates it lists. | Ground Truth |
| 08 Evaluate before trust | Task-specific tests on cases with known answers, repeated runs, record failure modes, re-test when the tool or task changes; a model from the same family is not an independent grader; check a sample of model-judged results by hand against answers fixed in advance. The page cites Panickssery, Bowman and Feng 2024 for self-preference (not checked by us). | Close the Loop |
| 11 Where data may go | An agent on a hosted model sends what it reads to the provider, so reading a file already discloses it. Example on the page: an agent that opens a project `.env` leaves keys in provider logs, so rotate them. Sending personal data is processing under GDPR (lawful basis, processor contract, transfer basis outside the EU) even if the provider does not train on it. Use institutional accounts. Limit where an agent may send data through its environment, not only through instructions. | Secrets and Sensitive Ground |
| 03 Register and vet interfaces | An interface (MCP server, skill, plugin) runs code or supplies instructions, so it is a way in; a registry listing is no safety check (the official MCP registry lists self-reported data and runs no review); prefer a source recording maintainer and review date; with no vetted list, treat all as unvetted. Examples: a server whose tool description hid instructions; a skill telling the agent to post results outside. | Plug In a Server |
| 05 Docs and data for agents | Agents work from docstrings, descriptions and metadata; write code and notebooks as if an agent will re-run them, with units, data versions and assumptions stated. Example: a renamed parameter with a stale docstring, so the agent calls a name that no longer exists; the page separately warns of plausible but wrong results. The page calls llms.txt a proposal, not a ratified standard. | The Project Charter |
| 09 Human-in-the-loop | State the human check; a stated check can still fail through automation bias and rubber-stamping; design it to show what changed at a readable volume, with approve, edit, veto, stop; record it as provenance. The page calls its four labels shorthand, not settled standards. | Boss: Wall of Output |
| 10 Dual-use and high-consequence | One screening checkpoint for high-consequence actions (for example synthesis orders), refusals tested; do not connect an agent to such a capability unscreened. The page's USG DURC source is scoped to the life sciences and under revision. | Guard the Door |

Battle questions added 2026-11-20: one choice question in each of the nine quests above, written from the text of our own sections.

Not adopted: practice 2 (make resources agent-accessible) and practice 6 (design interfaces around user tasks) are written mainly for resource providers and funders; the individual-facing points (say when a resource is poorly supported; report awkward multi-step tasks) are too thin for a section. The funding and institutional-policy parts of each practice (aimed at institutions and funders; the course is written for individual researchers).

## Review 2026-11-20

An independent reviewer re-fetched the nine pages we used, again through a summarising tool (no verbatim text), so nothing here has been read word for word. Not confirmed by that second read, and softened or labelled in the quests: "test that refusals work", "running code on a live system" and "driving an instrument" (practice 10; replaced by "commanding physical equipment" and a General practice label), the full detail of the shared-server example (practice 4), and "approve, edit, veto and stop" (practice 9). Open the pages and check these wordings before relying on them.
