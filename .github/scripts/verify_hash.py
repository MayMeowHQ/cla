import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

EXPECTED_HASH = os.getenv("EXPECTED_HASH", "").lower()
PR_USERNAME = os.getenv("PR_USERNAME", "")
BASE_REF = os.getenv("BASE_REF", "")

if not EXPECTED_HASH or not PR_USERNAME or not BASE_REF:
    print("Missing EXPECTED_HASH, PR_USERNAME, or BASE_REF environment variable.")
    sys.exit(1)


def parse_json_payload(payload: str) -> list[str]:
    if not payload.strip():
        return []
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON content: {exc}") from exc
    contributors = data.get("contributors", [])
    if not isinstance(contributors, list):
        raise ValueError("The 'contributors' key must contain a list.")
    return [str(value).strip().lower() for value in contributors if str(value).strip()]


def parse_text_payload(payload: str) -> list[str]:
    if not payload.strip():
        return []
    return [line.strip().lower() for line in payload.splitlines() if line.strip()]


def read_worktree_file(path: Path, parser) -> list[str]:
    if not path.exists():
        return []
    return parser(path.read_text(encoding="utf-8"))


def read_base_file(relative_path: str, parser) -> list[str]:
    try:
        raw = subprocess.check_output(
            ["git", "show", f"origin/{BASE_REF}:{relative_path}"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return []
    return parser(raw)


def collect_new_entries(filename: str, parser) -> list[str]:
    worktree_values = [value for value in read_worktree_file(Path(filename), parser) if value]
    base_values = [value for value in read_base_file(filename, parser) if value]
    counter = Counter(worktree_values)
    counter.subtract(Counter(base_values))
    additions: list[str] = []
    for value, diff in counter.items():
        if diff > 0:
            additions.extend([value] * diff)
    return additions


def validate_hash_entries(entries: list[str]) -> None:
    invalid = [value for value in entries if value != EXPECTED_HASH]
    if invalid:
        formatted = "\n".join(invalid)
        message = (
            "Found hash entries that do not match the expected SHA-256 hash for user "
            f"'{PR_USERNAME}'.\n"
            f"Expected: {EXPECTED_HASH}\n"
            f"Found: \n{formatted}"
        )
        print(message)
        sys.exit(1)


if __name__ == "__main__":
    pairs = [
        ("contributors.json", parse_json_payload),
        ("contributors.txt", parse_text_payload),
    ]

    new_entries: list[str] = []
    for filename, parser in pairs:
        new_entries.extend(collect_new_entries(filename, parser))

    if not new_entries:
        print("No new contributor hashes detected; skipping CLA hash validation.")
        sys.exit(0)

    validate_hash_entries(new_entries)
    print(
        "Contributor hashes match the SHA-256 hash of GitHub user "
        f"'{PR_USERNAME}'. Validation passed."
    )
