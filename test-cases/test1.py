# basic test file for branch detection/analysis


def test_func(a: bool = True, b: bool = False) -> int:

    if a and b:
        return 1
    if a:
        return 2
    if b and not a:
        return 3
    else:
        return 4


def test_func3(a: bool = True, b: bool = True, c: bool = True) -> int:
    if (a and not b) or c:
        return 1

    return 2


def test_func3(a: bool = True, b: bool = True, c: bool = True) -> int:
    if a and b and not c:
        return 1

    return 2
