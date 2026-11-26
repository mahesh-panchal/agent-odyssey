# Factory zone: workflow-manager facts (Snakemake, Nextflow)

Read 2026-11-13. Official docs only. Snakemake: "Snakemake 9.27.1 documentation" (readthedocs /en/stable/).
Nextflow: nextflow.io/docs/latest/* redirects (302) to docs.seqera.io/nextflow/*; pages show no version number, only "Copyright 2026 Seqera".
Decision fed: accuracy of quest text about dry runs, stubs, resume, local runs, pinning.
Method note: pages fetched via a summarising fetch tool, not raw HTML; quotes below are as returned.

## 1. Snakemake dry run and lint
- CONFIRMED: `--dry-run, --dryrun, -n`: "Do not execute anything, and display what would be done." https://snakemake.readthedocs.io/en/stable/executing/cli.html
- CONFIRMED: `-p` additionally prints the shell commands; tutorial: dry run "will only show the execution plan instead of actually performing the steps." https://snakemake.readthedocs.io/en/stable/tutorial/basics.html
- CONFIRMED: `--lint`: "Perform linting on the given workflow ... print snakemake specific suggestions to improve code quality." (cli URL above)
- UNCONFIRMED: what a dry run does NOT check (that shell commands/tools work, that env/containers resolve, that outputs get produced). Docs read do not state it. Inference only: it executes nothing, so it cannot test commands. Do not teach as doc fact.
- UNCONFIRMED: whether dry run validates input file existence beyond DAG building (not stated).

## 2. Nextflow stub, resume, lint
- CONFIRMED: flag is `-stub-run`, alias `-stub`: "Run the workflow, replacing process scripts with command stubs." https://docs.seqera.io/nextflow/reference/cli/run
- CONFIRMED: `stub:` block "can be defined before or after the script section". https://docs.seqera.io/nextflow/process
- CONFIRMED: a stub block is NOT required: with `-stub-run` and no `stub` defined, the process `script` runs instead (same page). Teach "give every process a stub", not "stub is mandatory".
- CONFIRMED: stub-run status is part of the task hash, so stub results do not satisfy a real run. https://docs.seqera.io/nextflow/cache-and-resume
- CONFIRMED: `-resume`: "Run the script using cached results. Use this to continue a run that stopped because of an error." (run URL above)
- CONFIRMED: per-task hash inputs: session ID, task name, container image, modules, Conda/Spack env, CPU arch, task inputs, eval commands (25.10+), script, referenced globals, referenced `ext` properties, bundled scripts, stub-run flag. (cache-and-resume URL)
- CONFIRMED: task resumes only if hash matches AND outputs remain in work dir; else re-executed. Cache invalidated by changed inputs, different session ID, renamed process/calling workflow, changed container/Conda env, changed script.
- CONFIRMED: input file hash = full path + last-modified timestamp + size; `'lenient'` cache mode ignores timestamps (helps on NFS). A process that modifies its own inputs cannot be resumed.
- CONFIRMED (doc inconsistency): Tips section says "Nextflow resumes from the previous run by default" while the body says `-resume` is required. Treat `-resume` as required; flag the page for the programmer.
- CONFIRMED: `nextflow lint` exists: "parses and analyzes the given Nextflow scripts and config files", usage `nextflow lint [options] [paths]`, scans directories recursively. https://docs.seqera.io/nextflow/reference/cli/lint ; command table https://docs.seqera.io/nextflow/reference/cli

## 3. Laptop / no scheduler
- CONFIRMED (Nextflow): default executor is `local`: "runs tasks as processes on the machine where you launch Nextflow"; suited to "development and for small pipelines". https://docs.seqera.io/nextflow/executor
- CONFIRMED (Snakemake): tutorial runs locally with `snakemake --cores 1 <target>`; cores must always be given; `--cores`: "Use at most N CPU cores/jobs in parallel." https://snakemake.readthedocs.io/en/stable/tutorial/basics.html , cli URL above. The tutorial does not use the word "local"; no scheduler is involved in the example.
- CONFIRMED (Snakemake): `--local-cores` only matters "in cluster/cloud mode".

## 4. Reproducibility guidance (pinning)
- CONFIRMED (Snakemake): per-rule `conda` env files "highly encouraged"; per-rule container allowed ("for each rule, a (Docker) container"). https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html
- CONFIRMED (Snakemake): freezing: platform pin file (e.g. linux-64) next to env file is tried first, falling back to the regular file; gives "exactly the same environments down to the individual package builds"; generate via `snakedeploy pin-conda-envs`; update pins when env file changes. Referencing a pre-existing named env "can hamper reproducibility". Same page.
- CONFIRMED (Snakemake): `--use-conda`: without it "the conda directive is ignored". cli URL.
- CONFIRMED (Snakemake): `--containerize` generates a Dockerfile/Apptainer def from per-rule conda envs (deployment URL).
- CONFIRMED (Nextflow conda): pin by name in spec, e.g. `bwa=0.7.15`; lock files list every package and dependency, "more reproducible", optional MD5. https://docs.seqera.io/nextflow/conda
- CONFIRMED (Nextflow container): "Containerizing a pipeline makes it self-contained and reproducible."; `container` settable per process or in config; `nextflow inspect` previews containers per process. https://docs.seqera.io/nextflow/container
- UNCONFIRMED: any official Nextflow statement to pin container tags/digests (container page gives none; its example `biocontainers/samtools` has no tag). Do not claim one.
- Not recorded on purpose: specific image URIs/tags/versions; look them up at the registry when needed.

## Tested
Nothing executed; docs only.

- RUN 2026-11-26: the Read the Rails rule parses in Snakemake 9.27.2 (temporary `pixi exec`, nothing installed); `snakemake -n` fails with MissingInputException for the hard-coded /home/alice path, as the page describes.
