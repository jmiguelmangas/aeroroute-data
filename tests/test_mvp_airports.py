import csv
from pathlib import Path

import pytest

from aeroroute_data.mvp_airports import (
    MVP_AIRPORT_IDENTS,
    write_mvp_airports_csv,
)


def test_mvp_selection_is_complete_and_deterministic(tmp_path: Path) -> None:
    source = tmp_path / "global.csv"
    destination = tmp_path / "selected.csv"
    with source.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("ident", "name"))
        writer.writeheader()
        for ident in reversed(MVP_AIRPORT_IDENTS):
            writer.writerow({"ident": ident, "name": ident})
        writer.writerow({"ident": "ZZZZ", "name": "Not selected"})

    count = write_mvp_airports_csv(source, destination)
    rows = list(csv.DictReader(destination.open(encoding="utf-8")))

    assert count == len(MVP_AIRPORT_IDENTS)
    assert [row["ident"] for row in rows] == list(MVP_AIRPORT_IDENTS)


def test_mvp_selection_rejects_incomplete_source(tmp_path: Path) -> None:
    source = tmp_path / "global.csv"
    source.write_text("ident,name\nLEMD,Madrid\n")

    with pytest.raises(ValueError, match="source is missing"):
        write_mvp_airports_csv(source, tmp_path / "selected.csv")
