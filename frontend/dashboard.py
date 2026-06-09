from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app import app  # noqa: E402


if __name__ == "__main__":
    print("Starting Flask dashboard at http://127.0.0.1:5000/dashboard")
    app.run(debug=True)
