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

hyperfine --export-json results-idbench.json \
  -L runtime \
  ~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c,~/.pyenv/versions/pypy3.10-7.3.15/bin/pypy3.10 \
  --setup 'rm -f *.so && {runtime} setup.py build_ext --inplace' \
  --runs 3 \
  'taskset -c 0 {runtime} idbench.py'
