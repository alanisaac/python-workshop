from typing import Iterable, List


def _pluralize_word(word: str) -> str:
    if word.endswith(("s", "x")):
        return word + "es"
    elif word.endswith("y"):
        return word[:-1] + 'ies'
    else:
        return word + 's'


def pluralize_not_pure(words: List[str]) -> None:
    for i in range(len(words)):
        plural = _pluralize_word(words[i])
        words[i] = plural


def pluralize_pure(words: Iterable[str]) -> List[str]:
    result = []
    for word in words:
        plural = _pluralize_word(word)
        result.append(plural)
    return result
