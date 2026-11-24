#!/usr/bin/env python3
"""One Emoji, One Smile -- make.fun bounty entry.

Prints exactly one emoji, and nothing else, to stdout: no words, no
caption, no explanation, no trailing newline. The bounty is judged in
blind pairwise rounds where a judge model is shown two emojis at a time
and picks the warmer of the pair, so the program picks its emoji by
scoring a shortlist of warm candidates on the traits that read as
warmth -- a genuine smile, visible affection, an open embrace, and
sunshine -- and prints the highest scorer.

Pure Python 3 standard library only. No input, no network, no clock,
no randomness: two runs print byte-identical output.
"""

import sys
import unicodedata

# (emoji, smile, affection, embrace, sunshine)
# Why the winner wins: a judge shown two emojis picks the warmer one,
# and warmth here is a face that is visibly smiling *and* visibly
# affectionate. The hugging face offers an embrace but no hearts; heart
# hands offer affection but no smiling face; the sunflower and the sun
# offer sunshine but no smile at all. Only the smiling face with hearts
# carries both a smile and hearts, so it scores highest on every
# weighting that puts smile and affection first.
CANDIDATES = [
    ("\U0001F970", 3, 3, 0, 0),  # smiling face with hearts
    ("\U0001F917", 2, 0, 3, 0),  # hugging face
    ("\U0001FAF6", 0, 3, 0, 0),  # heart hands
    ("\U0001F60A", 3, 0, 0, 0),  # smiling face with smiling eyes
    ("\U0001F33B", 0, 0, 0, 2),  # sunflower
    ("\U00002600", 0, 0, 0, 2),  # sun
]

WEIGHTS = (3, 3, 2, 1)


def warmth(candidate):
    """Warmth score of one candidate: weighted sum of its traits."""
    _, smile, affection, embrace, sunshine = candidate
    return (
        WEIGHTS[0] * smile
        + WEIGHTS[1] * affection
        + WEIGHTS[2] * embrace
        + WEIGHTS[3] * sunshine
    )


def pick():
    """Return the warmest candidate; first maximum wins a tie."""
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        score = warmth(candidate)
        if score > best_score:
            best, best_score = candidate, score
    return best[0]


def main():
    emoji = pick()
    # Guard the bounty rule before anything reaches stdout: the entry
    # must be exactly one emoji, a single non-ASCII symbol character.
    # U+1F970 is one code point in the Symbol, other (So) category.
    if (
        len(emoji) != 1
        or emoji.isascii()
        or unicodedata.category(emoji) != "So"
    ):
        raise SystemExit("entry is not exactly one emoji")
    sys.stdout.write(emoji)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
