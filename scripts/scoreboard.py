#!/usr/bin/env python3
"""Compare the veir-interpret and llubi outputs in the corpus and write SCOREBOARD.md."""

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Literal

from capture import EXIT_STATUS, TIMEOUT
from corpus_manifest import sha256

VEIR_REPOSITORY = "https://github.com/opencompl/veir"

# Outcomes


type Kind = Literal["returned", "UB", "unsupported", "timeout"]


@dataclass(frozen=True, slots=True)
class Outcome:
    kind: Kind
    line: str | None  # The line of the output it was read from.
    value: str | None = None
    reason: str | None = None


def find(pattern: str, lines: Iterable[str]) -> re.Match[str] | None:
    """The first line that matches `pattern`, if any."""
    return next(filter(None, (re.fullmatch(pattern, line) for line in lines)), None)


def exit_status(lines: list[str]) -> str:
    return lines[-1].removeprefix(EXIT_STATUS)


def llubi_outcome(trace: str) -> Outcome:
    lines = trace.splitlines()
    if ub := find(r"Immediate UB detected: .*", lines):
        return Outcome("UB", ub[0])
    # `main` returns last, so its `ret` is the last one in the trace.
    ret = find(r"\s*ret (.*?)\s*", reversed(lines))
    if exit_status(lines) == "0" and ret:
        return Outcome("returned", f"ret {ret[1]}", llubi_value(ret[1]))
    raise ValueError("llubi neither returned from main nor reported UB")


def veir_outcome(trace: str) -> Outcome:
    lines = trace.splitlines()
    status = exit_status(lines)
    if status == TIMEOUT:
        return Outcome("timeout", None)
    if status == "0" and (output := find(r"Program output: (.*)", lines)):
        return Outcome("returned", output[0], veir_value(output[1]))
    if status == "0" and (ub := find(r"Undefined behavior.*", lines)):
        return Outcome("UB", ub[0])
    if error := find(r"Error.*", lines):
        return Outcome("unsupported", error[0], reason=unsupported_reason(error[0]))
    return Outcome("unsupported", None, reason=f"crashed with exit status {status}")


def unsupported_reason(error: str) -> str:
    if stuck := re.match(r"Error while interpreting module(?: at: (.*))?$", error):
        where = f" at {code(operation_name(stuck[1]))}" if stuck[1] else ""
        return f"**interpreter**: failed{where}"
    if verifier := re.match(r"Error verifying input program: (.*)$", error):
        return f"**verifier**: {code(verifier[1])}"
    if parser := re.match(r"Error: \S+:\d+:\d+: error: (.*)$", error):
        return f"**parser**: {code(parser[1])}"
    return code(error)


def operation_name(operation: str) -> str:
    """
    >>> operation_name('%10 = "llvm.fcmp"(%7, %7) : (f32, f32) -> i1')
    'llvm.fcmp'
    >>> operation_name('"llvm.unreachable"() : () -> ()')
    'llvm.unreachable'
    """
    name = re.search(r'^(?:%\S+ = )?"?([\w.]+)', operation)
    return name[1] if name else operation


# Values, written the same way for llubi and veir-interpret


def integer(width: int, value: int) -> str:
    """
    >>> integer(8, 255), integer(8, -1), integer(8, 127)
    ('i8 -1', 'i8 -1', 'i8 127')
    """
    bits = value % (1 << width)
    return f"i{width} {bits - (1 << width) if bits >> (width - 1) else bits}"


def llubi_value(ret: str) -> str:
    """
    >>> [llubi_value(ret) for ret in ["void", "i32 poison", "i32 -1", "ptr %p"]]
    ['void', 'poison', 'i32 -1', 'ptr']
    """
    match ret.split():
        case ["void"]:
            return "void"
        case [_, "poison"]:
            return "poison"
        case ["ptr", *_]:
            return "ptr"
        case [type, value] if type[0] == "i" and type[1:].isdigit():
            return integer(int(type[1:]), int(value))
        case _:
            raise ValueError(f"cannot read the value llubi returned: {ret!r}")


def veir_value(output: str) -> str:
    """
    >>> [veir_value(output) for output in ["#[]", "#[poison]", "#[0xffffffff#32]"]]
    ['void', 'poison', 'i32 -1']
    """
    match output.removeprefix("#[").removesuffix("]").split(", "):
        case [""]:
            return "void"
        case ["poison"]:
            return "poison"
        case [element] if bits := re.fullmatch(r"0x([0-9a-fA-F]+)#(\d+)", element):
            return integer(int(bits[2]), int(bits[1], 16))
        case _:
            return output


# Verdicts


class Verdict(StrEnum):
    PASS = "PASS"
    MISMATCH = "MISMATCH"
    UNSUPPORTED = "UNSUPPORTED"
    TIMEOUT = "TIMEOUT"


def verdict(llubi: Outcome, veir: Outcome) -> Verdict:
    if veir.kind == "unsupported":
        return Verdict.UNSUPPORTED
    if veir.kind == "timeout":
        return Verdict.TIMEOUT
    # Pointers are never compared: their addresses depend on the allocator.
    same_kind = llubi.kind == veir.kind
    same_value = llubi.value in (veir.value, "ptr")
    return Verdict.PASS if same_kind and same_value else Verdict.MISMATCH


@dataclass(frozen=True, slots=True)
class Test:
    name: str
    llubi: Outcome
    veir: Outcome

    @property
    def verdict(self) -> Verdict:
        return verdict(self.llubi, self.veir)


def test(directory: Path, llubi_trace: Path) -> Test:
    name = str(llubi_trace.relative_to(directory)).removesuffix(".llubi-output.txt")
    veir_trace = directory / f"{name}.veir-output.txt"
    try:
        llubi = llubi_outcome(llubi_trace.read_text())
    except ValueError as error:
        raise ValueError(f"{llubi_trace}: {error}") from error
    return Test(name, llubi, veir_outcome(veir_trace.read_text()))


def tests(corpus: Path) -> list[Test]:
    directory = corpus / "llubi-tests"
    return [
        test(directory, path) for path in sorted(directory.rglob("*.llubi-output.txt"))
    ]


# Rendering


def code(text: str) -> str:
    return f"`{text.replace('`', "'").replace('|', '\\|')}`"


def file_name(test: Test) -> str:
    return f"`{test.name}.ll`"


def describe(outcome: Outcome) -> str:
    if outcome.kind == "returned":
        return f"returned `{outcome.value}`"
    if outcome.line is not None:
        return code(outcome.line)
    return outcome.reason or outcome.kind


def results_table(tests: list[Test]) -> list[str]:
    return [
        "| Test | llubi | veir-interpret | Verdict |",
        "|---|---|---|---|",
        *(
            f"| {file_name(t)} | {describe(t.llubi)} | {describe(t.veir)} | {t.verdict} |"
            for t in tests
        ),
    ]


def unsupported_table(tests: list[Test]) -> list[str]:
    by_reason: defaultdict[str, list[str]] = defaultdict(list)
    for t in tests:
        if t.verdict is Verdict.UNSUPPORTED:
            by_reason[t.veir.reason or "unknown"].append(file_name(t))
    ranked = sorted(by_reason.items(), key=lambda item: -len(item[1]))
    return [
        "| Reason | Count | Tests |",
        "|---|---:|---|",
        *(
            f"| {reason} | {len(names)} | {', '.join(names)} |"
            for reason, names in ranked
        ),
    ]


def verdict_table(counts: Counter[Verdict]) -> list[str]:
    total = counts.total()
    return [
        "| Verdict | Tests |",
        "|---|---:|",
        *(f"| {v} | {counts[v]} ({100 * counts[v] / total:.1f}%) |" for v in Verdict),
    ]


def manifest_table(manifest: list[tuple[str, str, str]]) -> list[str]:
    return [
        "| Component | Version | SHA-256 |",
        "|---|---|---|",
        *(f"| {name} | {version} | `{digest}` |" for name, version, digest in manifest),
    ]


def render(tests: list[Test], manifest: list[tuple[str, str, str]]) -> str:
    counts = Counter(t.verdict for t in tests)
    mismatches = [t for t in tests if t.verdict is Verdict.MISMATCH]
    lines = [
        "# Veir-Interpreter Scoreboard",
        "",
        f"We run `veir-interpret` on the {len(tests)} tests in `llubi-tests` and compare with the",
        "results of `llubi`.",
        "",
        *verdict_table(counts),
    ]
    if mismatches:
        lines += [
            "",
            "## Mismatches",
            "",
            "`veir-interpret` fully executed these tests, but has a different result than `llubi`!",
            "",
            *results_table(mismatches),
        ]
    if counts[Verdict.UNSUPPORTED]:
        lines += [
            "",
            "## Unsupported",
            "",
            *unsupported_table(tests),
        ]
    lines += [
        "",
        "## All tests",
        "",
        "<details>",
        "<summary>Show all tests</summary>",
        "",
        *results_table(tests),
        "",
        "</details>",
        "",
        "## Manifest",
        "",
        *manifest_table(manifest),
    ]
    return "\n".join(lines) + "\n"


def read_manifest(
    veir_dir: Path, veir_interpret: Path, corpus_manifest: Path
) -> list[tuple[str, str, str]]:
    def git(*arguments: str) -> str:
        command = ["git", "-C", str(veir_dir), *arguments]
        return subprocess.run(
            command, capture_output=True, text=True, check=True
        ).stdout

    commit = git("rev-parse", "HEAD").strip()
    revision = f"[`{commit[:12]}`]({VEIR_REPOSITORY}/commit/{commit})"
    if git("status", "--porcelain", "--untracked-files=no"):
        revision += " with local changes"
    recorded = json.loads(corpus_manifest.read_text())
    return [
        ("veir-interpret", revision, sha256(veir_interpret)),
        *(
            (name, tool["version"], tool["sha256"])
            for name, tool in recorded["toolchain"].items()
        ),
        ("corpus.tar.gz", "", recorded["archive_sha256"]),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--veir-dir", type=Path, required=True)
    parser.add_argument("--veir-interpret", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        text = render(
            tests(args.corpus),
            read_manifest(args.veir_dir, args.veir_interpret, args.manifest),
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    args.output.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
