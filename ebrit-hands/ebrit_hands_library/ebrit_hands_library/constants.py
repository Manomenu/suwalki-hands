from pathlib import Path

# __file__ = ebrit_hands_library/ebrit_hands_library/constants.py
# .parent.parent.parent = solution root (contains all sub-projects)
SOLUTION_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = SOLUTION_ROOT / "logs"
ARTIFACTS = SOLUTION_ROOT / "artifacts"
