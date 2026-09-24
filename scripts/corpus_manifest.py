#!/usr/bin/env python3
"""Record or check the toolchain and SHA-256 of corpus.tar.gz in manifest.json."""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 2


def sha256(path: Path) -> str:
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def version(command: str) -> str:
    """The first line of `command --version` that mentions a version."""
    result = subprocess.run(
        [command, "--version"], capture_output=True, text=True, check=False
    )
    for line in result.stdout.splitlines():
        if "version" in line.lower():
            return line.strip()
    raise ValueError(f"cannot determine the version of {command}")


def executable(command: str) -> Path:
    """The file that runs for `command`, with symlinks resolved."""
    path = shutil.which(command)
    if path is None:
        raise ValueError(f"cannot find {command}")
    return Path(path).resolve()


def manifest(archive: Path, tools: dict[str, str]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "archive_sha256": sha256(archive),
        "toolchain": {
            name: {"version": version(command), "sha256": sha256(executable(command))}
            for name, command in tools.items()
        },
    }


def check(archive: Path, manifest_path: Path) -> None:
    recorded: Any = json.loads(manifest_path.read_text())
    if recorded.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"{manifest_path} is from another corpus schema")
    if recorded.get("archive_sha256") != sha256(archive):
        raise ValueError(f"{archive} differs from the one in {manifest_path}")


def tool(argument: str) -> tuple[str, str]:
    """
    >>> tool("llubi=/usr/bin/llubi"), tool("llubi")
    (('llubi', '/usr/bin/llubi'), ('llubi', 'llubi'))
    """
    name, _, command = argument.partition("=")
    return name, command or name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    manifest_command = commands.add_parser("manifest")
    manifest_command.add_argument("--archive", type=Path, required=True)
    manifest_command.add_argument("--manifest", type=Path, required=True)
    manifest_command.add_argument(
        "--tool", type=tool, action="append", default=[], metavar="NAME=COMMAND"
    )
    check_command = commands.add_parser("check")
    check_command.add_argument("--archive", type=Path, required=True)
    check_command.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "manifest":
            data = manifest(args.archive, dict(args.tool))
            args.manifest.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        else:
            check(args.archive, args.manifest)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
