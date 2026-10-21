#!/usr/bin/env python3
"""Compare the veir-interpret, llubi and alive-exec outputs in the corpus and write SCOREBOARD.md.

llubi and alive-exec are read with VeIR's `Tools/vsmith`, as VeIR's own
`Tools/llubi-interpret` and `Tools/alive-interpret` do. It writes their results
as veir-interpret prints its own, so all three compare as text.
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

from capture import EXIT_STATUS, TIMEOUT
from corpus_manifest import sha256

VEIR_REPOSITORY = "https://github.com/opencompl/veir"
UB = "Undefined behavior"

# Outcomes


@dataclass(frozen=True, slots=True)
class Outcome:
    result: str | None  # As veir-interpret prints it; None if the tool gave none.
    detail: str  # What the tool printed about `result`, or why there is none.
    timeout: bool = False


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


def classified(result: tuple[str, str]) -> Outcome:
    output, value = result
    return Outcome(output, code(value))


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


def llubi_outcome(trace: str, vsmith: ModuleType) -> Outcome:
    if crashed(trace):
        return Outcome(None, "crashed")
    try:
        return classified(vsmith.classify_llubi_output(main_trace(trace)))
    except ValueError:
        return Outcome(None, "no recognizable result")


def alive_outcome(trace: str, vsmith: ModuleType) -> Outcome:
    if exit_status(trace.splitlines()) == TIMEOUT:
        return Outcome(None, "timeout", timeout=True)
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
        return classified(vsmith.classify_alive_exec_output(trace, return_type))
    except ValueError:
        return Outcome(None, "no recognizable result")


# `<file>:<line>:<col>: error: <message>` (or `note:`), then the operation it is about.
DIAGNOSTIC = re.compile(r"^\S+:(\d+):\d+: (?:error|note): (.*)\n\s*(.*)$", re.MULTILINE)


def veir_outcome(trace: str) -> Outcome:
    lines = trace.splitlines()
    status = exit_status(lines)
    if status == TIMEOUT:
        return Outcome(None, "timeout", timeout=True)
    if status == "0" and (output := find(r"Program output: .*", lines)):
        return Outcome(output[0], code(output[0]))
    diagnostic = DIAGNOSTIC.search(trace)
    if status == "0" and find(UB, lines):
        if diagnostic:
            return Outcome(UB, f"UB at {code(diagnostic[3])} (line {diagnostic[1]})")
        return Outcome(UB, code(UB))
    if verifier := find(r"Error verifying input program: (.*)", lines):
        return Outcome(None, f"**verifier**: {code(verifier[1])}")
    if diagnostic:
        return Outcome(None, diagnostic_reason(diagnostic[2], diagnostic[3]))
    if error := find(r"(?:error|Error): (.*)", lines):
        return Outcome(None, f"**interpreter**: {code(error[1])}")
    return Outcome(None, f"crashed with exit status {status}")


def diagnostic_reason(message: str, operation: str) -> str:
    if message == "failed to interpret operation":
        return f"**interpreter**: failed at {code(operation_name(operation))}"
    return f"**parser**: {code(message)}"


def operation_name(operation: str) -> str:
    """
    >>> operation_name('%10 = "llvm.fcmp"(%7, %7) : (f32, f32) -> i1')
    'llvm.fcmp'
    >>> operation_name('"llvm.unreachable"() : () -> ()')
    'llvm.unreachable'
    """
    name = re.search(r'^(?:%\S+ = )?"?([\w.]+)', operation)
    return name[1] if name else operation


# Tests


REFERENCES = ("llubi", "alive-exec")


@dataclass(frozen=True, slots=True)
class Test:
    name: str
    references: tuple[Outcome, Outcome]  # In the order of `REFERENCES`.
    veir: Outcome

    @property
    def finished(self) -> bool:
        """Whether veir-interpret ran the test to a result."""
        return self.veir.result is not None

    def agrees(self, reference: Outcome) -> bool | None:
        """Whether both have the same result; None if one has none."""
        if not self.finished or reference.result is None:
            return None
        return reference.result == self.veir.result


def test(directory: Path, name: str, vsmith: ModuleType) -> Test:
    def trace(tool: str) -> str:
        return (directory / f"{name}.{tool}-output.txt").read_text()

    return Test(
        name,
        (
            llubi_outcome(trace("llubi"), vsmith),
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


# Rendering


def code(text: str) -> str:
    return f"`{text.replace('`', "'").replace('|', '\\|')}`"


def file_name(test: Test) -> str:
    return f"`{test.name}.ll`"


def describe(outcome: Outcome) -> str:
    if outcome.result in (None, UB):
        return outcome.detail
    return code(outcome.result)


def judge(test: Test, reference: Outcome) -> str:
    """The reference's result, marked with whether veir-interpret agrees."""
    mark = {True: "✅ ", False: "❌ ", None: ""}[test.agrees(reference)]
    return mark + describe(reference)


def headline(tests: list[Test]) -> str:
    finished = [t for t in tests if t.finished]
    parts = [f"**{len(finished)}/{len(tests)}** tests run to a result"]
    for i, name in enumerate(REFERENCES):
        answered = [t for t in finished if t.agrees(t.references[i]) is not None]
        agreeing = [t for t in answered if t.agrees(t.references[i])]
        part = f"**{len(agreeing)}/{len(answered)}** of those agree with `{name}`"
        if missing := len(finished) - len(answered):
            part += f" ({missing} where `{name}` has no result)"
        parts.append(part)
    if timeouts := sum(t.veir.timeout for t in tests):
        parts.append(f"**{timeouts}** time out")
    return " · ".join(parts)


def row(cells: Iterable[str]) -> str:
    return f"| {' | '.join(cells)} |"


def tests_table(tests: list[Test]) -> list[str]:
    return [
        row(["Test", "veir-interpret", *REFERENCES]),
        row(["--"] * (2 + len(REFERENCES))),
        *(
            row([file_name(t), describe(t.veir), *(judge(t, r) for r in t.references)])
            for t in tests
        ),
    ]


def stop_reasons(tests: list[Test]) -> list[tuple[str, list[Test]]]:
    """Why veir-interpret gave no result, most common first."""
    by_reason: defaultdict[str, list[Test]] = defaultdict(list)
    for t in tests:
        if not t.finished and not t.veir.timeout:
            by_reason[t.veir.detail].append(t)
    return sorted(by_reason.items(), key=lambda item: -len(item[1]))


def fix_next_table(
    reasons: list[tuple[str, list[Test]]], total: int, count: int = 5
) -> list[str]:
    return [
        "| # | Reason | Tests affected |",
        "| -: | -- | -: |",
        *(
            f"| {rank} | {reason} | {len(stopped)}/{total} |"
            for rank, (reason, stopped) in enumerate(reasons[:count], start=1)
        ),
    ]


def reasons_table(reasons: list[tuple[str, list[Test]]]) -> list[str]:
    return [
        "| Reason | Tests |",
        "| -- | -- |",
        *(
            f"| {reason} | {', '.join(map(file_name, stopped))} |"
            for reason, stopped in reasons
        ),
    ]


def manifest_table(manifest: list[tuple[str, str, str]]) -> list[str]:
    return [
        "| Component | Version | SHA-256 |",
        "| -- | -- | -- |",
        *(f"| {name} | {version} | `{digest}` |" for name, version, digest in manifest),
    ]


def render(tests: list[Test], manifest: list[tuple[str, str, str]]) -> str:
    mismatches = [t for t in tests if False in map(t.agrees, t.references)]
    reasons = stop_reasons(tests)
    lines = [
        "# Veir-Interpreter Scoreboard",
        "",
        "We run `veir-interpret` on the tests in `llubi-tests` and compare its results with",
        "`llubi` and Alive2's `alive-exec`, read the way VeIR's `Tools/llubi-interpret` and",
        "`Tools/alive-interpret` read them. See [README.md](README.md).",
        "",
        headline(tests),
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
    if reasons:
        lines += [
            "",
            "## Fix next",
            "",
            "Why `veir-interpret` gives no result, for the most tests. The collapsed table below",
            "lists every reason, with its tests.",
            "",
            *fix_next_table(reasons, len(tests)),
            "",
            "<details>",
            f"<summary>All reasons ({len(reasons)}), with their tests</summary>",
            "",
            *reasons_table(reasons),
            "",
            "</details>",
        ]
    lines += [
        "",
        "## Tests",
        "",
        "✅ and ❌ mark whether `veir-interpret` has the same result as `llubi` and `alive-exec`.",
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
            tests(args.corpus, load_vsmith(args.veir_dir)),
            read_manifest(args.veir_dir, args.veir_interpret, args.manifest),
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    args.output.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
