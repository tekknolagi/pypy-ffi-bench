import signature


def main(n):
    i = 0
    while i < n:
        i = signature.inc(i)
    return i


if __name__ == "__main__":
    print(main(int(__import__("sys").argv[1])))
