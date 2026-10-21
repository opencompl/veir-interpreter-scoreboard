#!/usr/bin/env python3
"""Compare the veir-interpret, llubi and alive-exec outputs in the corpus and write SCOREBOARD.md.

llubi and alive-exec are read with VeIR's `Tools/vsmith`, as VeIR's own
`Tools/llubi-interpret` and `Tools/alive-interpret` do. It writes their results
as veir-interpret prints its own, so all three compare as text.

The results are also written as JSON, so that the next run can list what changed.
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from types import ModuleType
from typing import Any

from capture import EXIT_STATUS, TIMEOUT
from corpus_manifest import sha256

VEIR_REPOSITORY = "https://github.com/opencompl/veir"
SCOREBOARD_REPOSITORY = "https://github.com/opencompl/veir-interpreter-scoreboard"
UB = "Undefined behavior"
VOID = "Program output: #[]"

# Outcomes


@dataclass(frozen=True, slots=True)
class Outcome:
    result: str | None  # As veir-interpret prints it; None if the tool gave none.
    detail: str = ""  # Markdown: where the UB is, or why there is no result.


@dataclass(frozen=True, slots=True)
class Stop:
    """Why veir-interpret gave no result."""

    operation: str  # Markdown: the operation it stopped at, or **parser**, ...
    why: str = ""  # Markdown: the types of that operation, or a message.

    def __str__(self) -> str:
        return f"{self.operation}: {self.why}" if self.why else self.operation


def find(pattern: str, lines: Iterable[str]) -> re.Match[str] | None:
    """The first line that matches `pattern`, if any."""
    return next(filter(None, (re.fullmatch(pattern, line) for line in lines)), None)


def exit_status(lines: list[str]) -> str:
    return lines[-1].removeprefix(EXIT_STATUS)


def crashed(trace: str) -> bool:
    # As in `Tools/llubi-interpret` and `Tools/alive-interpret`.
    status = exit_status(trace.splitlines())
    return status.startswith("-") or status in ("134", "139") or "Stack dump:" in trace


def load_vsmith(veir_dir: Path) -> ModuleType:
    loader = SourceFileLoader("vsmith", str(veir_dir / "Tools" / "vsmith"))
    spec = spec_from_loader("vsmith", loader)
    assert spec is not None
    # `dataclass` looks up the module of the class it decorates.
    vsmith = sys.modules["vsmith"] = module_from_spec(spec)
    loader.exec_module(vsmith)
    return vsmith


def main_trace(trace: str) -> str:
    """
    llubi's trace without the calls that `main` returned from, so that their
    `ret` cannot be mistaken for the one of `main`.

    >>> main_trace("Entering function: main\\nEntering function: f\\n  ret i8 1\\n"
    ...            "Exiting function: f\\n  ret i8 2\\nExiting function: main")
    'Entering function: main\\n  ret i8 2\\nExiting function: main'
    """
    kept: list[str] = []
    calls: list[int] = []
    for line in trace.splitlines():
        if line.startswith("Entering function:"):
            calls.append(len(kept))
        kept.append(line)
        if line.startswith("Exiting function:") and len(calls) > 1:
            del kept[calls.pop() :]
    return "\n".join(kept)


def llubi_outcome(trace: str, source: str, vsmith: ModuleType) -> Outcome:
    if crashed(trace):
        return Outcome(None, "crashed")
    try:
        result, _ = vsmith.classify_llubi_output(main_trace(trace))
    except ValueError:
        return Outcome(None, "no recognizable result")
    if result != UB:
        return Outcome(result)
    lines = trace.splitlines()
    # The innermost frame of the stack trace is the instruction with UB.
    frame = find(r"#0 .*:(\d+)", lines)
    where = f" at [line {frame[1]}]({source}#L{frame[1]})" if frame else ""
    message = find(r".*Immediate UB detected: (.*)", lines)
    return Outcome(UB, f"UB{where}" + (f": {plain(message[1])}" if message else ""))


def alive_outcome(trace: str, vsmith: ModuleType) -> Outcome:
    if exit_status(trace.splitlines()) == TIMEOUT:
        return Outcome(None, "timeout")
    # As in `Tools/alive-interpret`.
    if "Severe Z3 error" in trace:
        return Outcome(None, "failed: `Severe Z3 error`")
    error = r"^(?:Internal )?ERROR: (?!program returned poison)(.*)$"
    if rejected := re.search(error, trace, re.MULTILINE):
        return Outcome(None, f"rejected: {code(rejected[1].strip())}")
    if crashed(trace):
        return Outcome(None, "crashed")
    declared = re.search(r"^define (.+?) @main\(", trace, re.MULTILINE)
    return_type = declared[1] if declared else None
    try:
        result, _ = vsmith.classify_alive_exec_output(trace, return_type)
    except ValueError:
        return Outcome(None, "no recognizable result")
    if result != UB:
        return Outcome(result)
    # An instruction without a name, such as a call, is `<void>`.
    instruction = find(r"(\S+) = UB triggered!", trace.splitlines())
    if instruction and instruction[1] != "<void>":
        return Outcome(UB, f"UB at {code(instruction[1])}")
    return Outcome(UB, "UB")


# `<file>:<line>:<col>: error: <message>` (or `note:`), then the line it is about.
DIAGNOSTIC = re.compile(r"^\S+:\d+:(\d+): (?:error|note): (.*)\n(.*)$", re.MULTILINE)


def veir_outcome(trace: str) -> Outcome | Stop:
    lines = trace.splitlines()
    status = exit_status(lines)
    if status == TIMEOUT:
        return Stop("**timeout**")
    if status == "0" and (output := find(r"Program output: .*", lines)):
        return Outcome(output[0])
    diagnostic = DIAGNOSTIC.search(trace)
    if status == "0" and find(UB, lines):
        if diagnostic:
            return Outcome(UB, f"UB at {code(operation_name(diagnostic[3].strip()))}")
        return Outcome(UB, "UB")
    if verifier := find(r"Error verifying input program: ([\w.]+): (.*)", lines):
        return Stop(code(verifier[1]), f"verifier says {code(verifier[2])}")
    if diagnostic:
        return diagnostic_stop(int(diagnostic[1]), diagnostic[2], diagnostic[3])
    if error := find(r"(?:error|Error): (.*)", lines):
        return Stop("**other**", code(error[1]))
    return Stop("**crash**", f"exit status {status}")


def diagnostic_stop(column: int, message: str, line: str) -> Stop:
    if message == "failed to interpret operation":
        operation = line.strip()
        types = operation.rpartition(" : ")[2]
        return Stop(code(operation_name(operation)), code(types))
    return Stop("**parser**", f"{code(message)} at {code(token_at(line, column))}")


def operation_name(operation: str) -> str:
    """
    >>> operation_name('%10 = "llvm.fcmp"(%7, %7) : (f32, f32) -> i1')
    'llvm.fcmp'
    >>> operation_name('"llvm.unreachable"() : () -> ()')
    'llvm.unreachable'
    """
    name = re.search(r'^(?:%\S+ = )?"?([\w.]+)', operation)
    return name[1] if name else operation


def token_at(line: str, column: int) -> str:
    """
    The text between spaces at `column`, counted from 1, as a diagnostic points at it.

    >>> token_at('  %2 = "llvm.inttoptr"(%0) : (i64) -> !llvm.ptr<1>', 40)
    '!llvm.ptr<1>'
    >>> token_at('  %3 = "llvm.getelementptr" <{elem_type = vector<[4]xi32>, a}>', 43)
    'vector<[4]xi32>'
    """
    start = line.rfind(" ", 0, column - 1) + 1
    end = line.find(" ", column - 1)
    return line[start : end if end >= 0 else None].rstrip(",")


def readable(output: str) -> str:
    """
    >>> readable("Program output: #[]")
    'void'
    >>> readable("Program output: #[0xffffffff#32, poison, ptr]")
    'i32 -1, poison, ptr'
    """
    values = output.removeprefix("Program output: #[").removesuffix("]")
    return ", ".join(map(readable_value, values.split(", "))) if values else "void"


def readable_value(value: str) -> str:
    if bits := re.fullmatch(r"0x([0-9a-fA-F]+)#(\d+)", value):
        width, unsigned = int(bits[2]), int(bits[1], 16)
        signed = unsigned - (1 << width) if unsigned >> (width - 1) else unsigned
        return f"i{width} {signed}"
    return value


# Tests


REFERENCES = ("llubi", "alive-exec")


@dataclass(frozen=True, slots=True)
class Test:
    name: str
    references: tuple[Outcome, Outcome]  # In the order of `REFERENCES`.
    veir: Outcome | Stop

    @property
    def finished(self) -> bool:
        """Whether veir-interpret ran the test to a result."""
        return isinstance(self.veir, Outcome)

    def agrees(self, reference: Outcome) -> bool | None:
        """Whether both have the same result; None if one has none."""
        if not isinstance(self.veir, Outcome) or reference.result is None:
            return None
        return reference.result == self.veir.result

    def only_void(self, reference: Outcome) -> bool:
        """Whether both agree on nothing but `main` returning void."""
        return bool(self.agrees(reference)) and reference.result == VOID


def test(directory: Path, name: str, vsmith: ModuleType) -> Test:
    def trace(tool: str) -> str:
        return (directory / f"{name}.{tool}-output.txt").read_text()

    return Test(
        name,
        (
            llubi_outcome(trace("llubi"), source(name), vsmith),
            alive_outcome(trace("alive-exec"), vsmith),
        ),
        veir_outcome(trace("veir")),
    )


def tests(corpus: Path, vsmith: ModuleType) -> list[Test]:
    directory = corpus / "llubi-tests"
    return [
        test(directory, str(path.relative_to(directory)).removesuffix(".mlir"), vsmith)
        for path in sorted(directory.rglob("*.mlir"))
    ]


type Group = tuple[str, list[Test]]


def stops(tests: list[Test]) -> list[tuple[str, list[Group]]]:
    """Where veir-interpret stopped, by operation and then why; most tests first."""
    by_operation: defaultdict[str, defaultdict[str, list[Test]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for t in tests:
        if isinstance(t.veir, Stop):
            by_operation[t.veir.operation][t.veir.why].append(t)

    def ranked(groups: dict[str, list[Test]]) -> list[Group]:
        return sorted(groups.items(), key=lambda group: -len(group[1]))

    operations = [(operation, ranked(whys)) for operation, whys in by_operation.items()]
    return sorted(operations, key=lambda item: -sum(len(t) for _, t in item[1]))


# Results, and how they changed since the previous run


def results(tests: list[Test], veir_commit: str) -> dict[str, Any]:
    return {
        "veir": veir_commit,
        "tests": {
            t.name: {
                "finished": t.finished,
                "agrees": dict(
                    zip(REFERENCES, map(t.agrees, t.references), strict=True)
                ),
            }
            for t in tests
        },
    }


def changes(previous: dict[str, Any], tests: list[Test]) -> list[str]:
    lines: list[str] = []
    for t in tests:
        if (before := previous["tests"].get(t.name)) is None:
            continue
        if t.finished and not before["finished"]:
            lines.append(f"- 🟢 {link(t)} now runs to a result")
        if before["finished"] and not t.finished:
            lines.append(
                f"- 🔴 {link(t)} no longer runs to a result ({describe(t.veir)})"
            )
        for name, reference in zip(REFERENCES, t.references, strict=True):
            agrees, agreed = t.agrees(reference), before["agrees"].get(name)
            if agrees and not agreed:
                lines.append(f"- 🟢 {link(t)} now agrees with `{name}`")
            if agreed and not agrees:
                lines.append(f"- 🔴 {link(t)} no longer agrees with `{name}`")
    return lines


# Rendering


def code(text: str) -> str:
    return f"`{text.replace('`', "'").replace('|', '\\|')}`"


def plain(text: str) -> str:
    return text.replace("|", "\\|")


def source(name: str) -> str:
    return f"llubi-tests/{name}.ll"


def link(test: Test) -> str:
    return f"[`{test.name}.ll`]({source(test.name)})"


def row(cells: Iterable[str]) -> str:
    return f"| {' | '.join(cells)} |"


def describe(outcome: Outcome | Stop) -> str:
    if isinstance(outcome, Stop):
        return str(outcome)
    if outcome.result is None or outcome.result == UB:
        return outcome.detail
    return f"returned {code(readable(outcome.result))}"


def judge(test: Test, reference: Outcome) -> str:
    """The reference's result, marked with whether veir-interpret agrees."""
    if test.only_void(reference):
        mark = "⚪ "
    else:
        mark = {True: "✅ ", False: "❌ ", None: ""}[test.agrees(reference)]
    return mark + describe(reference)


def agreement(tests: list[Test], i: int) -> tuple[str, str]:
    """
    Of the tests that have both results, how many agree with reference `i`, and
    how many of those only on `void`, if any.
    """
    answered = [t for t in tests if t.agrees(t.references[i]) is not None]
    agreeing = sum(bool(t.agrees(t.references[i])) for t in answered)
    only_void = sum(t.only_void(t.references[i]) for t in answered)
    return (
        f"{agreeing}/{len(answered)}",
        f"{only_void} only on `void`" if only_void else "",
    )


def headline(tests: list[Test]) -> str:
    finished = [t for t in tests if t.finished]
    parts = [f"**{len(finished)}/{len(tests)}** tests run to a result"]
    for i, name in enumerate(REFERENCES):
        count, note = agreement(finished, i)
        parts.append(
            f"**{count}** agree with `{name}`" + (f" ({note})" if note else "")
        )
    return " · ".join(parts)


def summary_table(tests: list[Test]) -> list[str]:
    groups = [
        (
            "`clean/`, which return normally",
            [t for t in tests if t.name.startswith("clean/")],
        ),
        ("`ub/`, which trigger UB", [t for t in tests if t.name.startswith("ub/")]),
        ("All", tests),
    ]
    return [
        row(
            [
                "Tests",
                "Run to a result",
                *(f"Agree with `{name}`" for name in REFERENCES),
            ]
        ),
        row(["--", "-:", *(["-:"] * len(REFERENCES))]),
        *(
            row(
                [
                    label,
                    f"{sum(t.finished for t in group)}/{len(group)}",
                    *(
                        ", ".join(filter(None, agreement(group, i)))
                        for i in range(len(REFERENCES))
                    ),
                ]
            )
            for label, group in groups
        ),
    ]


def tests_table(tests: list[Test]) -> list[str]:
    return [
        row(["Test", "veir-interpret", *REFERENCES]),
        row(["--"] * (2 + len(REFERENCES))),
        *(
            row([link(t), describe(t.veir), *(judge(t, r) for r in t.references)])
            for t in tests
        ),
    ]


def whys(groups: list[Group], count: int = 3) -> str:
    """
    >>> whys([("`() -> f32`", [None, None]), ("`() -> i1`", [None])], count=1)
    '`() -> f32` ×2, …'
    """
    shown = [why + (f" ×{len(t)}" if len(t) > 1 else "") for why, t in groups if why]
    return ", ".join(shown[:count] + (["…"] if len(shown) > count else []))


def fix_next_table(stopped: list[tuple[str, list[Group]]], total: int) -> list[str]:
    return [
        "| # | Operation | Tests affected | Why |",
        "| -: | -- | -: | -- |",
        *(
            row(
                [
                    str(rank),
                    operation,
                    f"{sum(len(t) for _, t in groups)}/{total}",
                    whys(groups),
                ]
            )
            for rank, (operation, groups) in enumerate(stopped[:5], start=1)
        ),
    ]


def stops_table(stopped: list[tuple[str, list[Group]]]) -> list[str]:
    return [
        "| Operation | Why | Tests |",
        "| -- | -- | -- |",
        *(
            row([operation, why, ", ".join(map(link, group))])
            for operation, groups in stopped
            for why, group in groups
        ),
    ]


def manifest_table(manifest: list[tuple[str, str, str]]) -> list[str]:
    return [
        "| Component | Version | SHA-256 |",
        "| -- | -- | -- |",
        *(f"| {name} | {version} | `{digest}` |" for name, version, digest in manifest),
    ]


def render(
    tests: list[Test],
    manifest: list[tuple[str, str, str]],
    previous: tuple[str, dict[str, Any]] | None,
) -> str:
    mismatches = [t for t in tests if False in map(t.agrees, t.references)]
    stopped = stops(tests)
    lines = [
        "# Veir-Interpreter Scoreboard",
        "",
        "We run `veir-interpret` on the tests in `llubi-tests` and compare its results with",
        "`llubi` and Alive2's `alive-exec`, read the way VeIR's `Tools/llubi-interpret` and",
        "`Tools/alive-interpret` read them. See [README.md](README.md).",
        "",
        headline(tests),
        "",
        *summary_table(tests),
        "",
        "Agreement counts the tests that have both results. A test that only returns `void`",
        "agrees trivially (⚪): llubi's own tests check the values in between, which",
        "`veir-interpret` does not print.",
    ]
    if previous:
        commit, before = previous
        run = f"[previous run]({SCOREBOARD_REPOSITORY}/blob/{commit}/SCOREBOARD.md)"
        lines += [
            "",
            "## Since the previous run",
            "",
            f"Compared with the {run} (`{commit[:12]}`, VeIR `{before['veir'][:12]}`).",
            "",
            *(changes(before, tests) or ["Nothing changed."]),
        ]
    if mismatches:
        lines += [
            "",
            "## Mismatches",
            "",
            "`veir-interpret` ran these tests to a different result than `llubi` or `alive-exec`.",
            "",
            *tests_table(mismatches),
        ]
    if stopped:
        lines += [
            "",
            "## Fix next",
            "",
            "The operations `veir-interpret` stops at in the most tests, and why: their types,",
            "or what the verifier or parser says. The collapsed table below lists all of them.",
            "",
            *fix_next_table(stopped, len(tests)),
            "",
            "<details>",
            f"<summary>All operations `veir-interpret` stops at ({len(stopped)}), with their tests</summary>",
            "",
            *stops_table(stopped),
            "",
            "</details>",
        ]
    lines += [
        "",
        "## Tests",
        "",
        "✅, ⚪ and ❌ mark whether `veir-interpret` has the same result as `llubi` and `alive-exec`.",
        "",
        "<details>",
        f"<summary>All {len(tests)} tests, those with a result first</summary>",
        "",
        *tests_table(sorted(tests, key=lambda t: not t.finished)),
        "",
        "</details>",
        "",
        "## Manifest",
        "",
        *manifest_table(manifest),
    ]
    return "\n".join(lines) + "\n"


def git(directory: Path, *arguments: str) -> str:
    command = ["git", "-C", str(directory), *arguments]
    return subprocess.run(command, capture_output=True, text=True, check=True).stdout


def previous_run(results_path: Path) -> tuple[str, dict[str, Any]] | None:
    """The commit of this repository and the results it holds, if it holds any."""
    try:
        commit = git(Path(), "rev-parse", "HEAD").strip()
        return commit, json.loads(git(Path(), "show", f"HEAD:./{results_path}"))
    except subprocess.CalledProcessError:
        return None


def read_manifest(
    veir_dir: Path, veir_interpret: Path, corpus_manifest: Path
) -> list[tuple[str, str, str]]:
    commit = git(veir_dir, "rev-parse", "HEAD").strip()
    revision = f"[`{commit[:12]}`]({VEIR_REPOSITORY}/commit/{commit})"
    if git(veir_dir, "status", "--porcelain", "--untracked-files=no"):
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
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()
    try:
        scored = tests(args.corpus, load_vsmith(args.veir_dir))
        manifest = read_manifest(args.veir_dir, args.veir_interpret, args.manifest)
        text = render(scored, manifest, previous_run(args.results))
        veir_commit = git(args.veir_dir, "rev-parse", "HEAD").strip()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    args.output.write_text(text)
    args.results.write_text(json.dumps(results(scored, veir_commit), indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
