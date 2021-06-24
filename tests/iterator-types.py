from typing import Iterator

def fib(n: int) -> Iterator[int]:
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a+b

print(next(fib(5)))


def test(n: str) -> None:
    print(n)


test(23)