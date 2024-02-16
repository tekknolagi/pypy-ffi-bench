#!/usr/bin/env python
# From https://github.com/sharkdp/hyperfine/blob/master/scripts/README.md

# For example,
# plot_whisker_multi.py out/results-ffibench--jit_off.json out/results-idbench_exc--jit_off.json out/results-idbench--jit_off.json out/results-objbench--jit_off.json  --title "ffibench (jit off)" --title "idbench_exc (jit off)" --title "idbench (jit off)" --title "objbench (jit off)" --output /tmp/foo.png --labels "pypy-base,pypy-new"

"""This program shows `hyperfine` benchmark results as a box and whisker plot.

Quoting from the matplotlib documentation:
    The box extends from the lower to upper quartile values of the data, with
    a line at the median. The whiskers extend from the box to show the range
    of the data. Flier points are those past the end of the whiskers.
"""

import argparse
import json
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("files", nargs='+', help="JSON file with benchmark results")
parser.add_argument("--title", default=[], action="append", help="Plot Title")
parser.add_argument(
    "--labels", help="Comma-separated list of entries for the plot legend"
)
parser.add_argument(
    "-o", "--output", help="Save image to the given filename."
)

args = parser.parse_args()
assert len(args.files) == 4, f"Don't know how to lay out {len(args.files)} plots"
assert len(args.files) == len(args.title), "len(files) must equal len(titles)"

def load_data(filename):
    with open(filename) as f:
        results = json.load(f)["results"]

    if args.labels:
        labels = args.labels.split(",")
    else:
        labels = [b["command"].split(" ")[0] for b in results]

    times = [b["times"] for b in results]

    return (times, labels)


data = [load_data(filename) for filename in args.files]
fig, axs = plt.subplots(2, 2, sharey=True, sharex=True)
for idx, datum in enumerate(data):
    times, labels = data[idx]
    ax = axs.flat[idx]
    ax.boxplot(times, vert=True, patch_artist=True)
    ax.set_xticks(range(1,len(labels)+1), labels)
    ax.set_title(args.title[idx])

fig.supylabel("Time [s]")
plt.ylim(0, None)
if args.output:
    plt.savefig(args.output)
else:
    plt.show()
