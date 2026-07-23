from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from student_portal_demo.__main__ import main


if __name__ == "__main__":
    raise SystemExit(main())

