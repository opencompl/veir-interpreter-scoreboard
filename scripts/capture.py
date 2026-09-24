#!/usr/bin/env python3
"""Run a command and save its output, followed by `Exit status: N` (or `TIMEOUT`)."""

import argparse
import subprocess
from pathlib import Path

EXIT_STATUS = "Exit status: "
TIMEOUT = "TIMEOUT"


def capture(command: list[str], timeout: float | None) -> str:
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            timeout=timeout,
            check=False,
        )
        output, status = result.stdout, str(result.returncode)
    except subprocess.TimeoutExpired as expired:
        # Always bytes, even with `text=True`.
        output, status = (expired.stdout or b"").decode(errors="replace"), TIMEOUT
    if output and not output.endswith("\n"):
        output += "\n"
    return f"{output}{EXIT_STATUS}{status}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=float)
    parser.add_argument("command", nargs="+")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(capture(args.command, args.timeout_seconds))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
