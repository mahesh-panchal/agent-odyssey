# Claims ledger: The Kennel (learner-facing cleanup)

Format: removed text | original label | action. Sources: research/kennel-and-crypt.md, doctor.md, claude-cloud.md, free-models.md, mistral.md, apple-foundation-models.md, model-and-effort.md.

## Recruit the Beast
- Removed: ao-badge "Last verified (docs, not run): Claude Code v2.1.323 on 2026-11-13 ... docs change quickly" | label: Last verified | action: dropped (sources stay in research notes).
- Removed: "The docs say to use bypassPermissions only in containers or VMs" | label: docs say | action: stated plainly (confirmed).
- Removed: /doctor "suggests it runs through the model and may use some of your usage (our inference)" | label: inference | action: dropped (unconfirmed in doctor.md).
- Removed: "Not checked: whether /doctor covers keybindings, sandbox, MCP validity, network calls" | label: Not checked | action: dropped.
- Removed: "OpenCode: CLI docs list no doctor or status command ... Not checked: its TUI slash commands" | label: Not checked | action: kept only the confirmed `opencode debug paths`; negation and unchecked part dropped.
- Removed: "The docs give no advice on [redacting], so the check is ours"; "General practice" | label: General practice | action: kept as a firm habit ("Read any output before you paste it"), label dropped.
- Removed: "(v2.1.252+)" on /skill-doctor | label: version note | action: dropped.
- Removed: callout-warning on subscription login versus API key | action: turned into callout-note with the confirmed fact and the action (/status, unset).
- Removed: "The docs say to use [claude doctor] when claude will not start" | action: stated plainly (confirmed).
- Removed mid-text: none beyond "Save Point" in prerequisites (kept as link in header).

## Adopt the Pet
- Removed: ao-badge "Last verified ... Ollama v0.40.16, OpenCode v2.3.0 ... Mistral tags 2026-11-20" | action: dropped.
- Removed: callout-warning "Some details are unconfirmed" and the "Unconfirmed" section | action: dropped; see items below.
- Removed: "WSL: neither tool publishes WSL guidance; installing in WSL is our best guess" | label: unconfirmed | action: turned into learner action ("run the Linux commands in your WSL terminal and check current docs if one fails").
- Removed: "OpenCode is in a version change: its pages differ on some config keys" | label: unconfirmed | action: turned into "if a snippet errors, check the current OpenCode docs for your version".
- Removed: "Small models are more error-prone than large ones ... vendors do not document it" | label: general experience | action: turned into learner action ("check its answers before you rely on them").
- Removed: "The docs make no promise that a model fits your RAM, so test it" | action: turned into action (`ollama ps`).
- Removed: "A bigger context ... can push work onto the CPU, which is slow, so the Pet may be a patient companion" | label: inference (research says inference, not measured) | action: reworded to the documented check (PROCESSOR column of `ollama ps`).
- Removed: "Ollama's docs say" / "OpenCode says it requires 64k" / "docs also warn" attributions | action: stated plainly (confirmed in kennel-and-crypt.md).
- Removed: "We ran ministral-3:8b ... gave valid JSON but misread a note"; "Not checked: how ministral-3 behaves as an OpenCode backend" | label: own run / Not checked | action: first dropped (forward reference to a later quest), second dropped. Link to Grow a Graph with Ollama moved to Related.
- Removed: Mistral Vibe pointer to Pick Your Companion | action: moved to Related.
- Removed: Free Is Not Free pointer in the body | action: moved to Related.
- Removed: Apple "macOS 27 changes the model (June 2026)" and "Python SDK (March 2026)" | label: Last verified/updates page | action: dropped (not needed for the task).
- Removed: "Not checked: whether OpenCode, Claude Code or other agents can use the Apple model" | label: Not checked | action: dropped.
- Removed: "a helpful guide to what to ask of any small local model" | label: our generalisation | action: dropped (research says the table is for the small on-device model only).
- Removed: "Model names change quickly" kept as action; "Sizes and licences: Last verified" | action: label dropped, sizes stated plainly (confirmed in mistral.md).

## Pick Your Companion
- Removed: ao-badge "Last verified (docs, not run) ... spot-checked 2026-11-17 ... Mistral read 2026-11-20" | action: dropped.
- Removed: "One article's advice, not confirmed: effort cannot add knowledge the model lacks" | label: ARTICLE-ONLY | action: dropped from body; table row now says "a stronger model may know more"; bank text edited.
- Removed: "Treat that as a hypothesis to test" | action: dropped; "Start from this table and test each row on your own jobs" kept as action.
- Removed: "Pin a full name ... (our inference from how aliases work)" | label: inference | action: stated plainly (pin is defined in Words to know; pin variables confirmed).
- Removed: Sonnet 5.5 default disagreement "the two pages disagree, so name the surface" | action: stated as plain fact (medium in Claude Code, high on the API) plus "run /effort".
- Removed: "Sketch, not run" on subagent example and OpenCode frontmatter example | action: dropped.
- Removed: "Not checked: which model OpenCode's general/explore subagents use, small_model key, OpenCode agent file location, local model as cheap delegate, Ollama as Claude Code subagent" | label: Not checked | action: dropped.
- Removed: "Why `medium`? The docs say Haiku 5.5 at low is more likely to skip..." | action: stated plainly (confirmed).
- Removed: "The docs list Haiku as suited to subagent tasks; most workloads start with Opus. Everything else is General practice" | action: the two confirmed facts stated plainly; table kept as "Starting points ... test each row on your own jobs" (action).
- Removed: "The order (check, effort, model) is one article's advice"; claude.dev article byline/date/provenance paragraph | label: ARTICLE-ONLY | action: ladder kept as a practice to test (verify-first and effort-as-better-lever are confirmed); article paragraph dropped; bank explain edited (two places).
- Removed: "Keep edits on the main model (article)" | label: ARTICLE-ONLY | action: dropped.
- Removed: "compact first, or switch at a natural break (article)" | label: ARTICLE-ONLY | action: dropped; kept confirmed cache-behaviour note and "switch at a quiet moment".
- Removed: Mistral section hedges: "Ollama's mistral-small page may be an earlier release than Small 4", Devstral deprecation dates, "Premier models show no open licence", "smart-approve (a classifier; we did not read its details)", "Ollama untested", "Not run: Vibe", "instruction-file page: search summary names AGENTS.md" | label: Not checked / search only / inference | action: dropped; smart-approve and Ollama setup turned into "check the Vibe docs"; models line says check Mistral's page for names and deprecation dates.
- Removed: "General practice: start in ask until you trust the project" | action: kept as firm imperative, label dropped.
- Removed: answer key "General practice, not from the docs" | action: label dropped.
- Removed mid-text quest references: Know Your Gear, Plan Before You Edit, Ground Truth, Where Machines Fail, When to Start Fresh, Close the Loop, Test the Skill, "as Adopt the Pet showed" | action: terms defined inline; Plan Before You Edit, Close the Loop, Test the Skill, Ground Truth, When to Start Fresh, Know Your Gear moved to Related.
- Removed: "A subagent definition can also limit what the helper may use: the Lore docs give syntax" | action: shortened to a one-line pointer.

## Claude in the Cloud
- Removed: ao-badge "Last verified ... 2026-11-17 ... plan terms, limits and retention periods change" | action: dropped; "Check your own plan" kept as action.
- Removed: paragraph attributing ideas to a claude.dev article (byline Addy Osmani, date, "not verified") | label: ARTICLE-ONLY / provenance unverified | action: dropped. The article's Lore entry is unchanged (Lore not edited).
- Removed: "One article's advice: pick the narrowest network level" | label: ARTICLE-ONLY | action: kept as an imperative practice ("Pick the narrowest level that lets the task finish"), docs-gives-no-recommendation note dropped.
- Removed: "One article's habit: commit as you go" | label: ARTICLE-ONLY | action: turned into "Commit and push work you want to keep".
- Removed: "plan on files being gone afterwards (our inference)" | label: inference | action: dropped, replaced by the commit-and-push action.
- Removed: "One article's claim: parallel sessions use the limit faster" | label: ARTICLE-ONLY | action: dropped.
- Removed: "One article's advice: local beats cloud for local databases, VPN, hardware" and "last two rows partly our inference ... docs do not mention VPN, on-prem, cluster filesystems" | label: inference | action: dropped as claims; kept the firm table rows and one sentence ("roughly 30 GB disk, no GPU is listed; GPU, VPN or local-database work stays on your side").
- Removed: "This site's rule (our own rule; the docs make no such claim)" and "docs give no guidance for genomic, patient or controlled-access data, nor data location" | label: our own / NOT documented | action: rule kept firm, attribution dropped; "docs give no guidance" dropped.
- Removed: "The proof-command habit is one article's advice" | label: ARTICLE-ONLY | action: kept the ticket example (it is a format, not a claim); attribution dropped.
- Removed: OpenCode tab "We found no hosted cloud-session feature ... Not checked: Ollama ... no equivalent to teach" | label: unconfirmed | action: the negative claim dropped; kept the practical line (run it in your own container or VM) and the local-model note.
- Removed: "(per the docs)" / "the docs say" attributions on VM image, what stays behind, retention, network None, env vars, ZDR/HIPAA/CMEK, modes, timeouts, ceilings | action: stated plainly (confirmed in claude-cloud.md).
- Removed: "These figures are time-sensitive" (retention), "(time-sensitive: check your plan)" (shared usage) | action: turned into "check your own plan".
- Removed: answer key "our judgement", "General practice, not from the docs", "General practice, not a vendor claim" | action: labels dropped.
- Removed: mid-text quest references (Know Your Gear, Grow the Carapace, Plan Before You Edit, The Wall of Output, The Reviewer's Code, Save Point, The Locked Cabinet) | action: terms defined inline; links moved to Related and header prerequisites.
- Removed: callout-important wrapper type | action: same firm rule kept in a callout-note (the lint flags callout-important as a caveat callout).
- Removed: bank wording "the docs say ..." in 3 misconceptions; "No HPC filesystem or local database is documented" | action: reworded plainly.

## Free Is Not Free
- Removed: ao-badge "Last verified (docs, not run): provider pages ... 2026-11-20, summarising tool. Limits change often" | action: dropped; "treat every number as a snapshot, read the provider's page" kept as action.
- Removed: awesome-free-models paragraph ("over two hundred", banner corrections on 2026-11-14, three-day trial) | label: secondary source | action: replaced by one plain sentence ("providers have ended, shrunk or turned free tiers into short trials"); the list stays in Lore.
- Removed: "The list we read says nothing we could confirm about who pays for such sites" | label: NOT CONFIRMED | action: turned into the firm rule "ask who pays; send such a site nothing you would not post publicly".
- Removed: "OpenCode Zen says ...", "Cloudflare says ...", "Google's terms say ...", "Groq says ...", "OpenRouter says ..." | label: X says Y | action: stated as plain facts about each service (confirmed in free-models.md); no numbers beyond Groq's 30 days.
- Removed: "Claude Code does not use [an OpenAI-compatible protocol], so a free model usually means a different harness" | label: not in research notes | action: dropped.
- Removed: "Most free endpoints speak an OpenAI-compatible protocol" | label: unconfirmed generalisation | action: softened to "often"; learner is told to take the base URL from the provider's page and to test the model on a small task.
- Removed: "Not checked: how any particular free model behaves as an OpenCode backend" | label: Not checked | action: turned into "test one on a small task before you trust it".
- Removed: "This snippet ... was not run for any provider here" | label: not run | action: dropped.
- Removed: mid-text links to The Locked Cabinet (twice), Adopt the Pet | action: prerequisites in header plus Related; sensitive-data rule kept firm in the body.

## Move: Mistral terms block (2026-11-23)
- The Mistral data-terms block (training by product, opt-outs, zero data retention, global vs EU endpoint, local open-weight via Ollama) moved from zones/safe-editing/keep-secrets-out-of-reach.qmd to a new section "A worked comparison: Mistral's terms" in zones/agents-and-models/free-is-not-free.qmd. Facts kept are those CONFIRMED in research/mistral.md section 4; Locked Cabinet keeps one sentence ("Other providers' terms differ by product and plan"). A Lore item for the Mistral training-terms page (source in research/mistral.md section 4) now sits in Free Is Not Free; the Locked Cabinet had no Mistral-only Lore item. No bank question depended on the block.

- Free Is Not Free, Mistral section: the bullet that tool or web calls a local model makes may still send data out is general advice, not from research/mistral.md.
