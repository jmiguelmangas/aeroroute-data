from pathlib import Path

from aeroroute_data.airports import validate_airports_csv


def test_validates_local_ourairports_fixture() -> None:
    fixture = Path(__file__).parent / "fixtures" / "airports.csv"
    result = validate_airports_csv(fixture)

    assert len(result.accepted) == 2
    assert result.rejected_rows == 1
    assert result.accepted[0].ident == "LEMD"
    assert len(result.sha256) == 64
