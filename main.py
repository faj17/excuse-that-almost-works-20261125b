"""The excuse a gamer texts the boss to skip work on GTA 6 launch week.

The whole entry is one hurried line: a washing machine has flooded the
kitchen, and the sender is mopping before the water reaches the hallway
carpet. Nothing else is needed here — the script validates the line and
drops it into /output/entry.txt.
"""

from pathlib import Path

# The excuse itself: one line, 98 characters, 17 words.
# The laugh comes from the last clause: the emergency is not work, it is
# the hallway carpet — the sender's priorities are showing.
LINE = (
    "Sorry, my washing machine flooded the kitchen and I'm mopping "
    "before it gets to the hallway carpet"
)

OUTPUT_DIR = Path("/output")
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 140
MAX_WORDS = 20


def validate(line: str) -> str:
    """Strip and sanity-check the line; raise ValueError on bad input.

    Checks run in order of specificity: a blank line gets its own
    error instead of the length error, and control characters are
    rejected so the output is always a clean, printable single line.
    Word count and single-line shape are enforced too: at most 20
    words, no newline or carriage return anywhere, no tabs, and no
    runs of consecutive whitespace — a hurried text is one plain line
    with single spaces between words.
    """
    text = line.strip()
    if not text:
        raise ValueError("line must not be empty or only whitespace")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"line must be {MIN_CHARS}-{MAX_CHARS} chars, got {len(text)}"
        )
    if len(text.split()) > MAX_WORDS:
        raise ValueError(
            f"line must be at most {MAX_WORDS} words, "
            f"got {len(text.split())}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if "\t" in text:
        raise ValueError("line must not contain tabs")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("line must not contain control characters")
    if any(a == " " and b == " " for a, b in zip(text, text[1:])):
        raise ValueError("line must not contain consecutive spaces")
    return text


def main() -> None:
    text = validate(LINE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    # Read back and confirm the file holds exactly the validated line:
    # a stray newline or encoding slip would fail the 1-140 char gate.
    written = OUTPUT_FILE.read_text(encoding="utf-8")
    if written != text:
        raise RuntimeError(
            f"{OUTPUT_FILE} does not match the validated line "
            f"({len(written)} chars written, {len(text)} expected)"
        )
    print(text)
    print(f"Wrote {len(text)} chars, {len(text.split())} words to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
