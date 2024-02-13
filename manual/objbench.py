import signature


def main(n):
    i = 0
    obj = object()
    while i < n:
        i = signature.takes_object(obj, i)
    return i


if __name__ == "__main__":
    print(main(int(__import__("sys").argv[1])))
