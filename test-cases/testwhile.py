# basic test file for branch detection/analysis

def test_func(a: bool = True, b: int = 0) -> int:

    i: int = 0
    while a:
        i = i + 1
        b = b - 1

        if i == 1:
            print(f"i = {i}")
        if i < 5:
            print(f"{i} < 5")
        elif i == 5:
            print(f"{i} == 5")
        else:
            print(f"{i} >= 5")

        if i > 10:
            a = False
