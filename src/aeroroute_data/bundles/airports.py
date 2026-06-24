"""Immutable, normalized airport bundle generation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from aeroroute_data.airports import validate_airports_csv


@dataclass(frozen=True, slots=True)
class BundleManifest:
    version: str
    source_sha256: str
    bundle_sha256: str
    accepted_rows: int
    rejected_rows: int
    source_kind: str = "public"
    contract_version: str = "1.0.0"


def build_airport_bundle(
    source_csv: Path, output_dir: Path, version: str
) -> BundleManifest:
    summary = validate_airports_csv(source_csv)
    output_dir.mkdir(parents=True, exist_ok=True)
    records = [asdict(record) for record in summary.accepted]
    canonical_records = json.dumps(
        records, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    bundle_sha256 = hashlib.sha256(canonical_records.encode()).hexdigest()
    (output_dir / "airports.normalized.json").write_text(
        canonical_records + "\n", encoding="utf-8"
    )
    manifest = BundleManifest(
        version=version,
        source_sha256=summary.sha256,
        bundle_sha256=bundle_sha256,
        accepted_rows=len(summary.accepted),
        rejected_rows=summary.rejected_rows,
    )
    (output_dir / "manifest.json").write_text(
        json.dumps(asdict(manifest), sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest
