import filecmp
from pathlib import Path

import pytest

from distance_matrix import async_runner, main, pandas_runner


def test_run_calculates_distances():
    data_file = Path(__file__).parent / "data" / "locations.csv"
    output_file = Path(__file__).parent / "data" / "output.csv"
    expected_file = Path(__file__).parent / "data" / "expected_output.csv"

    _ = main.run(data_file)

    assert filecmp.cmp(output_file, expected_file)


@pytest.mark.asyncio
async def test_async_run_calculates_distances():
    data_file = Path(__file__).parent / "data" / "locations.csv"
    output_file = Path(__file__).parent / "data" / "output.csv"
    expected_file = Path(__file__).parent / "data" / "expected_output.csv"

    _ = await async_runner.run(data_file)

    assert filecmp.cmp(output_file, expected_file)


def test_pandas_run_calculates_distances():
    data_file = Path(__file__).parent / "data" / "locations.csv"
    output_file = Path(__file__).parent / "data" / "output.csv"
    expected_file = Path(__file__).parent / "data" / "expected_output.csv"

    _ = pandas_runner.run(data_file)

    assert filecmp.cmp(output_file, expected_file)
