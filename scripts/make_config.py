#!/usr/bin/env python3
from __future__ import annotations

import shlex
import subprocess
from functools import cache
from pathlib import Path

REQUIRED_KEYS = {
    "clang",
    "llvm_link",
    "opt",
    "mlir_translate",
    "mlir_opt",
    "llvm_profdata",
    "cflags",
    "harnesses",
}


@cache
def make_config() -> dict[str, list[str]]:
    result = subprocess.run(
        ["make", "--no-print-directory", "print-python-config"],
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(f"make print-python-config failed: {result.stderr.strip()}")
    config: dict[str, list[str]] = {}
    for line in result.stdout.splitlines():
        key, separator, value = line.partition("=")
        if not separator:
            raise RuntimeError("make print-python-config returned invalid output")
        config[key] = shlex.split(value)
    missing = REQUIRED_KEYS - config.keys()
    if missing:
        raise RuntimeError(
            f"make print-python-config omitted: {', '.join(sorted(missing))}"
        )
    return config


def _tool(key: str) -> str:
    values = make_config()[key]
    if len(values) != 1:
        raise RuntimeError(f"make print-python-config returned invalid {key}")
    return values[0]


def clang() -> str:
    return _tool("clang")


def llvm_link() -> str:
    return _tool("llvm_link")


def opt() -> str:
    return _tool("opt")


def mlir_translate() -> str:
    return _tool("mlir_translate")


def mlir_opt() -> str:
    return _tool("mlir_opt")


def llvm_profdata() -> str:
    return _tool("llvm_profdata")


def cflags() -> list[str]:
    return make_config()["cflags"]


def harnesses() -> list[Path]:
    return [Path(path) for path in make_config()["harnesses"]]
