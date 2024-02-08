#!/bin/sh

set -eux

hyperfine --export-json results.json \
  -L runtime \
  ~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c,pypy3.8,python3.8,python3.10,python3.11,python3.12,python3.13,~/.pyenv/versions/graalpython-22.2.0/bin/graalpython \
  --setup '{runtime} setup.py build_ext --inplace' \
  --runs 3 \
  'taskset -c 0 {runtime} ffibench.py'
