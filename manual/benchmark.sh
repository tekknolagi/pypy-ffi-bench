#!/bin/sh

set -eux

hyperfine --export-json results.json \
  -L runtime \
  ~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c,pypy3.8,python3.8,python3.10,python3.11,python3.12,python3.13 \
  --setup '{runtime} setup.py build_ext --inplace' \
  --warmup 1 --runs 10 \
  '{runtime} ffibench.py'
