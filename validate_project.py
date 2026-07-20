"""Repository validation command with a CI-friendly exit code."""

from __future__ import annotations

import json
import sys

from src.project_validation import validate_project


def main() -> int:
    """Run all project checks and return zero only when every check passes."""
    result = validate_project()
    print(
        json.dumps(
            {
                "status": result["status"],
                "checks_passed": result["checks_passed"],
                "checks_total": result["checks_total"],
            }
        )
    )
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
