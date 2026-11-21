#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Entry for make.fun competition
`the-passport-page-of-a-countr-2-20261121-0318`.

Reads the bundled artwork ``image.jpg`` (an invented passport spread
for the fictional Republic of Auralia), validates that it is a
well-formed JPEG under 1 MiB, and copies it byte-for-byte to the
output file ``entry.png``.

The self-check is deliberately strict: the file must start with the
JPEG SOI marker, end with the EOI marker, contain a readable Start
Of Frame segment, and stay within the size and dimension limits.
Anything failing that check stops the run with a clear error instead
of writing a corrupt or oversized ``entry.png``.

Pure standard library only. No network access. Deterministic: two
runs produce byte-identical output.

Usage:
    python3 main.py
    MAKEFUN_OUTPUT_DIR=/tmp/passport-out python3 main.py
"""

import os
import struct
import sys

SOURCE = "image.jpg"
MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024

HERE = os.path.dirname(os.path.abspath(__file__))


def _read_jpeg_dimensions(data):
    """Return (width, height) from a JPEG byte string.

    Walks the JPEG marker segments until a Start Of Frame marker is
    found and reads its dimensions. Raises ValueError if the data is
    not a well-formed JPEG.
    """
    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        raise ValueError("missing JPEG SOI marker (FFD8)")
    if data[-2:] != b"\xff\xd9":
        raise ValueError("missing JPEG EOI marker (FFD9)")

    i = 2
    while i + 1 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            if i + 9 > len(data):
                raise ValueError("truncated SOF segment")
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return width, height
        if i + 4 > len(data):
            raise ValueError("truncated JPEG segment")
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        if length < 2:
            raise ValueError("invalid JPEG segment length")
        i += 2 + length
    raise ValueError("no SOF marker found; not a well-formed JPEG")


def validate(source_path):
    """Validate the bundled artwork; return its bytes.

    Refuses (raises ValueError) when the file is missing, not a
    well-formed JPEG, larger than 1 MiB, or larger than 1024x1024.
    """
    with open(source_path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        raise ValueError(
            "image.jpg is %d bytes, over the 1,048,576 byte "
            "(1 MiB) limit for the bundled artwork" % len(data)
        )
    width, height = _read_jpeg_dimensions(data)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            "image.jpg is %dx%d, over the 1024x1024 limit"
            % (width, height)
        )
    return data


def main():
    source_path = os.path.join(HERE, SOURCE)
    try:
        data = validate(source_path)
    except (OSError, ValueError) as exc:
        print("self-check FAILED: %s" % exc, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d bytes, %s)" % (out_path, len(data), SOURCE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
