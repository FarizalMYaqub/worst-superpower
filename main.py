"""Worst Superpower entry: one useless power, one line, no sequel.

The gate for this bounty reads /output/entry.txt and accepts UTF-8 text
of 1 to 140 characters that is not only white space. This module keeps
the line in one place, proves it fits the gate, lands it on disk without
ever leaving a half-written file behind, then reads it back and refuses
to exit cleanly unless the bytes match what was meant to ship.
"""

import os
import sys
from pathlib import Path

# The joke in three beats. Beat one borrows a marquee hero power: mind
# reading. Beat two shrinks the cast to houseplants. Beat three lets
# every fern on the windowsill deliver the same one-word review.
ENTRY_TEXT = (
    "I can read the minds of houseplants, but every one of them "
    "is only ever thinking 'water.'"
)

GATE_MIN = 1
GATE_MAX = 140


def destination() -> Path:
    """The file the sealed scorer reads.

    The harness mounts /output. OUTPUT_DIR exists so a local dry run can
    aim the same program at a scratch folder and compare runs byte for
    byte without touching the real mount.
    """
    root = os.environ.get("OUTPUT_DIR", "/output")
    return Path(root) / "entry.txt"


def assert_fits_gate(text: str) -> None:
    """Raise before writing anything if the line would score 0."""
    if text.strip() == "":
        raise ValueError("entry is empty or only white space")
    size = len(text)
    if size < GATE_MIN or size > GATE_MAX:
        raise ValueError(f"entry is {size} chars; gate allows 1-140")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable


def land_atomically(target: Path, text: str) -> None:
    """Write beside the target, then swap into place in one rename."""
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.with_name(target.name + ".part")
    staging.write_text(text, encoding="utf-8")
    os.replace(staging, target)


def prove_on_disk(target: Path, expected: str) -> None:
    """Read the landed file back; anything else is a failed run."""
    landed = target.read_text(encoding="utf-8")
    if landed != expected:
        raise RuntimeError("entry.txt on disk does not match ENTRY_TEXT")


def run() -> int:
    assert_fits_gate(ENTRY_TEXT)
    target = destination()
    land_atomically(target, ENTRY_TEXT)
    prove_on_disk(target, ENTRY_TEXT)
    return 0


if __name__ == "__main__":
    sys.exit(run())
