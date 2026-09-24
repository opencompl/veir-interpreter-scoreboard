# LLVM UB-aware Interpreter (llubi) Test Suite

The `.ll` files in `clean/` and `ub/` are copied verbatim from LLVM's `llubi`
regression tests:
https://github.com/llvm/llvm-project/tree/main/llvm/test/tools/llubi

They are distributed under the Apache License v2.0 with LLVM Exceptions (see
`llvm/LICENSE.TXT` upstream). The `; RUN:` and `; CHECK` lines are kept for
reference but are not used here: every test is run with plain
`llubi --verbose`, so all of them are scored under the same settings.

- `clean/`: `main` returns normally.
- `ub/`: `main` triggers undefined behavior that `llubi` reports.

## Not imported

Upstream tests whose result would not say anything about `veir-interpret` are not
part of this directory. Tests that show a feature `veir-interpret` lacks are kept.

Examples for omitted tests:
- `ub/verify.c`; Reason: Deliberately invalid IR
- `clean/lib_cxx_memory`; Reason: Calls foreign functions
- ...
