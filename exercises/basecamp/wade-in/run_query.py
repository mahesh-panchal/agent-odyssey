# Run ONE query file against mock.db, read-only, on your own machine.
# Usage: python run_query.py report-query.sql
import sqlite3, sys
from pathlib import Path

here = Path(__file__).parent
sql = Path(sys.argv[1]).read_text()
con = sqlite3.connect(f"file:{here / 'mock.db'}?mode=ro", uri=True)  # read-only: a write fails
cur = con.execute(sql)
print("\t".join(c[0] for c in cur.description))
for row in cur:
    print("\t".join(str(v) for v in row))
