import subprocess, sys
from pathlib import Path
here = Path(__file__).parent
for script in ("build_banks.py", "make_art.py"):
    subprocess.run([sys.executable, str(here / script)], check=True)
