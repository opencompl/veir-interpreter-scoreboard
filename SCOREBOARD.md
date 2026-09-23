# VeIR execution scoreboard

Whole-program SQLite-and-harness O3 corpus with cached LLVM entry counts.

| Profile | Functions executed | `veir-interpret` functions executed | Status | Completion |
|---|---:|---:|---|---:|
| `minimal-harnesses/alloca.c` | 1 | 0 | FAILED | 0.0% |
| `minimal-harnesses/call.c` | 2 | 0 | FAILED | 0.0% |
| `minimal-harnesses/global.c` | 1 | 0 | FAILED | 0.0% |
| `minimal-harnesses/minimal-main.c` | 1 | 0 | SUCCESS | 0.0% |
| `sqlite-harnesses/initialize.c` | 18 | 0 | FAILED | 0.0% |
| `sqlite-harnesses/malloc1.c` | 15 | 0 | FAILED | 0.0% |
| `sqlite-harnesses/open_close.c` | 34 | 0 | FAILED | 0.0% |
| `sqlite-harnesses/select1.c` | 84 | 0 | FAILED | 0.0% |
| `sqlite-harnesses/version.c` | 1 | 0 | FAILED | 0.0% |

## Details

<details>
<summary>Per-function execution counts</summary>

### `minimal-harnesses/alloca.c`

| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |
|---|---:|---:|
| `main` | 1 | 0 |

### `minimal-harnesses/call.c`

| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |
|---|---:|---:|
| `answer` | 1 | 0 |
| `main` | 1 | 0 |

### `minimal-harnesses/global.c`

| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |
|---|---:|---:|
| `main` | 1 | 0 |

### `minimal-harnesses/minimal-main.c`

| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |
|---|---:|---:|
| `main` | 1 | 0 |

### `sqlite-harnesses/initialize.c`

| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |
|---|---:|---:|
| `llvm-link;pcache1Init` | 1 | 0 |
| `llvm-link;pcache1Shutdown` | 1 | 0 |
| `llvm-link;pthreadMutexAlloc` | 1 | 0 |
| `llvm-link;pthreadMutexEnd` | 1 | 0 |
| `llvm-link;pthreadMutexEnter` | 35 | 0 |
| `llvm-link;pthreadMutexFree` | 1 | 0 |
| `llvm-link;pthreadMutexInit` | 8 | 0 |
| `llvm-link;pthreadMutexLeave` | 35 | 0 |
| `llvm-link;sqlite3MemFree` | 2 | 0 |
| `llvm-link;sqlite3MemInit` | 1 | 0 |
| `llvm-link;sqlite3MemMalloc` | 2 | 0 |
| `llvm-link;sqlite3MemRoundup` | 2 | 0 |
| `llvm-link;sqlite3MemShutdown` | 1 | 0 |
| `llvm-link;sqlite3MemSize` | 4 | 0 |
| `llvm-link;sqlite3MemdbInit` | 3 | 0 |
| `main` | 1 | 0 |
| `sqlite3_reset_auto_extension` | 1 | 0 |
| `sqlite3_shutdown` | 1 | 0 |

### `sqlite-harnesses/malloc1.c`

| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |
|---|---:|---:|
| `llvm-link;pcache1Init` | 1 | 0 |
| `llvm-link;pthreadMutexAlloc` | 1 | 0 |
| `llvm-link;pthreadMutexEnter` | 36 | 0 |
| `llvm-link;pthreadMutexFree` | 1 | 0 |
| `llvm-link;pthreadMutexInit` | 8 | 0 |
| `llvm-link;pthreadMutexLeave` | 36 | 0 |
| `llvm-link;sqlite3MemFree` | 3 | 0 |
| `llvm-link;sqlite3MemInit` | 1 | 0 |
| `llvm-link;sqlite3MemMalloc` | 3 | 0 |
| `llvm-link;sqlite3MemRoundup` | 3 | 0 |
| `llvm-link;sqlite3MemSize` | 6 | 0 |
| `llvm-link;sqlite3MemdbInit` | 3 | 0 |
| `main` | 1 | 0 |
| `sqlite3_free` | 1 | 0 |
| `sqlite3_malloc` | 1 | 0 |

### `sqlite-harnesses/open_close.c`

| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |
|---|---:|---:|
| `llvm-link;btreeEnterAll` | 1 | 0 |
| `llvm-link;createCollation` | 24 | 0 |
| `llvm-link;functionDestroy` | 1 | 0 |
| `llvm-link;pcache1Cachesize` | 2 | 0 |
| `llvm-link;pcache1Create` | 1 | 0 |
| `llvm-link;pcache1Free` | 2 | 0 |
| `llvm-link;pcache1Init` | 1 | 0 |
| `llvm-link;pcache1Truncate` | 1 | 0 |
| `llvm-link;pthreadMutexAlloc` | 2 | 0 |
| `llvm-link;pthreadMutexEnter` | 91 | 0 |
| `llvm-link;pthreadMutexFree` | 2 | 0 |
| `llvm-link;pthreadMutexInit` | 8 | 0 |
| `llvm-link;pthreadMutexLeave` | 91 | 0 |
| `llvm-link;sqlite3BitvecDestroy` | 1 | 0 |
| `llvm-link;sqlite3BtreeEnter` | 1 | 0 |
| `llvm-link;sqlite3BtreeRollback` | 2 | 0 |
| `llvm-link;sqlite3DbFreeNN` | 5 | 0 |
| `llvm-link;sqlite3DbMallocRawNN` | 4 | 0 |
| `llvm-link;sqlite3FindCollSeq` | 24 | 0 |
| `llvm-link;sqlite3FindFunction` | 12 | 0 |
| `llvm-link;sqlite3HashClear` | 9 | 0 |
| `llvm-link;sqlite3HashInsert` | 18 | 0 |
| `llvm-link;sqlite3MemFree` | 25 | 0 |
| `llvm-link;sqlite3MemInit` | 1 | 0 |
| `llvm-link;sqlite3MemMalloc` | 25 | 0 |
| `llvm-link;sqlite3MemRoundup` | 25 | 0 |
| `llvm-link;sqlite3MemSize` | 53 | 0 |
| `llvm-link;sqlite3MemdbInit` | 3 | 0 |
| `llvm-link;sqlite3WalClose` | 1 | 0 |
| `llvm-link;strAccumFinishRealloc` | 1 | 0 |
| `sqlite3_close` | 1 | 0 |
| `sqlite3_free` | 1 | 0 |
| `sqlite3_mprintf` | 1 | 0 |
| `sqlite3_open` | 1 | 0 |

### `sqlite-harnesses/select1.c`

| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |
|---|---:|---:|
| `llvm-link;btreeEnterAll` | 1 | 0 |
| `llvm-link;countOfViewOptimization` | 2 | 0 |
| `llvm-link;createCollation` | 24 | 0 |
| `llvm-link;estLog` | 3 | 0 |
| `llvm-link;exprListDeleteNN` | 2 | 0 |
| `llvm-link;functionDestroy` | 1 | 0 |
| `llvm-link;growOp3` | 2 | 0 |
| `llvm-link;pagerUnlockAndRollback` | 1 | 0 |
| `llvm-link;pcache1Cachesize` | 3 | 0 |
| `llvm-link;pcache1Create` | 1 | 0 |
| `llvm-link;pcache1Free` | 2 | 0 |
| `llvm-link;pcache1Init` | 1 | 0 |
| `llvm-link;pcache1Truncate` | 1 | 0 |
| `llvm-link;pthreadMutexAlloc` | 2 | 0 |
| `llvm-link;pthreadMutexEnter` | 150 | 0 |
| `llvm-link;pthreadMutexFree` | 2 | 0 |
| `llvm-link;pthreadMutexInit` | 8 | 0 |
| `llvm-link;pthreadMutexLeave` | 150 | 0 |
| `llvm-link;resolveExprStep` | 26 | 0 |
| `llvm-link;resolveOrderGroupBy` | 5 | 0 |
| `llvm-link;resolveSelectStep` | 1 | 0 |
| `llvm-link;selectAddSubqueryTypeInfo` | 1 | 0 |
| `llvm-link;sqlite3AddColumn` | 38 | 0 |
| `llvm-link;sqlite3BitvecDestroy` | 2 | 0 |
| `llvm-link;sqlite3BtreeEnter` | 1 | 0 |
| `llvm-link;sqlite3BtreeRollback` | 2 | 0 |
| `llvm-link;sqlite3Close` | 2 | 0 |
| `llvm-link;sqlite3ColumnDefault` | 5 | 0 |
| `llvm-link;sqlite3DbFreeNN` | 24 | 0 |
| `llvm-link;sqlite3DbMallocRawNN` | 22 | 0 |
| `llvm-link;sqlite3ExprCodeExprList` | 6 | 0 |
| `llvm-link;sqlite3ExprCodeGetColumn` | 5 | 0 |
| `llvm-link;sqlite3ExprInt32` | 1 | 0 |
| `llvm-link;sqlite3ExprListAppend` | 2 | 0 |
| `llvm-link;sqlite3ExprListAppendGrow` | 1 | 0 |
| `llvm-link;sqlite3ExprListAppendNew` | 4 | 0 |
| `llvm-link;sqlite3ExprListSetSortOrder` | 1 | 0 |
| `llvm-link;sqlite3ExprWalkNoop` | 14 | 0 |
| `llvm-link;sqlite3FindCollSeq` | 24 | 0 |
| `llvm-link;sqlite3FindFunction` | 12 | 0 |
| `llvm-link;sqlite3FindIndex` | 29 | 0 |
| `llvm-link;sqlite3FindTable` | 52 | 0 |
| `llvm-link;sqlite3HashClear` | 7 | 0 |
| `llvm-link;sqlite3HashInsert` | 47 | 0 |
| `llvm-link;sqlite3KeyInfoUnref` | 1 | 0 |
| `llvm-link;sqlite3MPrintf` | 1 | 0 |
| `llvm-link;sqlite3MemFree` | 46 | 0 |
| `llvm-link;sqlite3MemInit` | 1 | 0 |
| `llvm-link;sqlite3MemMalloc` | 46 | 0 |
| `llvm-link;sqlite3MemRealloc` | 8 | 0 |
| `llvm-link;sqlite3MemRoundup` | 54 | 0 |
| `llvm-link;sqlite3MemSize` | 113 | 0 |
| `llvm-link;sqlite3MemdbInit` | 3 | 0 |
| `llvm-link;sqlite3PcacheRelease` | 1 | 0 |
| `llvm-link;sqlite3Realloc` | 8 | 0 |
| `llvm-link;sqlite3ResolveExprNames` | 1 | 0 |
| `llvm-link;sqlite3RunParser` | 8 | 0 |
| `llvm-link;sqlite3SelectNew` | 2 | 0 |
| `llvm-link;sqlite3SelectPrep` | 2 | 0 |
| `llvm-link;sqlite3SelectWalkNoop` | 2 | 0 |
| `llvm-link;sqlite3ShadowTableName` | 2 | 0 |
| `llvm-link;sqlite3SrcListDelete` | 1 | 0 |
| `llvm-link;sqlite3VdbeChangeToNoop` | 1 | 0 |
| `llvm-link;sqlite3VdbeExplain` | 1 | 0 |
| `llvm-link;sqlite3VdbeResolveLabel` | 2 | 0 |
| `llvm-link;sqlite3VdbeSetNumCols` | 2 | 0 |
| `llvm-link;sqlite3WalClose` | 1 | 0 |
| `llvm-link;sqlite3WalkExpr` | 12 | 0 |
| `llvm-link;sqlite3WalkExprNN` | 15 | 0 |
| `llvm-link;sqlite3WalkSelect` | 2 | 0 |
| `llvm-link;sqlite3WhereExplainOneScan` | 1 | 0 |
| `llvm-link;strAccumFinishRealloc` | 2 | 0 |
| `llvm-link;vdbeFreeOpArray` | 19 | 0 |
| `llvm-link;whereLoopAddBtreeIndex` | 3 | 0 |
| `llvm-link;whereLoopClearUnion` | 4 | 0 |
| `main` | 1 | 0 |
| `sqlite3_close` | 1 | 0 |
| `sqlite3_column_int` | 1 | 0 |
| `sqlite3_finalize` | 3 | 0 |
| `sqlite3_free` | 1 | 0 |
| `sqlite3_mprintf` | 1 | 0 |
| `sqlite3_open` | 1 | 0 |
| `sqlite3_prepare_v2` | 1 | 0 |
| `sqlite3_strnicmp` | 13 | 0 |

### `sqlite-harnesses/version.c`

| Function | Times executed (LLVM binary) | Times executed (`veir-interpret`) |
|---|---:|---:|
| `main` | 1 | 0 |

</details>

## Provenance

| Field | Value |
|---|---|
| VeIR | `9462999134b6a14054981efafc460e2607cf47d7` |
| VeIR source | `<omitted>/veir-interpreter-scoreboard/veir` |
| `veir-interpret` SHA-256 | `1207c36d1da814fa6c204bccfc6fda0c39a92fedc10b71111a28fcefa71adb02` |
| C flags | `-O3 -fno-vectorize -fno-slp-vectorize` |
| Scored | `2026-09-23 13:22 UTC` |
| Host | `Linux x86_64` |
