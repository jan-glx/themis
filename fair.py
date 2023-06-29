import random
import logging

def unfair() -> bool:
    """Generates an unfair coin toss."""
    i = 0
    while True:
        i = i + 1
        out = random.choice((True, False))
        if not i % 100000:
            logging.info(f"{i}th unfair toss: {out}")
        yield out

def push_and_forward(coroutine, value):
    """Pushes a value into a coroutine and yields all its output neccessary to do so."""
    while True:
        result = coroutine.send(value)
        if result is not None:
            yield result
        else:
            break

def push_all_and_forward(coroutine, generator):
    """Pushes all values from a generator into a coroutine and yields its output."""
    for i in generator:
        yield from push_and_forward(coroutine, i)

def fair_maker():
    """Generates a fair coin toss from an unfair source."""
    coin_toss_1 = yield
    coin_toss_2 = yield

    are_equal_fair_maker = fair_maker()
    next(are_equal_fair_maker)
    
    which_if_equal_fair_maker = fair_maker()
    next(which_if_equal_fair_maker)

    while True:
        # P(coin_toss_1,coin_toss_2) can be decomposed into  P(coint_toss_1 | coin_toss_1=coin_toss_2) P(coin_toss_1=coin_toss_2) 
        if coin_toss_1 == coin_toss_2:
            yield from push_and_forward(which_if_equal_fair_maker, coin_toss_1)
        else:
            yield coin_toss_1 # Given that "Heads,Tails" is as likely as "Tails,Heads" this is a fair coin toss

        yield from push_and_forward(are_equal_fair_maker, coin_toss_1 == coin_toss_2)

        coin_toss_1 = yield
        coin_toss_2 = yield

def make_fair(generator):
    """Makes an unfair generator fair."""
    fair = fair_maker()
    next(fair)
    yield from push_all_and_forward(fair, generator)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    fair_coin = make_fair(unfair())

    j = 0
    for _ in range(10000000):
        j = j + 1
        fair_toss = next(fair_coin)
        if not j % 100000:
            logging.info(f"{j}th fair toss: {fair_toss}")
