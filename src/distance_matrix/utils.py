def permutations(sequence):
    """
    Returns the set of permutations from a single sequence.

    This is available as `itertools.permutations`,
    but implemented here as an example of type vars.
    """
    length = len(sequence)
    for i in range(length):
        for j in range(i + 1, length):
            yield (sequence[i], sequence[j])
