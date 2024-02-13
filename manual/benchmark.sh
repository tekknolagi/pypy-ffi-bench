#!/bin/sh

set -eux

# hyperfine --export-json results-ffibench.json \
#   -L runtime \
#   ~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c,pypy3.8,python3.8,python3.10,python3.11,python3.12,python3.13,~/.pyenv/versions/graalpython-22.2.0/bin/graalpython \
#   --setup '{runtime} setup.py build_ext --inplace' \
#   --runs 3 \
#   'taskset -c 0 {runtime} ffibench.py'

# hyperfine --export-json results-objbench.json \
#   -L runtime \
#   ~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c,pypy3.8,python3.8,python3.10,python3.11,python3.12,python3.13,~/.pyenv/versions/graalpython-22.2.0/bin/graalpython \
#   --setup '{runtime} setup.py build_ext --inplace' \
#   --runs 3 \
#   'taskset -c 0 {runtime} objbench.py'

# hyperfine --export-json results-idbench.json --export-markdown results-idbench.md \
#   -L runtime \
#   ~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c,pypy3.8,python3.8,python3.10,python3.11,python3.12,python3.13,~/.pyenv/versions/graalpython-22.2.0/bin/graalpython,~/.pyenv/versions/graalpy-community-23.1.0/bin/python3 \
#   --setup 'rm -f *.so && {runtime} setup.py build_ext --inplace' \
#   --runs 3 \
#   'taskset -c 0 {runtime} idbench.py'

# hyperfine --export-json results-idbench-nojit.json --export-markdown results-idbench-nojit.md \
#   -L runtime \
#   ~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c,pypy3.8,~/.pyenv/versions/pypy3.10-7.3.15/bin/pypy3.10 \
#   --setup 'rm -f *.so && {runtime} setup.py build_ext --inplace' \
#   --runs 3 \
#   'taskset -c 0 {runtime} --jit off idbench.py'

# hyperfine --export-json results-objbench-nojit.json --export-markdown results-objbench-nojit.md \
#   -L runtime \
#   ~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c,~/.pyenv/versions/pypy3.10-7.3.15/bin/pypy3.10,~/.pyenv/versions/pypy3.8-7.3.11/bin/python3 \
#   --setup 'rm -f *.so && {runtime} setup.py build_ext --inplace' \
#   --runs 3 \
#   'taskset -c 0 {runtime} --jit off objbench.py'

hyperfine --export-json results-ffibench-nojit.json --export-markdown results-ffibench-nojit.md \
  -L runtime \
  ~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c,~/.pyenv/versions/pypy3.10-7.3.15/bin/pypy3.10,~/.pyenv/versions/pypy3.8-7.3.11/bin/python3 \
  --setup 'rm -f *.so && {runtime} setup.py build_ext --inplace' \
  --runs 3 \
  'taskset -c 0 {runtime} --jit off ffibench.py'
