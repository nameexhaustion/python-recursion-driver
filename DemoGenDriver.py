from GenDriverLib import GenDriverLib, Result, GenTask


def test(x):
    if x == 1000:
        return

    v = yield GenTask(generator=test(1 + x), resultMode="iter")

    if v == StopIteration:
        yield Result(result=x)

    yield Result(result=x + v.result)


print(
    next(
        GenDriverLib.fromTask(GenTask(generator=test(0), resultMode="iter")).iter()
    ).result
)
