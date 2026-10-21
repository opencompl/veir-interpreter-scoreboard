# Veir-Interpreter Scoreboard

Like the [veir-sqlite](https://github.com/opencompl/veir-sqlite) scoreboard, but for `veir-interpret`.
This compares `veir-interpret` with [`llubi`](https://llvm.org/docs/CommandGuide/llubi.html) (LLVM UB-aware Interpreter) using selected tests from `llubi`'s test-suite.
It also compares with Alive2's `alive-exec`.
Both are read the way VeIR's own cross-checks read them (`Tools/llubi-interpret`, `Tools/alive-interpret`).

## Updating the Scoreboard

Updating `SCOREBOARD.md` requires only `uv`, `lake` and a local VeIR checkout used for the scoring.

``` bash
make check-corpus # Optional
VEIR_DIR=veir make scoreboard --jobs <N>
```

Next to it, `results.json` keeps each test's results, so that the next run can list what changed.

GitHub Actions does this automatically: [`scoreboard.yml`](.github/workflows/scoreboard.yml) polls VeIR's `main` every five minutes and commits a new `SCOREBOARD.md` whenever it has moved.

The tests in `llubi-tests` are taken from LLVM's `llubi` test suite.
The tests in `clean` return normally, the ones in `ub` trigger undefined behavior.

MLIR files, `llubi` and `alive-exec` outputs require a full LLVM/MLIR toolchain to generate. They are therefore cached and stored in `corpus.tar.gz`.

## Updating the Corpus

The Nix development shell is derived from VeIR's Nix flake.
The following commands regenerate the corpus with the toolchain provided by upstream VeIR:

```bash
nix flake update
nix develop
make refresh-corpus ALIVE_EXEC=<path to alive-exec>
```

`alive-exec` is not part of the Nix shell; build it from [Alive2](https://github.com/AliveToolkit/alive2).

The generated files are not reproducible between different toolchains / architectures!
`make refresh-corpus` records the toolchain that produced the corpus, plus a SHA-256 of `corpus.tar.gz`, in `manifest.json`.
