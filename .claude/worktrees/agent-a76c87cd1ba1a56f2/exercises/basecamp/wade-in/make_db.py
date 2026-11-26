# Build a MOCK project database (all rows invented) and write the schema-only text
# you would paste into a chat window. Stdlib only. Usage: python make_db.py
import sqlite3, random
from pathlib import Path

here = Path(__file__).parent
db = here / "mock.db"
db.unlink(missing_ok=True)
con = sqlite3.connect(db)
con.executescript("""
CREATE TABLE projects (
  id INTEGER PRIMARY KEY,
  name TEXT,
  lead TEXT,
  status TEXT            -- active, paused, closed
);
CREATE TABLE samples (
  id INTEGER PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id),
  participant_code TEXT, -- pseudonymised code, still personal data in real life
  received_date TEXT,    -- YYYY-MM-DD
  notes TEXT             -- free text, may hold anything
);
CREATE TABLE milestones (
  id INTEGER PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id),
  title TEXT,
  due_date TEXT,         -- YYYY-MM-DD
  done INTEGER           -- 0 or 1
);
""")
random.seed(7)
names = [("Heron", "A. Lind", "active"), ("Kelp", "B. Roos", "active"), ("Vega", "C. Holm", "paused")]
for i, (n, lead, st) in enumerate(names, 1):
    con.execute("INSERT INTO projects VALUES (?,?,?,?)", (i, n, lead, st))
    for m in range(1, 4):
        con.execute("INSERT INTO milestones VALUES (NULL,?,?,?,?)",
                    (i, f"Milestone {m}", f"2026-{3*m:02d}-28", 1 if m == 1 else 0))
    for s in range(1, 9 + 3 * i):
        con.execute("INSERT INTO samples VALUES (NULL,?,?,?,?)",
                    (i, f"P{i}{s:03d}", f"2026-{random.randint(1, 9):02d}-{random.randint(1, 28):02d}", "invented"))
con.commit()
schema = "\n".join(r[0] + ";" for r in con.execute("SELECT sql FROM sqlite_master WHERE type='table'"))
con.close()
(here / "schema-only.txt").write_text(schema + "\n")
print("wrote mock.db (invented rows) and schema-only.txt (table and column names, no rows)")
