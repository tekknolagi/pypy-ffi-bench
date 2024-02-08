import signature


def main():
    i = 0
    for _ in signature.RangeIterator(10_000_000):
        i += 1
    return i


if __name__ == "__main__":
    print(main())
