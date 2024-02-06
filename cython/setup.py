from setuptools import setup
from Cython.Build import cythonize

# python3.10 setup.py build_ext --inplace
setup(
    ext_modules = cythonize("signature.pyx")
)
