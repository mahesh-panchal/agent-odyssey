# Wade In: chat windows, uploads and how much to hand over

Date read 2026-11-23. Official Anthropic pages only, read by a subagent through a fetch tool that summarises, so quotes are as returned and the wording should be re-checked on the live page before anyone relies on it.
Question: for a non-agent route (a chat window, with or without uploads), what do the docs say about training use, retention and review, so the quest "Wade In" can say what leaves the machine at each rung. Feeds: zones/basecamp/wade-in.qmd. Complements `research/privacy-and-unpublished-work.md`, which covers Claude Code only.

Page prefixes: P = https://privacy.claude.com/en/articles/ , S = https://support.claude.com/en/articles/

## Training use
- CONFIRMED, consumer (Free, Pro, Max): a user setting. P10023580-is-my-data-used-for-model-training (updated 2026-03-16): "We will use your chats and coding sessions (including to improve our models) if: You choose to allow us to use your chats and coding sessions to improve Claude". The page states no default. Opt-in wording suggests off until enabled: that is our inference, not stated.
- CONFIRMED, commercial: P7996868-is-my-data-used-for-model-training (updated 2026-08-18): "we will not use your inputs or outputs from our commercial products". Names Claude for Work, the API and Claude Gov. Exceptions: feedback or bug reports, or an explicit opt-in.
- NOT FOUND: any statement about uploaded files separate from chats.

## Retention
- CONFIRMED, consumer, training on: P10023548-how-long-do-you-store-my-data (updated 2026-07-01): "in a de-identified format for up to 5 years".
- NOT FOUND: a number for consumer, training off. The page says only "for as long as reasonably necessary".
- CONFIRMED, after the user deletes a chat: "Deleted from our back-end storage systems within 30 days".
- CONFIRMED, commercial: P7996866-how-long-do-you-store-my-organization-s-data (updated 2026-07-01): "we automatically delete inputs and outputs on our backend within 30 days of receipt or generation". The 30-day default does not apply to services with longer retention, such as the Files API (an API feature, not the chat window).
- Policy-violation flags: the page says inputs and outputs flagged for a Usage Policy violation may be kept up to 2 years and classification scores up to 7 years. Feedback (thumbs) is kept 5 years.
- NOT FOUND: whether files uploaded in claude.ai chat are kept differently from typed prompts.

## Incognito chats
- CONFIRMED: S12260368-use-incognito-chats: "Incognito chats are not used for training." Not saved to history or memory. Kept 30 days by default, or longer under an Enterprise organisation's custom retention setting. P7996866 says incognito chats are deleted within 30 days unless flagged as a Usage Policy violation.
- Not verified: whether Team or Enterprise exports include them.

## Human review
- CONFIRMED, consumer: P10458704-how-does-anthropic-protect-the-personal-data-of-claude-users (updated 2026-03-16): "By default, Anthropic employees cannot access your conversations unless: You explicitly consent to share your data with us as a part of giving us feedback", and "only designated members of our Trust & Safety team may access this data on a need-to-know basis."
- NOT FOUND: commercial-specific human review, and review of uploaded files.

## Organisation agreement and admin settings
- CONFIRMED: P9267385-does-anthropic-act-as-a-data-processor-or-controller: "the customer is the "Controller"... Anthropic acts as a "Processor"", under the Commercial Terms. The word "DPA" was NOT FOUND on that page.
- Partly confirmed: Enterprise plans can set custom data retention (named on S12260368). The detail page was not fetched. Do not state a period.

## What the quest may say (and may not)
- May say: consumer accounts have a training setting; organisation (commercial) accounts are documented as not trained on; consumer retention up to 5 years with training on, 30 days after you delete; commercial default 30 days; ask your organisation which account and agreement apply.
- May NOT say: that uploads are treated differently from prompts (not found); a retention number for consumer with training off (not found); that incognito is safe for regulated data (kept up to 30 days, may be flagged); anything about other vendors' chat tools.
- Our own reasoning (General practice, no source): anything you type, paste or upload is sent to the provider; reading a file with an agent sends it the same way; a query you run yourself sends nothing but the query's text.

## Other sources used in the quest
- https://code.claude.com/docs/en/data-usage and https://docs.ollama.com/faq : see `research/privacy-and-unpublished-work.md` (read 2026-11-17).
- https://aiforscience.eu/short-version/ : see `research/aiforscience.md`.

## Full URLs (all returned HTTP 200 on 2026-11-23)
- https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training (consumer training)
- https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data (consumer retention)
- https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data (commercial retention)
- https://support.claude.com/en/articles/12260368-use-incognito-chats (incognito)
- 2026-11-26 fact-check (Wade In): commercial retention reworded per privacy.claude.com 7996866 and code.claude.com/docs/en/data-usage (API 30 days; Team/Enterprise keep saved chats until deleted). Sycophancy paper venue ICLR 2024 not stated on the arXiv page; kept from general knowledge, re-check.
- 2026-11-26: sycophancy paper (arXiv 2310.13548) venue CONFIRMED as ICLR 2024 by https://iclr.cc/virtual/2024/poster/17593 and the ICLR proceedings entry https://proceedings.iclr.cc/paper_files/paper/2024/hash/0105f7972202c1d4fb817da9f21a9663-Abstract-Conference.html (search result summaries, pages not opened by us). arXiv v1 abstract says 'negligible', later versions 'non-negligible' for preferred-over-correct; the course quotes neither.

2026-11-26: the mock database exercise (make_db.py, run_query.py, SQL files, 22 versus 11 join check) was removed. Wade In now has four persona scenes and a decision exercise (pick the step, what leaves, one check). The retention and privacy facts above are unchanged.
