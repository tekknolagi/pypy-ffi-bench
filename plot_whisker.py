#!/usr/bin/env python
# From https://github.com/sharkdp/hyperfine/blob/master/scripts/README.md

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
parser.add_argument("file", help="JSON file with benchmark results")
parser.add_argument("--title", help="Plot Title")
parser.add_argument(
    "--labels", help="Comma-separated list of entries for the plot legend"
)
parser.add_argument(
    "-o", "--output", help="Save image to the given filename."
)
parser.add_argument("--dpi", type=int, default=300, help="Resolution in dots per inch (DPI)")

args = parser.parse_args()

with open(args.file) as f:
    results = json.load(f)["results"]

if args.labels:
    labels = args.labels.split(",")
else:
    labels = [b["command"].split(" ")[0] for b in results]
times = [b["times"] for b in results]

boxplot = plt.boxplot(times, vert=True, patch_artist=True)
cmap = plt.get_cmap("rainbow")
colors = [cmap(val / len(times)) for val in range(len(times))]

for patch, color in zip(boxplot["boxes"], colors):
    patch.set_facecolor(color)

if args.title:
    plt.title(args.title)
plt.subplots_adjust(bottom=0.20)
plt.xticks(range(1,len(labels)+1), labels, rotation=45)
plt.ylabel("Time [s]")
plt.ylim(0, None)
if args.output:
    plt.savefig(args.output, dpi=args.dpi)
else:
    plt.show()
