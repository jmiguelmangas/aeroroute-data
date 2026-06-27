"""Curated global airport selection for the AeroRoute MVP."""

from __future__ import annotations

import csv
from pathlib import Path

MVP_AIRPORT_IDENTS = (
    "CYYZ",
    "CYVR",
    "EDDF",
    "EGLL",
    "EHAM",
    "EIDW",
    "EKCH",
    "ENGM",
    "ESSA",
    "FACT",
    "HECA",
    "KJFK",
    "KLAX",
    "KMIA",
    "KORD",
    "LEBL",
    "LEMD",
    "LFPG",
    "LGAV",
    "LIRF",
    "LOWW",
    "LPPT",
    "LSZH",
    "NZAA",
    "OMDB",
    "OTHH",
    "RJTT",
    "RKSI",
    "SAEZ",
    "SBGR",
    "VABB",
    "VIDP",
    "VHHH",
    "WSSS",
    "YSSY",
)


def write_mvp_airports_csv(source: Path, destination: Path) -> int:
    with source.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("airport source has no CSV header")
        selected = {
            row["ident"]: row
            for row in reader
            if row.get("ident") in MVP_AIRPORT_IDENTS
        }
    missing = sorted(set(MVP_AIRPORT_IDENTS) - selected.keys())
    if missing:
        raise ValueError(f"MVP airport source is missing: {', '.join(missing)}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(selected[ident] for ident in MVP_AIRPORT_IDENTS)
    return len(selected)
