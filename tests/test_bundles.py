import json
from pathlib import Path

from aeroroute_data.bundles.airports import build_airport_bundle


def test_builds_deterministic_bundle_and_manifest(tmp_path: Path) -> None:
    source = Path(__file__).parent / "fixtures" / "airports.csv"
    manifest = build_airport_bundle(source, tmp_path, "2026.06.1")

    bundle = json.loads((tmp_path / "airports.normalized.json").read_text())
    written_manifest = json.loads((tmp_path / "manifest.json").read_text())

    assert len(bundle) == 2
    assert bundle[0]["ident"] == "LEMD"
    assert manifest.bundle_sha256 == written_manifest["bundle_sha256"]
    assert manifest.rejected_rows == 1
