# Restricted topics: safeguards that limit model help on biology and security

Checked 2026-11-28. Pages fetched through a summarising fetch tool (quotes as returned, short). Paraphrase on the site.

## Biology (Anthropic)
- CONFIRMED: when its biology classifiers fire, the request is re-routed to a less capable model. Source: https://www.anthropic.com/news/improving-fable-5-s-biology-safeguards (published Aug 7, 2026): "when a classifier fires, the model re-routes the user's request to Opus 5, a capable model that does not have the same level of biological capability as Fable 5".
- CONFIRMED: Anthropic says the launch design "would result in a high number of false positives", that an update cut biology-related fallbacks "by about 85% across our product surfaces", and that "There will inevitably remain false positives". The model "will continue to block dual-use professional biology and drug development queries" (virology, toxicology and molecular design named). It speaks of "trusted access pathways for frontier biology capabilities" without describing one.
- CONFIRMED: the API filters for Sonnet 4.5 are "narrowly focused on preventing assistance with CBRN weapons-related tasks" and "not intended to block general scientific discussion, educational content, or commonly available information". "False positives can occur." Biology-related content is listed among patterns that may trigger them. Vetted users can ask API support for exemptions. Source: https://support.claude.com/en/articles/12449294 (Sonnet 4.5 API filters, dated March 16, 2026).
- CONFIRMED: Constitutional Classifiers++ target jailbreaks, "in particular relating to the production of chemical, biological, radiological, or nuclear weapons (CBRN)", with a refusal rate on harmless queries of 0.05% over one month of Sonnet 4.5 traffic. Source: https://www.anthropic.com/research/next-generation-constitutional-classifiers (Jan 9, 2026).

## Security (Anthropic)
- CONFIRMED: usage policy effective Nov 12, 2026 prohibits finding or exploiting vulnerabilities "without authorization of the system owner", creating malware, and building persistent unauthorised remote access tools. It does not prohibit "security research, testing, or tool development conducted on systems you own or operate, with the authorization of the system owner". "Our products also include real-time safeguards that may block or limit certain outputs, but encountering a block does not by itself indicate a violation of the Usage Policy." It also prohibits bypassing guardrails (for example jailbreaking) without prior authorisation. Source: https://www.anthropic.com/legal/aup
- CONFIRMED: the Cyber Verification Program "lets verified security professionals use our most capable models for advanced security work with fewer interruptions from our cyber safeguards". Individuals can apply for Defense Access (security operations, malware analysis, vulnerability triage); Red Team and Specialized Access are for organisations. Everyday secure development, such as reviewing code, needs no programme. It states "You may experience some model refusals and classifier blocks for allowed security work", and that it adjusts only the cyber safeguards. Source: https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet (page served is titled "Cyber Verification Program").

## General over-refusal
- CONFIRMED: https://arxiv.org/abs/2405.20947 (OR-Bench, ICML 2025) reports a trade-off: most of the 32 models tested achieve safety at the cost of over-refusal, rejecting benign prompts that look harmful. Its test set is 80,000 seemingly toxic prompts.

## Machine-learning research
- NOT FOUND: no provider page read (Anthropic usage policy, Responsible Scaling Policy HTML) says a model is trained or filtered to be less helpful on AI or machine-learning research tasks. The Responsible Scaling Policy discusses AI R&D capability thresholds for the provider's own risk assessment. Do not claim a restriction on ML research in lesson text. OpenAI and Google pages were not read.

## Not verified
- The content of Anthropic's "Life Sciences Verification Program" page (title seen as a related link, not fetched).
- Behaviour of OpenAI or Google models and policies.
