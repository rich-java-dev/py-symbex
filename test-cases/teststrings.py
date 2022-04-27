def test1(a: str, b: int):

    c: str = "test string"

    if a == 'GET':
        if b > 0:
            return 1
        else:
            return 2

    elif a == 'POST':
        return 2

    elif a == 'PUT':
        return 4

    elif a == 'DELETE':
        return 5
