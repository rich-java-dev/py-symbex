
def test1(a: int, b: int, c: bool):

    if a > 100 or b > 100:
        return 1

    if a < 0 and b > 0:
        return 1


def test1(a: int, b: int, c: bool):

    if c and a > 100:
        return 1

    if b < 100 and c:
        return 2
