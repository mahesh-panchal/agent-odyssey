# fasta-tools

A tiny teaching plugin from the Agent Odyssey Forge. It contains one skill, `check-fasta`, which counts the records in a FASTA file and lists duplicated header lines, then reports the exact commands it ran. It changes no files. Load it for a session with `claude --plugin-dir .` and ask for a new FASTA file to be checked. It needs no setup and no network access.
