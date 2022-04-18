
def test1(a: int, b: int, c: bool):

    if a > 100 or b > 100:
        return 1

    if a < 0 and b > 0:
        return 1


def test2(a: int, b: int, c: bool):

    if c and a > 100:
        return 1

    if b < 100 and not c:
        return 2


def test3(a: int, b: int):

    c: int = a + b

    if c > 100:
        return 1
    elif c < 0:
        return 2
    elif c == b:
        return 3
    else:
        return 4


def test4(a: int, b: int):
    if a > b and b > 100:
        if a % b == 0:
            return 1
        else:
            return 2
    elif a > 100:
        return 3
    elif a < b:
        return 4
    else:
        return 5


def test5(a: int, b: int, c: bool):

    if c:
        if a == 1:
            return 1
        elif a == 2:
            return 2
        elif b == 3:
            return 3
        else:
            return 4
    elif a > 100:
        if c:
            return 5
        else:
            return 6


def test6(a: int, b: int):
    if a % 10 == 0:
        return 1
    elif a % 100 == 0:
        return 2
    elif b % 3 == 0:
        return 3
    else:
        return 4
