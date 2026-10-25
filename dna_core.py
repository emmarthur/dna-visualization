"""
DNA scrolling animation — shared logic for reference script and FastAPI web app.

How the demo fits together:
  1. reference/dna.py  — original terminal program (print + sleep loop).
  2. dna_core.py       — same rules extracted here so the web server does not duplicate logic.
  3. web/main.py       — calls next_row() repeatedly and sends each line to the browser.

A reader can trace: browser EventSource → GET /stream → next_row() → ROWS templates.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

# Seconds to wait after each row that shows base pairs (A/T, C/G).
# Spacer rows (indexes 0 and 9) do not pause — see next_row().
PAUSE = 0.15

# ASCII art templates for one "cycle" of the helix. Leading spaces center the ladder.
# Rows with {} get two nucleotide letters via str.format(left, right).
# Index 0 and 9 are fixed "##" rungs with no placeholders.
ROWS = [
    "         ##",
    "        #{}-{}#",
    "       #{}---{}#",
    "      #{}-----{}#",
    "     #{}------{}#",
    "    #{}------{}#",
    "    #{}-----{}#",
    "     #{}---{}#",
    "     #{}-{}#",
    "      ##",
    "     #{}-{}#",
    "     #{}---{}#",
    "    #{}-----{}#",
    "    #{}------{}#",
    "     #{}------{}#",
    "      #{}-----{}#",
    "       #{}---{}#",
    "        #{}-{}#",
]


@dataclass
class DnaAnimationState:
    """
    Tracks where we are in the ROWS cycle.

    row_index is the index used on the *last* step (0 before the first next_row call).
    The reference script uses the same wrap pattern: increment first, then wrap at len(ROWS).
    """

    row_index: int = 0


def _random_pair() -> tuple[str, str]:
    """
    Pick a complementary DNA base pair for the left and right sides of the helix.

    Biology: A pairs with T, C pairs with G. The animation randomizes orientation
    (A-T vs T-A) for visual variety, matching reference/dna.py randomSelection 1–4.
    """
    selection = random.randint(1, 4)
    if selection == 1:
        return "A", "T"
    if selection == 2:
        return "T", "A"
    if selection == 3:
        return "C", "G"
    return "G", "C"


def next_row(state: DnaAnimationState) -> tuple[str, DnaAnimationState, bool]:
    """
    Advance the animation by one printed line.

    Returns:
        line:         The exact string to show (one row of the helix).
        new_state:    Updated index for the next call.
        should_pause: True if the caller should sleep PAUSE seconds before the next row.
                      False for spacer rows 0 and 9 (reference script uses continue without sleep).

    Call this in a loop from the terminal script or from the FastAPI SSE generator.
    """
    # Move to the next template row, wrapping back to 0 after the last row.
    row_index = state.row_index + 1
    if row_index == len(ROWS):
        row_index = 0

    new_state = DnaAnimationState(row_index=row_index)

    # Spacer rungs: print as-is, no nucleotides, no pause afterward.
    if row_index == 0 or row_index == 9:
        return ROWS[row_index], new_state, False

    left, right = _random_pair()
    return ROWS[row_index].format(left, right), new_state, True
