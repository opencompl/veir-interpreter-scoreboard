#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import cast

from make_config import (
    cflags,
    clang,
    llvm_link,
    llvm_profdata,
    mlir_opt,
    mlir_translate,
    opt,
)

SCHEMA_VERSION = 1


def sha256(path: Path) -> str:
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def json_object(value: object, name: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"invalid manifest {name}")
    items = cast(dict[object, object], value)
    if not all(isinstance(key, str) for key in items):
        raise ValueError(f"invalid manifest {name}")
    return cast(dict[str, object], items)


def tool_version(command: str) -> str:
    result = subprocess.run(
        [command, "--version"], capture_output=True, check=False, text=True
    )
    if result.returncode:
        raise ValueError(f"{command} --version failed: {result.stderr.strip()}")
    lines = [
        line.strip() for line in result.stdout.splitlines() if "version" in line.lower()
    ]
    if not lines:
        raise ValueError(
            f"{command} --version did not report a version: {result.stdout.strip()}"
        )
    return lines[0]


def manifest_data(archive: Path) -> dict[str, object]:
    archive_digest = sha256(archive)
    compiler = clang()
    target = subprocess.run(
        [compiler, "-dumpmachine"], capture_output=True, check=False, text=True
    )
    if target.returncode or not target.stdout.strip():
        raise ValueError(f"{compiler} -dumpmachine failed: {target.stderr.strip()}")
    return {
        "schema_version": SCHEMA_VERSION,
        "cflags": cflags(),
        "archive_sha256": archive_digest,
        "toolchain": {
            "clang": tool_version(compiler),
            "llvm-link": tool_version(llvm_link()),
            "opt": tool_version(opt()),
            "mlir-translate": tool_version(mlir_translate()),
            "mlir-opt": tool_version(mlir_opt()),
            "llvm-profdata": tool_version(llvm_profdata()),
            "target": target.stdout.strip(),
        },
    }


def validate(archive: Path, manifest_path: Path) -> None:
    try:
        raw: object = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read {manifest_path}: {error}") from error
    manifest = json_object(raw, "root")
    if (
        manifest.get("schema_version") != SCHEMA_VERSION
        or manifest.get("cflags") != cflags()
    ):
        raise ValueError("manifest does not describe the required O3 corpus")
    if manifest.get("archive_sha256") != sha256(archive):
        raise ValueError("corpus archive differs from the manifest")


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("manifest", "check"):
        child = commands.add_parser(name)
        child.add_argument("--archive", type=Path, required=True)
        child.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "manifest":
            args.manifest.write_text(
                json.dumps(manifest_data(args.archive), indent=2, sort_keys=True) + "\n"
            )
        else:
            validate(args.archive, args.manifest)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
