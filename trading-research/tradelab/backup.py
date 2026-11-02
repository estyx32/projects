"""Consistent SQLite backups with a checksum manifest."""

from __future__ import annotations

import hashlib
import sqlite3
from datetime import UTC, datetime
from pathlib import Path


def backup(db_path: str | Path, out_dir: str | Path = "backups") -> Path:
    """Copy the database using SQLite's online backup API, then record a sha256."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    dest = out_dir / f"research-{stamp}.db"

    src = sqlite3.connect(str(db_path))
    dst = sqlite3.connect(str(dest))
    with dst:
        src.backup(dst)
    src.close()
    dst.close()

    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    with open(out_dir / "MANIFEST.txt", "a") as fh:
        fh.write(f"{digest}  {dest.name}\n")
    return dest


def verify(backup_path: str | Path, manifest: str | Path) -> bool:
    backup_path = Path(backup_path)
    digest = hashlib.sha256(backup_path.read_bytes()).hexdigest()
    for line in Path(manifest).read_text().splitlines():
        h, _, name = line.partition("  ")
        if name == backup_path.name:
            return h == digest
    return False
