import signature


def main():
    i = 0
    while i < 1_000_000_000:
        i = signature.inc(i)
    return i


if __name__ == "__main__":
    print(main())
