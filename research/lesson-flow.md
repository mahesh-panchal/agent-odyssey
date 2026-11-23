# How lessons and learning paths should flow

Research note for Agent Odyssey, written 2026-11-23. It collects the pedagogy and UX evidence behind a restructure of the course, then turns it into testable rules.

## How to read the confidence tags

The fetch tool used here returns a summary produced by a small model, not the page text. So no source below counts as "read in full" in the strict sense. The tags are:

- **Fetched summary**: the page was fetched and summarised by the tool; quotes come from that output.
- **Search snippets**: only search-result snippets or abstracts were seen.
- **Memory only**: I am relying on prior knowledge. Check before citing.

Sources that failed to load are listed at the end. Nothing here has been checked against a full primary paper, with the partial exception of the Diataxis and NN/g pages.

---

## 1. Order of material across the course

### 1.1 Whole task first, then parts (Merrill; 4C/ID)

- **Sources**: Merrill, "First Principles of Instruction", Educational Technology Research and Development 50(3), 2002, 43-59 (https://link.springer.com/content/pdf/10.1007/bf02505024.pdf). van Merrienboer, Clark and de Croock, "Blueprints for complex learning: the 4C/ID model", 2002 (https://link.springer.com/content/pdf/10.1007/BF02504993.pdf). van Merrienboer, Kirschner and Frerejean, *Ten Steps to Complex Learning* (Routledge).
- **Says**: Merrill's first principle is that learning is promoted when learners work on real-world tasks or problems, in a cycle of activation, demonstration, application and integration. 4C/ID builds a course on whole learning tasks grouped in classes from simple to complex, with support that fades, plus just-in-time information shown when a step needs it, and part-task practice only for routine skills.
- **Implies here**: Each quest should be a small complete task a bioinformatician recognises (for example, ask an agent to explore a dataset, then review what it did), not a lecture on a concept. Early quests are complete but low-risk (read-only, small data). Later quests raise the stakes (write access, scheduler, shared data). Facts a learner needs for one step (a flag, a config key) appear at that step, not in an up-front theory block.
- **Confidence**: Search snippets for both (search results and a secondary summary of 4C/ID from EduTech Wiki; the Springer PDFs were not read). Content otherwise memory.

### 1.2 Pre-training principle (Mayer)

- **Source**: Mayer, *Multimedia Learning* (Cambridge UP, 2nd ed. 2009) and *Cambridge Handbook of Multimedia Learning*; overview at https://pmc.ncbi.nlm.nih.gov/articles/PMC7940870 (fetch failed; only the search snippet was seen).
- **Says**: People learn better from a complex explanation when they first know the names and characteristics of its main components.
- **Implies here**: Introduce the vocabulary a quest uses (session, context window, tool call, permission mode, sandbox) in one short "Before you start" block with one-line definitions, before the task uses them. Do not define terms in the middle of a step.
- **Confidence**: Search snippets, and memory. The original effect was shown with narrated animations, so transfer to text is an inference.

### 1.3 Worked examples, then faded practice (Sweller; Kalyuga)

- **Sources**: Sweller, "Cognitive load during problem solving", Cognitive Science 1988; Cooper and Sweller 1987; Kalyuga, "Expertise reversal effect and its implications for learner-tailored instruction", Educational Psychology Review 2007 (https://doi.org/10.1007/S10648-007-9054-3). Cited via https://en.wikipedia.org/wiki/Cognitive_load.
- **Says**: Novices learn more from studying worked solutions than from solving the same problems unaided, because searching for a solution consumes working memory. As knowledge grows the benefit shrinks and can reverse (expertise reversal), so guidance should fade. Wikipedia's page notes some researchers question the subjective load measures behind these studies.
- **Implies here**: Early quests show a complete agent transcript (prompt, plan, diff, check) and ask the learner to read it and answer one question. Middle quests give a half-finished transcript to complete. Late quests give only the goal. Because the audience mixes beginners and experienced bioinformaticians, offer a visible "I know this" skip on the opening quest of each trunk instead of forcing the full worked example on everyone.
- **Confidence**: Fetched summary (Wikipedia on cognitive load), search snippets for Kalyuga. The fading schedule is from memory and only partly supported in snippets.

### 1.4 Prerequisite sequencing

- **Source**: Gagne, *The Conditions of Learning* (1965 and later editions); learning hierarchies. No page fetched.
- **Says**: Skills form a hierarchy; a learner who lacks a prerequisite skill fails the dependent one.
- **Implies here**: Draw the dependency graph of quests once (for example, "reading a diff" before "approving an edit"; "permission modes" before "unattended runs") and let a quest depend only on quests already completed. A learner should never meet a term whose quest comes later.
- **Confidence**: Memory only.

---

## 2. Shape of a single lesson

### 2.1 Gagne's nine events

- **Source**: Gagne, Briggs and Wager, *Principles of Instructional Design* (1992 ed.); Gagne 1985, *The Conditions of Learning*, 4th ed. A Wikipedia page was tried and returned 404.
- **Says (from memory)**: gain attention; state objectives; stimulate recall of prior learning; present content; provide guidance; elicit performance; give feedback; assess performance; enhance retention and transfer.
- **Implies here**: A quest maps onto the nine events cleanly if compressed to six visible parts: hook (scene), goal, recall (one line linking to the previous quest), do, check, wrap-up with one transfer prompt. The objectives belong at the top, as one sentence about what the learner will do. A recap belongs at the end, as the learner's own takeaways, not a restatement.
- **Confidence**: Memory only.

### 2.2 Merrill's demonstrate then apply

- **Source**: Merrill 2002 (above).
- **Says**: Demonstration should be consistent with the learning goal and include guidance; application should be practice with corrective feedback, with coaching that diminishes. A synthesis PDF could not be decoded, so this wording is from memory and a search summary.
- **Implies here**: Order inside a quest is: show it done once, then the learner does a variant, then feedback. "Tell them what they will do, do it, then check" is a restatement of this and fits.
- **Confidence**: Search snippets and memory.

### 2.3 Cognitive load, coherence, segmenting, signalling

- **Sources**: Sweller, van Merrienboer and Paas, "Cognitive architecture and instructional design", Educational Psychology Review 1998; Sweller 2010; Mayer's multimedia principles (see 1.2).
- **Says**: Learning load splits into intrinsic (topic difficulty), extraneous (caused by presentation) and germane (building schemas). Designers can only cut extraneous load. Mayer's coherence principle says to drop interesting but irrelevant material; segmenting says to let the learner control the pace through small chunks; signalling says to cue what matters (headings, bold on the key term, numbered steps).
- **Implies here**: Lore, jokes and character backstory are extraneous unless they carry the task. Keep them to the hook and to one line at the end. A quest is split into steps the learner advances one at a time, each with one action. Highlight only the thing to do or notice, not whole sentences.
- **Confidence**: Fetched summary (Wikipedia) for the load types; snippets for Mayer. The coherence effect is mostly shown for multimedia; the size for plain web text is not established here.

### 2.4 Where objectives, recap and quiz go

- **Source**: Gagne (2.1); Diataxis tutorials page, https://diataxis.fr/tutorials/ (fetched summary).
- **Says**: Diataxis advises showing the end goal up front ("what the learner will build or accomplish, not promising what they will learn") and giving the expected output at each step so the learner can tell they are on track.
- **Implies here**: One-sentence goal at the top. Check questions sit directly after the step they test, not collected at the end of a long page. Each step states what the learner should see when it worked. A closing quiz, if any, has three questions or fewer and tests the decision the quest taught.
- **Confidence**: Fetched summary (Diataxis); the quiz-length figure is my own design choice, not from a source.

---

## 3. Reference, tutorial, how-to, explanation (Diataxis)

- **Sources**: https://diataxis.fr/ (home page only gave the four-way split), https://diataxis.fr/tutorials/, https://diataxis.fr/tutorials-how-to/, https://diataxis.fr/explanation/, https://diataxis.fr/reference/. Author: Daniele Procida.
- **Says**: Four forms serve four needs. A tutorial is a learning-oriented practical activity with a achievable goal; it "is not the place for explanation", and should "provide a link or reference" instead of explaining mid-task. Tutorials and how-to guides differ because the first serves someone studying and the second someone already competent doing a task; mixing them harms both. Reference is neutral description and should link out to how-to, explanation and tutorials rather than add them. Explanation "tends to absorb other things", so keep instruction and description out of it.
- **Implies here**: Agent Odyssey quests are tutorials. A quest should contain doing and the minimum needed to do it. Why-it-works material (for example, why an agent can leak a secret into a transcript) goes in a separate explanation page or a clearly labelled "Why this works" section after the quest. Tool flags, settings tables and glossary entries live on reference pages. A quest never grows a settings table in the middle.
- **Placing links**: Diataxis says to link, but its pages I could fetch do not say where in the page. Putting links in a "Going further" list after the lesson is my inference from three things together: (a) Diataxis says tutorials should not be interrupted by explanation; (b) the NN/g command-links snippet says in-body links should be limited to navigation; (c) split-attention (Chandler and Sweller 1992, memory only). I found no NN/g result that tests whether mid-sentence links break reading.
- **Confidence**: Fetched summary for Diataxis pages. Link placement: inference, not confirmed.

---

## 4. Navigation and wayfinding

### 4.1 Progressive disclosure

- **Source**: https://www.nngroup.com/articles/progressive-disclosure/
- **Says**: Show a small set of core options first and reveal specialised ones on request. What appears first signals importance. Keep to two levels; more "typically have low usability". Label the control so users know what they will find. For linear tasks, staged disclosure (a wizard) works when steps are not interdependent.
- **Implies here**: The start page offers one primary action and a short list of trunks, with advanced or optional quests behind a single "More" step. A quest page shows its steps one at a time or in clearly separate blocks. Course structure is at most two levels deep (trunk, quest), with branches reached from the quest end, not a third menu level.
- **Confidence**: Fetched summary.

### 4.2 Chunking and scanning

- **Sources**: https://www.nngroup.com/articles/chunking/ ; https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/ ; https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/
- **Say**: Short paragraphs, 50-75 character lines, grouped related items, meaningful subheadings and lists help scanning. Without them readers fixate on the start of lines and the top of the page (F pattern). Users see roughly the first two words of list items and links, so those words should carry the meaning. NN/g recommends bulleted lists and making key words look different. The chunking article warns the "magical number seven" is often misapplied.
- **Implies here**: Prefer a list whose items start with the key term over a paragraph with run-in bold labels, when the reader needs to find an item. Headings and link text begin with the distinctive word ("Permission modes", not "A look at how permission modes work"). Do not use seven as a hard cap; the cap in rule 3 below is a design choice.
- **Confidence**: Fetched summary. NN/g does not (in what I saw) directly compare lists with run-in bold labels; that preference is my inference from the scanning findings.

### 4.3 "You are here" and next-step cues

- **Source**: https://www.nngroup.com/articles/progress-indicators/ (search snippet only); NN/g "Visibility of System Status" heuristic (https://www.nngroup.com/articles/visibility-system-status/, snippet only).
- **Says**: Systems should keep users informed about where they are and what is happening. Progress indicators that show steps completed and remaining raise confidence; one NN/g test reported users waited about three times longer with a bar. This evidence concerns waiting, not learning.
- **Implies here**: Every quest page shows trunk name, step "3 of 7" and a single clearly styled Next link. Back and forward path links look different from reference links (for example, buttons at the page end versus plain links in a list). The sidebar marks the current quest.
- **Confidence**: Search snippets. Applying wait-time findings to course progress is an analogy.

### 4.4 Serial position

- **Source**: NN/g serial position URL returned 404 and search did not surface an NN/g page. Secondary pages only (Baymard, LogRocket). Original: Murdock 1962 (memory).
- **Says**: Items at the start and end of a list are remembered better than those in the middle; later studies found limits with long lists and delays (LogRocket snippet).
- **Implies here**: Put the most important action first and the next-step link last on a page. Do not bury a safety rule in the middle of a long list; give it its own heading or put it first.
- **Confidence**: Memory plus secondary snippets. Treat as weak support.

### 4.5 Tables

- **Source**: https://www.nngroup.com/articles/comparison-tables/
- **Says**: Keep cell text short, avoid full sentences, keep attributes complete across items, use consistent alignment and clear row separation.
- **Implies here**: A table holds short comparable values only (a word, a number, yes/no). If one cell needs a paragraph, that row becomes a heading with prose, or the table becomes a list. Do not put one long cell next to terse cells. This article is about comparison tables; applying it to every table is an extension.
- **Confidence**: Fetched summary.

---

## 5. Motivation and feedback

### 5.1 Immediate feedback on practice

- **Sources**: Merrill 2002 (application with feedback); Diataxis tutorials page (expected output at each step); Hattie and Timperley, "The power of feedback", Review of Educational Research 2007 (memory only).
- **Say**: Practice without feedback leaves the learner unsure whether they are right. In a static site the equivalent is showing the expected result at each step and a worked answer after each check question.
- **Implies here**: Each check question reveals its answer and a one-line reason immediately on selection (or directly below, for no-JavaScript fallbacks). Each hands-on step says what the learner should see, and what a likely failure looks like.
- **Confidence**: Diataxis fetched summary; others memory.

### 5.2 Visible progress, goal gradient

- **Sources**: Hull 1932 goal-gradient hypothesis; Kivetz, Urminsky and Zheng, "The goal-gradient hypothesis resurrected", Journal of Marketing Research 2006 (both memory only). NN/g goal-gradient article fetch timed out.
- **Says (memory)**: Effort rises as a goal gets closer; showing progress toward a goal can increase persistence. Evidence is from loyalty cards and coffee-shop settings, not courses.
- **Implies here**: Show completed quests per trunk (for example "4 of 6") and a clear finish line per trunk. Do not claim this will raise completion; it is plausible, not shown for this course type.
- **Confidence**: Memory only; unverified.

### 5.3 Gamification: mixed evidence

- **Sources**: Sailer and Homner, "The Gamification of Learning: a Meta-analysis", Educational Psychology Review 2020 (https://link.springer.com/article/10.1007/s10648-019-09498-w, snippet only); Li, Ma and Shi 2023, Frontiers in Psychology (https://www.frontiersin.org/articles/10.3389/fpsyg.2023.1253549/full, snippet only); a 2026 second-order review listed on EconPapers (abstract only, preliminary).
- **Say**: Meta-analyses find positive average effects, but sizes range from small (g about 0.26, from my memory of Sailer and Homner; the snippet did not confirm the number) to large (g = 0.82 in Li et al.). The snippet-level summary of the 2026 review says the literature probably overstates cognitive effects, with adjusted estimates of 0.29 to 0.48 and mostly low-quality underlying studies. Sailer and Homner report that effects on cognitive outcomes were stable in high-rigour studies, while motivational and behavioural effects were less stable.
- **Implies here**: The RPG frame can stay, but should not be the reason for any design choice. It must not add steps or text between the learner and the task (coherence). Points, badges and streaks are optional extras. Sceptical learners may find heavy theming off-putting; there is no evidence here on that audience either way.
- **Confidence**: Search snippets only.

---

## 6. Writing for learners

### 6.1 Keep hedging and provenance out of the lesson body

- **Source**: Coherence principle (Mayer; see 2.3); NN/g scanning findings (4.2). No source I found tests hedging in lessons directly.
- **Says**: Extraneous material, including text that does not help the task, costs attention.
- **Implies here**: State the lesson claim plainly. "How this was verified", version numbers tested and source citations move to a maintainers' note (this research/ folder) and, at most, one "Sources" link at the end. Where a claim is uncertain, the lesson should say what to do (check it), not describe the uncertainty. This is a design inference; I found no study of hedging in instructional text.
- **Confidence**: Inference from fetched and remembered principles.

### 6.2 Plain, direct style

- **Sources**: NN/g first-two-words and scanning pages (above); Plain-language guidance such as plainlanguage.gov (not fetched).
- **Says**: Front-load meaning; avoid filler openers.
- **Implies here**: Use present tense and imperative for steps ("Run the command. Read the diff."). State what a thing is, not what it is not; avoid contrastive framing ("this is not X, it is Y") unless the learner holds the wrong belief and the lesson must correct it. Define a term at first use, in the pre-training block or the first sentence it appears in. Do not point forward ("you will see later why"); if the reason matters now, give it in a clause, otherwise omit it.
- **Confidence**: The contrastive-framing and no-forward-reference rules are style choices, not findings. Fetched summary only for the scanning pieces.

### 6.3 Sceptical and novice audience

- **Sources**: None fetched. Kalyuga (expertise reversal) bears on the mixed-expertise point.
- **Implies here**: A sceptic is helped by seeing the agent's failure and the check that catches it early, in a small real task. This is a hypothesis for the course, not a cited finding.
- **Confidence**: No source; hypothesis.

---

## What this evidence does not show

- Almost every cited effect comes from controlled studies of short lessons, often multimedia with narration, tested on students. Transfer to a self-paced static website for working scientists is an assumption.
- I did not read any primary paper in full. Quotes and claims come from tool summaries of web pages, search snippets, or memory, as tagged above. Citations marked memory-only should be checked before use in any public text.
- No source I found settles where links should sit, whether run-in bold labels scan worse than lists, or the best start-page option count. Rules on those are design decisions informed by general scanning and load findings.
- Gamification meta-analyses disagree widely on size and are criticised for quality and publication bias. The evidence cannot support a claim that the RPG theme will improve completion or learning.
- Goal-gradient and progress-bar evidence comes from commerce and waiting contexts.
- Nothing here measures effects on sceptics or on LLM beginners. A small test with five learners per lesson shape, watching where they stall, would tell more than any of this.

Sources that failed: NN/g serial position and goal-gradient pages (404, timeout), the Mayer overview on PMC (connection reset), Merrill synthesis PDF (unreadable), Wikipedia nine-events page (404). The NN/g "Anchors OK? Re-Assessing In-Page Links" article (https://www.nngroup.com/articles/in-page-links/) was listed but not read.

---

## Proposed structure for Agent Odyssey

Each rule is testable by inspecting a page. Tags name the supporting principle; "(design)" marks a choice only loosely supported.

1. **Section order of a quest.** Goal (one sentence) / Before you start (terms and prerequisites) / Steps / Check / Wrap-up / Going further. No other top-level sections. *Gagne events 2-3, 6-9; Merrill demonstrate-apply; Diataxis tutorial.*
2. **Goal line.** The first line of every quest says what the learner will do or produce, in the form "You will ...". *Diataxis tutorials; Gagne event 2.*
3. **Start page choices.** The start page shows one primary action and at most 5 trunk choices; everything else is one click deeper. *Progressive disclosure; chunking; (design) for the number 5.*
4. **Depth.** Navigation has at most two levels, trunk then quest. Branches link from the end of a quest. *Progressive disclosure (two-level limit).*
5. **Step size.** One step contains one action and ends with what the learner should see. A step of more than about 6 lines of prose is split. *Segmenting; Diataxis tutorials; (design) for 6.*
6. **Terms before use.** Every term used in a quest is defined in its "Before you start" block or in an earlier quest of the same trunk. Test: no term is linked to a later quest. *Pre-training; prerequisite sequencing.*
7. **No forward references.** The body never mentions material from a later quest. Hand-offs appear only in "Next". *Prerequisite sequencing; coherence; (design).*
8. **Worked example first.** The first quest in a trunk shows a complete agent transcript before asking the learner to do anything; later quests show less. *Worked-example effect; fading; Merrill.*
9. **Skip for the experienced.** Each trunk opener has a short self-check that lets a competent reader jump ahead. *Expertise reversal.*
10. **Check placement.** A check question follows the step it tests and shows its answer with a one-line reason immediately. At most 3 per quest. *Immediate feedback; Merrill application; (design) for 3.*
11. **Reference stays out of the body.** Settings tables, flag lists and glossary entries live on reference pages. A quest body contains no table longer than 4 rows. *Diataxis reference vs tutorial; cognitive load; (design) for 4.*
12. **Links go after the lesson.** Links to reference and explanation appear in a "Going further" list at the end, not inside sentences of the Steps. Exception: the first use of a defined term may link to the glossary. *Diataxis; split attention; command-links snippet; (inference, unconfirmed).*
13. **Two link styles.** Path links (previous, next) look like buttons at the page end; reference links are plain list items. *Wayfinding; visibility of status.*
14. **You are here.** Every quest shows trunk name, "step n of N" or "quest n of N", and highlights the current quest in the sidebar. *Visibility of status; progress indicators; goal gradient (weak).*
15. **Lists over run-in labels.** Where items are looked up (commands, modes, risks), use a list or table whose items start with the key term, not a paragraph with bold run-ins. *First-two-words; F-pattern; chunking; (inference).*
16. **Table cells stay short.** Table cells hold a word, number or phrase of under about 12 words; longer content becomes a list or prose. *NN/g comparison tables; (design) for 12.*
17. **No provenance in the body.** Lesson text contains no "verified on", "as of version", hedging chains, or inline citations. Maintainer notes live in research/. A single "Sources" link per quest is allowed in Going further. *Coherence; extraneous load.*
18. **Direct style.** Steps use the imperative and present tense. A sentence of the form "not X, but Y" needs a stated reason (it corrects a likely wrong belief) or is rewritten. *Coherence; first-two-words; (design).*
19. **Lore budget.** Story text is limited to the hook (3 sentences) and one closing line. No story text inside Steps. *Coherence; gamification evidence mixed.*
20. **Progress without pressure.** Progress shows completed count per trunk; no streaks or timers. Completion is stored locally and the course works without it. *Goal gradient (weak); gamification evidence mixed; (design).*
