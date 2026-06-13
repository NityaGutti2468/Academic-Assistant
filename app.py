from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from backend.app import app  # noqa: E402,F401


if __name__ == "__main__":
    app.run(debug=True)
