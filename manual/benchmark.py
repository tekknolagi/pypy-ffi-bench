import argparse
import shlex
import subprocess
import sys
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


ALL_RUNTIMES = [
    "pypy3.8",
    "pypy3.10",
    "python3.8",
    "python3.10",
    "python3.11",
    "python3.12",
    "python3.13",
    "graalpy22",
    "graalpy23",
]

RUNTIME_PATHS = {
    "pypy3.8": "~/.pyenv/versions/pypy3.8-7.3.11/bin/python3",
    "pypy3.10": "~/.pyenv/versions/pypy3.10-7.3.15/bin/pypy3.10",
    "pypy3.10-new": "~/Documents/dev/pypy-git/pypy/goal/pypy3.10-c",
}


def run_benchmark(args):
    benchmark = args.benchmark
    runtimes = [RUNTIME_PATHS[runtime] for runtime in args.runtimes]
    run(
        [
            "hyperfine",
            #
            "--export-json",
            f"results-{benchmark}.json",
            #
            "--export-markdown",
            f"results-{benchmark}.md",
            #
            "-L",
            "runtime",
            ",".join(runtimes),
            #
            "--setup",
            "rm -rf *.so && {runtime} setup.py build_ext --inplace",
            #
            "--runs",
            "3",
            #
            f"taskset -c 0 {{runtime}} {args.runtime_options} {benchmark}.py {args.num_iterations}",
        ],
        verbose=True,
    )


def parse_runtimes(comma_separated):
    return comma_separated.split(",")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark", choices=["ffibench", "objbench", "idbench"])
    parser.add_argument("--num-iterations", type=int, required=True)
    parser.add_argument("--runtimes", default=ALL_RUNTIMES, type=parse_runtimes)
    parser.add_argument("--runtime-options", default="")
    args = parser.parse_args()
    run_benchmark(args)


if __name__ == "__main__":
    main()
