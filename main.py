#!/usr/bin/env python3
"""Entrypoint for the news-image-20261125 V1 repo (stdlib only).

The front page is pre-rendered as entry.png (1024x1024 RGB, <= 1 MiB).
This script only copies it to MAKEFUN_OUTPUT_DIR and verifies it:
size cap, PNG magic bytes, and sha256 against the pinned digest.
Deterministic: two runs write byte-identical output.
"""
import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576
# Pinned after the render — sha256sum entry.png (175117 bytes, 1024x1024 RGB)
EXPECTED_SHA256 = "32a027cdaccd6a252e7e4cc01e2477fc41e5e98795516aea7343a2e236cc9c3a"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png too large: {len(data)} bytes")
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("entry.png is not a PNG file")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"entry.png sha256 mismatch: {digest}")
    dest = out_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    if dest.read_bytes() != data:
        raise SystemExit("written copy differs from source")
    print(f"wrote {dest} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
