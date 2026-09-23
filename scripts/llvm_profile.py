#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path


def entries(report: str) -> dict[str, int]:
    result: dict[str, int] = {}
    name: str | None = None
    for line in report.splitlines():
        if match := re.fullmatch(r"  (.+):", line):
            name = match.group(1)
        elif match := re.fullmatch(r"    Block counts: \[([0-9]+).*\]", line):
            if name is None:
                raise ValueError("LLVM profile contains counts without a function")
            count = int(match.group(1))
            if count:
                result[name] = count
            name = None
    if name is not None:
        raise ValueError("LLVM profile ended before function counts")
    return result


def run(
    command: list[str],
    environment: dict[str, str] | None = None,
    *,
    allow_failure: bool = False,
) -> str:
    result = subprocess.run(
        command, capture_output=True, check=False, env=environment, text=True
    )
    if result.returncode and not allow_failure:
        raise ValueError(f"{shlex.join(command)} failed:\n{result.stderr}")
    return result.stdout


def write(output: Path, rows: list[tuple[str, str, int]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(("harness", "function", "entries"))
        writer.writerows(sorted(rows))


def collect(harness: str, instrumented: Path, llvm_profdata: str, output: Path) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        raw = directory / "profile.profraw"
        data = directory / "profile.profdata"
        environment = os.environ | {"LLVM_PROFILE_FILE": str(raw)}
        run([str(instrumented)], environment, allow_failure=True)
        if not raw.is_file():
            raise ValueError(f"{harness} wrote no LLVM profile")
        run([llvm_profdata, "merge", "--sparse", str(raw), "-o", str(data)])
        counts = entries(
            run([llvm_profdata, "show", "--all-functions", "--counts", str(data)])
        )
    write(output, [(harness, function, count) for function, count in counts.items()])


def merge(inputs: list[Path], output: Path) -> None:
    rows: list[tuple[str, str, int]] = []
    for input_path in inputs:
        with input_path.open(encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            if next(reader, None) != ["harness", "function", "entries"]:
                raise ValueError(f"{input_path} has an invalid LLVM profile CSV header")
            for row in reader:
                if len(row) != 3 or not row[0] or not row[1] or not row[2].isdecimal():
                    raise ValueError(
                        f"{input_path} has an invalid LLVM profile CSV row"
                    )
                rows.append((row[0], row[1], int(row[2])))
    write(output, rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    collect_parser = commands.add_parser("collect")
    collect_parser.add_argument("--harness", required=True)
    collect_parser.add_argument("--instrumented", type=Path, required=True)
    collect_parser.add_argument("--llvm-profdata", required=True)
    collect_parser.add_argument("--output", type=Path, required=True)
    merge_parser = commands.add_parser("merge")
    merge_parser.add_argument("--output", type=Path, required=True)
    merge_parser.add_argument("inputs", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "collect":
            collect(args.harness, args.instrumented, args.llvm_profdata, args.output)
        else:
            merge(args.inputs, args.output)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
