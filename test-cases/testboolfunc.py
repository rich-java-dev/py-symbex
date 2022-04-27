def not_func(a: bool) -> bool:
    return not a


def test1(a: bool):

    if not_func(a):
        return 1
