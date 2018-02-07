import random


def unfair():
    i = 0
    while True:
        i = i + 1
        out = random.choice((True, False))  # True,
        print(i, "th unfair toss:", out)
        yield out


def fair():
    a = yield
    b = yield
    next_level = fair()
    next(next_level)
    emitted = fair()
    next(emitted)
    while True:
        if a == b:
            while True:
                next_level_out = next_level.send(a)
                if next_level_out is None:
                    break
                else:
                    yield next_level_out
        else:
            yield a

        while True:
            emitted_out = emitted.send(a != b)
            if emitted_out is None:
                break
            else:
                yield emitted_out

        a = yield
        b = yield


def fair_gen(g):
    fair_ = fair()
    next(fair_)
    while True:
        next_in = next(g)
        while True:
            next_out = fair_.send(next_in)
            if next_out is None:
                break
            else:
                yield next_out


fair_coin = fair_gen(unfair())
j = 0
for e in range(1000000):
    j = j + 1
    fc = next(fair_coin)
    print(j, "th fair toss:", fc)
