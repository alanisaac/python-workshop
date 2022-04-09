import filecmp
from pathlib import Path

from distance_matrix.main import run


def test_run_calculates_distances():
    data_file = Path(__file__).parent / "data" / "locations.csv"
    output_file = Path(__file__).parent / "data" / "output.csv"
    expected_file = Path(__file__).parent / "data" / "expected_output.csv"

    _ = run(data_file)

    assert filecmp.cmp(output_file, expected_file)
