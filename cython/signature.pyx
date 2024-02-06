import cython

cpdef cython.long inc(x: cython.long):
    return x + 1
