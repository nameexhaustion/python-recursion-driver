from GenDriver import GenDriver, GenTask


def test(x):
    yield x
    if x == 1000:
        return

    it = test(1 + x)
    while True:
        v = yield GenTask(generator=it)
        if v == StopIteration:
            break

        yield v

    yield x


for v in GenDriver(test(0)).iter():
    print(v)
