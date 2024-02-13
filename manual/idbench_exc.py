import signature


def main(n):
    i = 0
    obj = object()
    while i < n:
        signature.meth_o_object_may_raise(obj)
        i += 1
    return i


if __name__ == "__main__":
    print(main(int(__import__("sys").argv[1])))
