# Agent Odyssey

A role-playing course on using LLM coding agents safely in bioinformatics. It is written for people who may never have used these tools, and for sceptics who want to know where the risks sit before deciding.

**Play it: <https://mahesh-panchal.github.io/agent-odyssey/>**

> Status: first draft, not v1. The content and the learning path are stable enough to walk through. Expect rough edges and changes.

## What it is

A static website built with [Quarto](https://quarto.org/). You walk an overworld map, clear quests, and answer short quizzes (choice, ordering, sorting, matching and spot-the-faulty-line). The site calls no LLM, and every exercise runs on tiny mock data in your browser or on your laptop. Progress lives in your browser, and a save code lets you move it between machines.

The story is simple. A Blight is spreading: plausible but false knowledge that grows when nobody checks. You recruit a companion, build armour, and learn the habits that keep the Blight small.

Using an agent is always your choice. The course shows how to do it with care, and it says plainly when the right answer is to use a script or nothing at all.

## How to walk it

Open **Start Here** on the site. The path is a trunk, then branches, then a final boss:

- **Trunk (14 quests):** worries and habits, kinds of machine, how much to hand over (a step-by-step way in that needs no agent), tokens and failure modes, the context window, an undo point, your first agent, its armour, secrets, and trust in output. It ends with the mid-boss, the Wall of Output.
- **Eight branches, by interest:** memory and sessions, skills and plugins, guards (MCP and hooks), pipelines, notebooks, shared clusters, working with people, and models and cloud.
- **Final boss:** *Clear the Murk* opens when you finish the trunk and any three branches.

Only the final boss waits for conditions. Every other quest stays open, and the order is advice.

## What it covers

Fears and counter-habits, how models read text, where they fail, memory and sessions, choosing models and effort, undo and permissions, secrets and unpublished work, checking output against something the agent did not write, skills and plugins, MCP servers and hooks, pipeline dry runs, notebooks, shared HPC clusters, review etiquette, and keeping your own voice and judgement.

Every quest ends with a **Lore** block of sourced further reading. A generated Lore library page collects them all.

## Run it locally

You need [pixi](https://pixi.sh/).

```bash
pixi install
pixi run preview     # live preview
pixi run render      # build the site into _site/
pixi run e2e         # drive the built site with real key presses
pixi run lore        # lint the Lore blocks and rebuild the Lore page
pixi run shots       # screenshots for visual review (.shots/)
pixi run publish     # publish to GitHub Pages (gh-pages branch)
```

`pixi run e2e` needs a headless browser once: `quarto install chrome-headless-shell`.

The learning path lives in `zones.yml` (gates, quests, prerequisites, branches, finale). The build validates it and generates the data the site reads.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a quest and the content rules, and [REVIEW.md](REVIEW.md) for the review checklist. In short:

- Check tool facts against official documentation and record the sources in `research/`.
- Label claims honestly: "Verified: ran ..." only when you ran it, otherwise "Last verified (docs, not run)", "General practice" or "Not checked:".
- Keep exercises on mock data, never real or sensitive data.
- Write for sceptics: mitigations over cheerleading, and no hint that LLM use is mandatory.

Issues and suggestions are welcome.

## Licence

Code (JavaScript, CSS, Python tools) is under the MIT licence in [LICENSE](LICENSE). The written content, quests, test banks and generated artwork are under [CC BY 4.0](LICENSE-CONTENT).
