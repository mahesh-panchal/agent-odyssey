# Apple Foundation Models (on-device model)

Checked 2026-11-20. Official Apple docs only. The HTML pages are JS shells, so the content came from the JSON behind them via a summarising fetch tool (quotes as returned, short).
Pages:
- https://developer.apple.com/documentation/foundationmodels/generating-content-and-performing-tasks-with-foundation-models#Understand-model-capabilities
- https://developer.apple.com/documentation/updates/foundationmodels
Decision fed: a capabilities-of-a-bare-model reminder in Script, Model, or LLM; a short "built-in Pet" note in Adopt the Pet.

## CONFIRMED (capabilities page)
- Intro: "it helps to know what the on-device language model can do."
- Suits: summarise; extract entities; understand text; refine or edit text; classify or judge text; compose creative writing; generate tags from text; generate game dialog.
- "May not be suitable": basic math (example: counting b's in "bagel"); create code; logical reasoning.
- Complex tasks become possible with guided generation or tool calling (page links to both).
- Availability depends on whether the device and region support Apple Intelligence; the model can take time to download after Apple Intelligence is turned on.

## CONFIRMED (updates page)
- June 2026: the model changes when a person updates to iOS, iPadOS, macOS and visionOS 27; test prompts again. Also a `PrivateCloudComputeLanguageModel` class and Vision tools for image prompts.
- March 2026: a Python SDK for the on-device model (`python-apple-fm-sdk`).
- February 2026: model change at 26.4; `contextSize` property (4,096-token window); `#Playground` macro in Xcode.

## UNCONFIRMED
- Which OS version first shipped the framework: neither page says. The user suspected 27 or later; the pages show updates at 26.4 and 27, so it existed before 27. Not stated on the pages, so the site does not claim a first version.
- Whether any coding-agent harness (OpenCode, Claude Code) can use the model as a backend: not covered by the pages.
- The capabilities table is for the small on-device model; it should not be read as limits of larger hosted models.
