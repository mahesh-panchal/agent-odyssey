# Mock notebook in py:percent style. Cells run in the order you give run_cells.py.
# %% [1] load
reads = [12, 35, 41, 28, 50]

# %% [2] cutoff
threshold = 30

# %% [3] filter and report
kept = [r for r in reads if r >= threshold]
print("reads kept:", len(kept))

# %% [4] tried a stricter cutoff later
threshold = 40
