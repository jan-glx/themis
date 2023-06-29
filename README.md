# Themis
Provides a coroutine-baesed python implementation of an algorithm that allows to produces samples from a fair coin given samples from a possibly biased coin.

Thr relevant parts are:
```python
def push_and_forward(coroutine, value):
    """Pushes a value into a coroutine and yields all its output neccessary to do so."""
    while True:
        result = coroutine.send(value)
        if result is not None:
            yield result
        else:
            break

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

```

Based on great writeup ["Tossing a Biased Coin" by Michael Mitzenmacher](http://www.eecs.harvard.edu/~michaelm/coinflipext.pdf)

Proof of optimality (statistical not computational):
[“Iterating von Neumann’s Procedure” by Yuval Peres, in The Annals of Statistics](https://projecteuclid.org/euclid.aos/1176348543)
