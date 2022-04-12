from GenDriver import GenDriver, GenTask, GenResult


def test(x):
    yield x
    if x == 10000:
        return

    it = test(1 + x)
    v = yield GenTask(generator=it)
    while v != StopIteration:
        yield v
        v = yield GenTask(generator=it)


for v in GenDriver(test(0)).iter():
    print(v)
