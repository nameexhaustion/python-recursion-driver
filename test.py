from GenDriver import GenDriver, GenTask


def test(x):
    yield x
    if x == 1000:
        return

    it = test(1 + x)
    v = yield GenTask(generator=it)
    while v != StopIteration:
        yield v
        v = yield GenTask(generator=it)

    yield x


for v in GenDriver(test(0)).iter():
    print(v)
