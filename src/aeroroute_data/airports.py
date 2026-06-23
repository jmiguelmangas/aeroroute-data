"""Deterministic validation for locally supplied OurAirports CSV files."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AirportRecord:
    ident: str
    airport_type: str
    name: str
    latitude_deg: float
    longitude_deg: float
    elevation_ft: int | None
    iso_country: str | None
    municipality: str | None
    iata_code: str | None


@dataclass(frozen=True, slots=True)
class ValidationSummary:
    accepted: tuple[AirportRecord, ...]
    rejected_rows: int
    sha256: str


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_airports_csv(path: Path) -> ValidationSummary:
    accepted: list[AirportRecord] = []
    rejected_rows = 0
    with path.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            try:
                latitude = float(row["latitude_deg"])
                longitude = float(row["longitude_deg"])
                if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                    raise ValueError("coordinate outside WGS84 bounds")
                ident = row["ident"].strip()
                name = row["name"].strip()
                if not ident or not name:
                    raise ValueError("airport identity is required")
                elevation = row.get("elevation_ft", "").strip()
                accepted.append(
                    AirportRecord(
                        ident=ident,
                        airport_type=row.get("type", "").strip(),
                        name=name,
                        latitude_deg=latitude,
                        longitude_deg=longitude,
                        elevation_ft=int(elevation) if elevation else None,
                        iso_country=_optional(row.get("iso_country")),
                        municipality=_optional(row.get("municipality")),
                        iata_code=_optional(row.get("iata_code")),
                    )
                )
            except (KeyError, ValueError):
                rejected_rows += 1
    return ValidationSummary(tuple(accepted), rejected_rows, file_sha256(path))


def _optional(value: str | None) -> str | None:
    normalized = (value or "").strip()
    return normalized or None
