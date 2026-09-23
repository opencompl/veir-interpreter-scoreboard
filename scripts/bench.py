#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import platform
import shlex
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path

from make_config import cflags, harnesses


class Outcome(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class Profile:
    outcome: Outcome
    entries: Mapping[str, int]


@dataclass(frozen=True, slots=True)
class Row:
    name: str
    native: Profile
    veir: Profile


@dataclass(frozen=True, slots=True)
class VeirIdentity:
    source: str
    executable_sha256: str
    revision: str


def llvm_profiles(path: Path) -> dict[str, Profile]:
    counts: dict[str, dict[str, int]] = {str(harness): {} for harness in harnesses()}
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["harness", "function", "entries"]:
            raise ValueError("invalid LLVM profile CSV header")
        for row in reader:
            harness = row.get("harness")
            function = row.get("function")
            entries = row.get("entries")
            if (
                harness not in counts
                or not function
                or entries is None
                or not entries.isdecimal()
            ):
                raise ValueError("invalid LLVM profile CSV row")
            counts[harness][function] = int(entries)
    return {
        harness: Profile(Outcome.SUCCESS, entries)
        for harness, entries in counts.items()
    }


def veir_profile(corpus: Path, harness: Path) -> Profile:
    root = corpus / harness.with_suffix("")
    try:
        status = int(
            root.with_suffix(".veir-status").read_text(encoding="utf-8").strip()
        )
        output = root.with_suffix(".veir-output.txt").read_text(encoding="utf-8")
    except (OSError, ValueError):
        return Profile(Outcome.FAILED, {})
    if status:
        return Profile(Outcome.FAILED, {})
    entries: dict[str, int] = {}
    for line in output.splitlines():
        name, tab, count = line.rpartition("\t")
        if not tab or not name or not count.isdecimal():
            continue
        value = int(count)
        if value:
            entries[name] = value
    return Profile(Outcome.SUCCESS, entries)


def run_text(command: list[str], *, cwd: Path | None = None) -> str:
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, check=False, text=True
    )
    if result.returncode:
        raise ValueError(f"{shlex.join(command)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def file_sha256(path: Path) -> str:
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def veir_executable(source: Path) -> Path:
    located = run_text(["lake", "env", "which", "veir-interpret"], cwd=source)
    path = Path(located)
    if not path.is_absolute():
        path = source / path
    if not path.is_file():
        raise ValueError(f"veir-interpret executable not found: {path}")
    return path.resolve()


def veir_identity(source: Path) -> VeirIdentity:
    if not source.is_dir():
        raise ValueError(f"VeIR source directory does not exist: {source}")
    root = Path(run_text(["git", "rev-parse", "--show-toplevel"], cwd=source)).resolve()
    revision = run_text(["git", "rev-parse", "HEAD"], cwd=root)
    executable = veir_executable(root)
    return VeirIdentity(str(root), file_sha256(executable), revision)


def profile_rows(corpus: Path) -> list[Row]:
    llvm_profiles_by_harness = llvm_profiles(corpus / "llvm-profile.csv")
    return [
        Row(
            str(harness),
            llvm_profiles_by_harness[str(harness)],
            veir_profile(corpus, harness),
        )
        for harness in harnesses()
    ]


def summary(rows: list[Row]) -> list[str]:
    lines = [
        "| Profile | Functions executed | `veir-interpret` functions executed | "
        "Status | Completion |",
        "|---|---:|---:|---|---:|",
    ]
    for row in rows:
        shared = len(set(row.native.entries) & set(row.veir.entries))
        completion = (
            "N/A"
            if not row.native.entries
            else f"{100 * shared / len(row.native.entries):.1f}%"
        )
        status = row.veir.outcome.upper()
        lines.append(
            f"| `{row.name}` | {len(row.native.entries)} | {len(row.veir.entries)} | "
            f"{status} | {completion} |"
        )
    return lines


def details(rows: list[Row]) -> list[str]:
    lines: list[str] = []
    lines.extend(
        [
            "",
            "## Details",
            "",
            "<details>",
            "<summary>Per-function execution counts</summary>",
            "",
        ]
    )
    for row in rows:
        lines.extend(
            [
                f"### `{row.name}`",
                "",
                "| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |",
                "|---|---:|---:|",
            ]
        )
        for function in sorted(set(row.native.entries) | set(row.veir.entries)):
            lines.append(
                f"| `{function}` | {row.native.entries.get(function, 0)} | "
                f"{row.veir.entries.get(function, 0)} |"
            )
        lines.append("")
    lines.extend(["</details>"])
    return lines


def provenance(source: Path) -> list[str]:
    identity = veir_identity(source)
    return [
        "",
        "## Provenance",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| VeIR | `{identity.revision}` |",
        f"| VeIR source | `{identity.source}` |",
        f"| `veir-interpret` SHA-256 | `{identity.executable_sha256}` |",
        f"| C flags | `{' '.join(cflags())}` |",
        f"| Scored | `{datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}` |",
        f"| Host | `{platform.system()} {platform.machine()}` |",
    ]


def render(corpus: Path, source: Path) -> str:
    rows = profile_rows(corpus)
    lines = [
        "# VeIR execution scoreboard",
        "",
        "Whole-program SQLite-and-harness O3 corpus with cached LLVM entry counts.",
        "",
        *summary(rows),
        *details(rows),
        *provenance(source),
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    scoreboard = commands.add_parser("scoreboard")
    scoreboard.add_argument("--corpus", type=Path, required=True)
    scoreboard.add_argument("--output", type=Path, required=True)
    scoreboard.add_argument("--veir-source", type=Path, required=True)
    args = parser.parse_args()
    try:
        args.output.write_text(render(args.corpus, args.veir_source), encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
