# Run the cells of a "# %% [n]" file in the order given, in ONE shared namespace
# (like a notebook kernel). Usage: python run_cells.py cells.py 1 2 3 4 3
import re, sys
text = open(sys.argv[1]).read()
cells = {m.group(1): m.group(2) for m in re.finditer(r"# %% \[(\d+)\][^\n]*\n(.*?)(?=# %% \[|\Z)", text, re.S)}
ns = {}
for n in sys.argv[2:]:
    print(f"[cell {n}]")
    exec(cells[n], ns)
