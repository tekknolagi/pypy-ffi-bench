import argparse
import json
import pathlib
import shlex
import subprocess
import sys
import tempfile
import textwrap


def run(
    cmd,
    verbose=True,
    cwd=None,
    check=True,
    capture_output=False,
    encoding="utf-8",
    # Specify an integer number of seconds
    timeout=-1,
    dry_run=False,
    **kwargs,
):
    # https://gist.github.com/tekknolagi/3b345cbc7035b8e10e50e7ec54cc7744
    if verbose:
        info = "$ "
        if cwd is not None:
            info += f"cd {cwd}; "
        info += " ".join(shlex.quote(c) for c in cmd)
        if capture_output:
            info += " >& ..."
        lines = textwrap.wrap(
            info,
            break_on_hyphens=False,
            break_long_words=False,
            replace_whitespace=False,
            subsequent_indent="  ",
        )
        print(" \\\n".join(lines))
    if timeout != -1:
        cmd = ["timeout", "--signal=KILL", f"{timeout}s", *cmd]
    if dry_run:
        return
    try:
        return subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            capture_output=capture_output,
            encoding=encoding,
            **kwargs,
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == -9:
            # Error code from `timeout` command signaling it had to be killed
            raise TimeoutError("Command timed out", cmd)
        raise


RUNTIME_PATHS = {
    "graalpy22": "~/.pyenv/versions/graalpython-22.2.0/bin/graalpython",
    "graalpy23": "~/.pyenv/versions/graalpy-community-23.1.0/bin/python3",
    "pypy3.10": "~/.pyenv/versions/pypy3.10-7.3.15/bin/pypy3.10",
    "pypy3.10-new": "~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c",
    "pypy3.8": "~/.pyenv/versions/pypy3.8-7.3.11/bin/python3",
    "python3.10": "/usr/bin/python3.10",
    "python3.11": "/usr/bin/python3.11",
    "python3.12": "/usr/bin/python3.12",
    "python3.13": "/usr/bin/python3.13",
    "python3.8": "/usr/bin/python3.8",
}


def filter_runtimes(runtimes, results_json):
    runtime_paths = set(RUNTIME_PATHS[runtime] for runtime in runtimes)
    with open(results_json, "r") as f:
        results = json.load(f)
    assert isinstance(results, dict)
    results = results["results"]
    filtered = []
    for result in results:
        runtime_path = result["parameters"]["runtime"]
        if runtime_path in runtime_paths:
            filtered.append(result)
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
        json.dump({"results": filtered}, f, indent=2)
        return f.name


def human_format(num):
    "https://stackoverflow.com/a/45846841/569183"
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(num).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude]
    )


def run_benchmark(args, benchmark):
    num_iterations = args.num_iterations
    outdir = args.output
    runtimes = sorted(args.runtimes)
    comma_runtime_paths = ",".join(RUNTIME_PATHS[runtime] for runtime in runtimes)
    comma_runtime_names = ",".join(runtimes)
    if num_iterations < 1_000_000_000 and "graal" in comma_runtime_names:
        print(
            f"WARNING: Graal will likely not get a chance to warm up with {human_format(num_iterations)} iterations"
        )
    run(["mkdir", "-p", outdir])
    if args.runtime_options:
        runtime_options = args.runtime_options.replace(" ", "_")
    else:
        runtime_options = ""
    json_output = f"{outdir}/results-{benchmark}{runtime_options}.json"
    if not args.plot_only:
        run(
            [
                "hyperfine",
                #
                "--export-json",
                json_output,
                #
                "--export-markdown",
                f"{outdir}/results-{benchmark}{runtime_options}.md",
                #
                "-L",
                "runtime",
                comma_runtime_paths,
                #
                # zsh and bash will fail on non-existent globs for e.g. *.so
                "--shell",
                "/usr/bin/sh",
                #
                "--setup",
                "rm -rf *.so build && {runtime} setup.py build_ext --inplace",
                #
                "--runs",
                "3",
                #
                f"taskset -c 0 {{runtime}} {args.runtime_options} {benchmark}.py {num_iterations}",
            ],
            verbose=True,
        )


def plot_single(args, benchmark):
    runtimes = args.runtimes
    outdir = args.output
    if args.runtime_options:
        runtime_options = args.runtime_options.replace(" ", "_")
    else:
        runtime_options = ""
    json_output = filter_runtimes(runtimes, f"{outdir}/results-{benchmark}{runtime_options}.json")
    with open(json_output, "r") as f:
        results_json = json.load(f)
        num_iterations = set(result["command"].split()[-1] for result in results_json["results"])
        assert len(num_iterations) == 1, "Benchmarks run for different iteration counts"
        num_iterations = int(num_iterations.pop())
    title = f"Time for {benchmark} with {human_format(num_iterations)} iterations (lower is better)"
    if args.runtime_options:
        title += f" ({args.runtime_options})"
    root = pathlib.Path(__file__).parent / ".."
    run(
        [
            sys.executable,
            str(root / "plot_whisker.py"),
            "--labels",
            ",".join(runtimes),
            "--title",
            title,
            "--output",
            f"{outdir}/results-{benchmark}{runtime_options}.png",
            "--dpi",
            str(args.dpi),
            json_output,
        ]
    )


def run_benchmarks(args):
    for benchmark in args.benchmark:
        run_benchmark(args, benchmark)


def plot_benchmarks(args):
    for benchmark in args.benchmark:
        plot_single(args, benchmark)


def parse_runtimes(comma_separated):
    return comma_separated.split(",")


BENCHMARKS = ["ffibench", "objbench", "idbench", "idbench_exc"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "benchmark",
        # TODO(max): Figure out how to get the choices to render and also limit
        # input without also converting to nargs='+' implicitly
        # choices=BENCHMARKS,
        nargs="*",
    )
    parser.add_argument("--num-iterations", type=int, default=1_000_000_000)
    parser.add_argument("--runtimes", default=RUNTIME_PATHS.keys(), type=parse_runtimes)
    parser.add_argument(
        "--graalpy23", action=argparse.BooleanOptionalAction, default=False
    )
    parser.add_argument("--runtime-options", default="")
    parser.add_argument("--output", default="out")
    parser.add_argument("--plot", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--plot-only", action=argparse.BooleanOptionalAction, default=False
    )
    parser.add_argument(
        "--dpi", type=int, default=300, help="Resolution in dots per inch (DPI)"
    )
    args = parser.parse_args()
    if not args.benchmark:
        args.benchmark = BENCHMARKS
    if not args.graalpy23:
        args.runtimes = [
            runtime for runtime in args.runtimes if "graalpy23" not in runtime
        ]
    if args.plot_only:
        args.plot = True
    if not args.plot_only:
        run_benchmarks(args)
    if args.plot:
        plot_benchmarks(args)


if __name__ == "__main__":
    main()
