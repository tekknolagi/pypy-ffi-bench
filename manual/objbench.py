import signature


def main():
    i = 0
    obj = object()
    while i < 500_000_000:
        i = signature.takes_object(obj, i)
    return i


if __name__ == "__main__":
    print(main())
