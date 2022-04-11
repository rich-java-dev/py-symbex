# basic test file for branch detection/analysis


def test_func1(a: bool, b: bool) -> int:

    if a and b:
        return 1
    if a:
        return 2
    if b and not a:
        return 3
    if a and not a:
        return 4

    return 0


def test_func2(a: bool = True, b: bool = True, c: bool = True) -> int:
    if (a and not b) or c:
        return 1

    return 2


def test_func3(a: bool = True, b: bool = True, c: bool = True) -> int:
    if a and b and not c:
        return 1

    return 2


def test_func4(a: bool, b: bool = True) -> int:
    c: bool = True
    if a and b and not c:
        return 1

    return 2


def test_func5(a: bool, b: bool = True) -> int:
    c: bool = True
    c = False

    if a and b and not c:
        return 1

    return 2
