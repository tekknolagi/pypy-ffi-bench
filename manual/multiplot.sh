#!/bin/sh
set -eux
out=out-nojit
python3 benchmark.py --runtimes pypy3.10-new,pypy3.10 --num-iterations 10_000_000 --output "$out" --runtime-options="--jit off"
python3 ../plot_whisker_multi.py --suptitle "Times for 10MM iterations with JIT off; lower is better" \
  --output "$out"/results-jit-off-multi.png --labels "pypy3.10,pypy3.10-new" \
  "$out"/results-ffibench--jit_off.json \
  "$out"/results-objbench--jit_off.json \
  "$out"/results-idbench--jit_off.json \
  "$out"/results-idbench_exc--jit_off.json \
  --title ffibench \
  --title objbench \
  --title idbench \
  --title idbench_exc \
