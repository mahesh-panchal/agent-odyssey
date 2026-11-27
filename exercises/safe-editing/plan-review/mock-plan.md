# Plan: accept a new `strandedness` column in the samplesheet

Task given to the agent: "Our samplesheet gets a new optional column, `strandedness`
(values: forward, reverse, unstranded). Make `parse_samplesheet.py` accept it."

1. Read `bin/parse_samplesheet.py` and `tests/test_parse_samplesheet.py` to see how columns are read.
2. Add `strandedness` to the list of known columns in `parse_samplesheet.py`, defaulting to `unstranded` when the column is absent.
3. Build the parsed result as a dictionary keyed by `sample_id`, since sample IDs are unique, so downstream code can look a sample up directly.
4. Rename the parameter `--input_sheet` to `--samplesheet` in `conf/base.config` so it matches the new parser option name.
5. Update the alignment and counting modules, the documentation and the test suite so the whole pipeline uses `strandedness` end to end.
6. Tell the user the parser now handles the new column.
