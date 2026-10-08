"""Development convenience entrypoint: python run.py.

Install dependencies first with: python -m pip install -e .
"""

from pathlib import Path
import sys

# Running directly from the Git checkout is supported even without editable install.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from openscore.application import main

if __name__ == "__main__":
    raise SystemExit(main())
