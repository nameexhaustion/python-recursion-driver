def test(x):
    if x == 1000:
        return

    return x + test(1 + x)


print(test(0))
