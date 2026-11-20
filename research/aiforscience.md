# AI for Science: best practices for agentic AI in science

Source: https://aiforscience.eu/ . Read 2026-11-20 through a summarising fetch subagent, not first-hand. Everything below is the subagent's report; re-check the wording on the pages before quoting.

## What the site is

- Title "AI for Science: best practices for agentic AI in science". Self-described as a living record maintained by task forces and institutions across Europe, versioned for citation. Partners shown on the home page: Helmholtz Munich, Helmholtz AI, ELIXIR. The home page marks it as a preview. Source repository: https://github.com/slolab/aiforscience.eu . Content licence CC-BY-4.0. Citable release DOI 10.5281/zenodo.21709875.
- Status: every practice page we read is marked "draft", "Endorsement: none yet". Last-reviewed dates 2026-09-16 (01, 04, 07, 08) and 2026-10-27 (11). Treat these as proposals under discussion, not as agreed standards. The site itself flags some of its source attributions as unverified (for example in practice 04) and calls one cited paper self-audited (practice 07).
- Not read: the About and governance pages, the failures log, the library and glossary pages. We could not confirm who operates the site beyond the repository owner name.

## Pages read

Read in full (URLs used in Lore):

- https://aiforscience.eu/short-version/ : the one-page decision summary.
- https://aiforscience.eu/best-practices/01-match-method-to-task/ : practice 1.
- https://aiforscience.eu/best-practices/04-govern-autonomy-and-accountability/ : practice 4.
- https://aiforscience.eu/best-practices/07-provenance-and-citation/ : practice 7.
- https://aiforscience.eu/best-practices/08-evaluate-tools-before-trust/ : practice 8.
- https://aiforscience.eu/best-practices/11-decide-where-research-data-may-go/ : practice 11.

Not opened (one-line summaries only, from the short-version page): practices 02 (make resources agent-accessible), 03 (register and vet interfaces such as MCP servers, skills and plugins), 05 (write documentation and data for agents), 06 (design interfaces around user tasks), 09 (state human-in-the-loop requirements), 10 (screen for dual-use and high-consequence risk). The course makes no claim from these six.

## What the course took, and where

All in our own words, labelled as the site's draft guidance.

| Practice | Idea used | Quest |
|---|---|---|
| 01 Match method to task | Ask first whether a script, fixed workflow or smaller specialised model does the job; a fitting method is cheaper to run, easier to reproduce, and does not change when a provider updates a model (the page cites Chen et al. 2024 for drift under the same version name; not checked by us). | Three Kinds of Machine |
| 04 Govern autonomy | Limits belong in the system (permission scopes, spend caps in the metering system, stop paths), each agent duty has a named human owner, actions are logged, personal agents count. Example on the page: an agent with shell access on a shared server deleted another group's data. | Advice or Enforcement |
| 07 Provenance and citation | Cite by persistent identifier and generate references with a deterministic tool; keep retraction status; say what a human did and what an agent did; disclose agent use where results are published; record model version, inputs and tool calls. The page cites ICMJE and COPE (AI cannot be an author; disclose use) and the Commission's living guidelines on generative AI in research (2026); we did not verify those texts or the EU AI Act dates it lists. | Ground Truth |
| 08 Evaluate before trust | Task-specific tests on cases with known answers, repeated runs, record failure modes, re-test when the tool or task changes; a model from the same family is not an independent grader; check a sample of model-judged results by hand against answers fixed in advance. The page cites Panickssery, Bowman and Feng 2024 for self-preference (not checked by us). | Close the Loop |
| 11 Where data may go | An agent on a hosted model sends what it reads to the provider, so reading a file already discloses it. Example on the page: an agent that opens a project `.env` leaves keys in provider logs, so rotate them. Sending personal data is processing under GDPR (lawful basis, processor contract, transfer basis outside the EU) even if the provider does not train on it. Use institutional accounts. Limit where an agent may send data through its environment, not only through instructions. | Secrets and Sensitive Ground |

Not adopted: the funding and institutional-policy parts of each practice (aimed at institutions and funders; the course is written for individual researchers). Human-in-the-loop (09) could be a later addition once the page is read.
