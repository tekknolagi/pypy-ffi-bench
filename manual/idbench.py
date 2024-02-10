import signature


def main():
    i = 0
    obj = object()
    while i < 500_000_000:
        signature.meth_o_object(obj)
        i += 1
    return i


if __name__ == "__main__":
    print(main())
