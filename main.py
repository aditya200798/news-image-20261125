#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261125 entry.

The poster (entry.png, drawn by draw_poster.py) is the deliverable: this
program copies it byte-for-byte into the output directory and verifies
the copy's SHA-256 against the source, failing loudly on any mismatch.
No network, no inputs — the same bytes come out on every run.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        print("entry.png missing beside main.py", file=sys.stderr)
        return 1
    dest = output_path()
    shutil.copyfile(SOURCE, dest)
    if digest(SOURCE) != digest(dest):
        print("copy verification failed: SHA-256 mismatch", file=sys.stderr)
        return 1
    print("wrote", dest, os.path.getsize(dest), "bytes, sha256 verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
