from distance_matrix.utils import permutations


def test_permutations_return_correct_pairs():
    items = (1, 2, 3)

    result = permutations(items)

    assert [*result] == [(1, 2), (1, 3), (2, 3)]


def test_permutations_returns_empty_when_empty():
    result = permutations([])

    assert [*result] == []
