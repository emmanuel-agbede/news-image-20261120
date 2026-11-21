"""make.fun entry: news-image-20261120.

Sums up the world news of Friday 20 November 2026 in one image: a newspaper
front page whose lead story is the International Court of Justice ruling
that Myanmar committed genocide against the Rohingya, alongside the Russian
barrage on Kyiv, the fallout from the Shenzhen trilateral summit, the Houthi
missile strike on Riyadh's tallest tower, the firing of the US cyber chief
amid nationwide tech outages, Iran's tanker convoy testing the US blockade,
Cyclone Akvan's landfall in Odisha, the EU-UK Brussels summit, the leak of
16,000 card customers' data and GTA 6's record-breaking launch sales.

The front page ships in this repository as entry.png (a JPEG by its first
bytes, which the rules allow under that name). This program copies it,
byte for byte, to entry.png inside the output directory: $MAKEFUN_OUTPUT_DIR
when set, else /output. It reads nothing else and needs no network, so both
grading runs write identical bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


MAX_BYTES = 1_048_576  # the gate's 1 MiB cap on the entry image


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"entry image missing: {SOURCE}", file=sys.stderr)
        return 1
    if os.path.getsize(SOURCE) > MAX_BYTES:
        print("entry image exceeds the 1 MiB gate limit", file=sys.stderr)
        return 1
    dest = output_path()
    shutil.copyfile(SOURCE, dest)
    # Verify the copy landed byte for byte; a short or torn write would
    # silently produce an invalid entry, so fail loudly instead.
    with open(SOURCE, "rb") as f:
        expected = f.read()
    with open(dest, "rb") as f:
        written = f.read()
    if written != expected:
        print("copy verification failed: output differs from source", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(written)} bytes, verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
