# basic test file for branch detection/analysis


def test_func1(a: int = 0):

    while a < 100:
        if a == 10:
            return 1
        if a > 50:
            return 2

        if a == 100:
            return 3


def test_func2(a: bool = True, b: int = 0) -> int:

    i: int = b
    while a:

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


# def test_func2(a: bool = True, b: int = 0) -> int:

#     i: int = b
#     while i <= 10:
#         i = i + 1

#         if i == 1:
#             print(f"i = {i}")
#         if i < 5:
#             print(f"{i} < 5")
#         elif i == 5:
#             print(f"{i} == 5")
#         else:
#             print(f"{i} >= 5")

#         if i > 10:
#             a = False
