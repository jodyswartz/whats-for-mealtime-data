import json
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_KEYS = {"date", "name", "amount"}

def fail(msg: str) -> None:
    print(f"❌ VALIDATION FAILED: {msg}")
    sys.exit(1)

def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: validate_rawdata.py <path-to-json>")

    p = Path(sys.argv[1])
    if not p.exists():
        fail(f"File not found: {p}")

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"Invalid JSON: {e}")

    if not isinstance(data, list) or not data:
        fail("Top-level JSON must be a non-empty list")

    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            fail(f"Entry {i} is not an object/dict")

        missing = REQUIRED_KEYS - set(entry.keys())
        if missing:
            fail(f"Entry {i} missing keys: {sorted(missing)}")

        date = entry["date"]
        name = entry["name"]
        amount = entry["amount"]

        if not isinstance(date, str) or not DATE_RE.match(date):
            fail(f"Entry {i} invalid date '{date}' (expected YYYY-MM-DD)")

        if not isinstance(name, str) or not name.strip():
            fail(f"Entry {i} invalid name '{name}'")

        try:
            int(amount)
        except Exception:
            fail(f"Entry {i} amount is not int-like: '{amount}'")

    print(f"✅ VALIDATION OK: {p} ({len(data)} entries)")

if __name__ == "__main__":
    main()
