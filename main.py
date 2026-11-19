#!/usr/bin/env python3
"""
Entry point for the make.fun bounty "Sum up 19 November's world news in
one image" (news-image-20261119). Standard library only, no network.

The picture itself - entry.png, drawn by build_image.py in this
repository - sits beside this file. This program checks that the file
is a whole PNG inside the contest limits (at most 1 MiB, at most
1024 by 1024 pixels, every chunk's CRC intact) and then writes it,
byte for byte, to /output/entry.png (or to $MAKEFUN_OUTPUT_DIR when
that is set, as the kit's starter does outside the grader's container).

It runs the same way every time, so two runs write the same bytes.
"""

import os
import struct
import sys
import zlib
from pathlib import Path

MAX_BYTES = 1_048_576  # 1 MiB
MAX_SIDE = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_png(data: bytes) -> tuple[int, int]:
    """Return (width, height) of a whole PNG, or raise ValueError."""
    if len(data) > MAX_BYTES:
        raise ValueError(f"image is {len(data)} bytes, over the 1 MiB limit")
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png does not start with the PNG signature")
    pos = len(PNG_SIGNATURE)
    width = height = None
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        kind = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        (crc_stored,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])
        if zlib.crc32(kind + chunk) & 0xFFFFFFFF != crc_stored:
            raise ValueError(f"CRC mismatch in chunk {kind!r}")
        if kind == b"IHDR":
            width, height = struct.unpack(">II", chunk[:8])
        pos += 12 + length
        if kind == b"IEND":
            break
    if width is None:
        raise ValueError("no IHDR chunk found")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"image is {width}x{height}, over the 1024x1024 limit")
    return width, height


def find_image() -> Path:
    """The image sits beside this file; fall back to the working directory."""
    beside = Path(__file__).resolve().with_name("entry.png")
    if beside.exists():
        return beside
    return Path.cwd() / "entry.png"


def main() -> int:
    source = find_image()
    data = source.read_bytes()
    width, height = check_png(data)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    print(f"wrote {target} ({len(data)} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
