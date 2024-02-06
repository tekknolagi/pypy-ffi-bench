import setuptools

setuptools.setup(
    name="ffibench",
    version="0.0.1",
    description="",
    ext_modules=[
        setuptools.Extension(
            "signature", sources=["signature.c"],
            extra_compile_args=['-std=c99', '-Wall', '-Wextra'],
            language='c',
            )
        ],
    url="https://github.com/tekknolagi/no",
    author="Maxwell Bernstein",
    packages=setuptools.find_packages(),
    author_email="python@bernsteinbear.com",
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
