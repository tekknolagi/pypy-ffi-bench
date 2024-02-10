import signature


def main():
    i = 0
    while True:
        try:
            i = signature.inc_might_raise(i)
        except StopIteration:
            return i
    return i


if __name__ == "__main__":
    print(main())
