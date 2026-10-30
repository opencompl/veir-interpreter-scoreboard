# Veir-Interpreter Scoreboard

We run `veir-interpret` on the tests in `llubi-tests` and compare its results with
`llubi` and Alive2's `alive-exec`, read the way VeIR's `Tools/llubi-interpret` and
`Tools/alive-interpret` read them. See [README.md](README.md).

**20/102** tests run to a result · **15/20** agree with `llubi` (3 only on `void`) · **8/13** agree with `alive-exec`

| Tests | Run to a result | Agree with `llubi` | Agree with `alive-exec` |
| -- | -: | -: | -: |
| `clean/`, which return normally | 4/50 | 4/4, 3 only on `void` | 1/1 |
| `ub/`, which trigger UB | 16/52 | 11/16 | 7/12 |
| All | 20/102 | 15/20, 3 only on `void` | 8/13 |

Agreement counts the tests that have both results. A test that only returns `void`
agrees trivially (⚪): llubi's own tests check the values in between, which
`veir-interpret` does not print.

## Since the previous run

Compared with the [previous run](https://github.com/opencompl/veir-interpreter-scoreboard/blob/1f1b172e928d01a4dddd6f014b826bb8e5e4d4e1/SCOREBOARD.md) (`1f1b172e928d`, VeIR `d0f3382c6ab7`).

Nothing changed.

## Mismatches

`veir-interpret` ran these tests to a different result than `llubi` or `alive-exec`.

| Test | veir-interpret | llubi | alive-exec |
| -- | -- | -- | -- |
| [`ub/global_constant_store.ll`](llubi-tests/ub/global_constant_store.ll) | returned `void` | ❌ UB at [line 6](llubi-tests/ub/global_constant_store.ll#L6): Try to write to a constant memory object: ptr 0x8 [@constant]. | ❌ UB at `store` |
| [`ub/inttoptr_gep.ll`](llubi-tests/ub/inttoptr_gep.ll) | returned `void` | ❌ UB at [line 23](llubi-tests/ub/inttoptr_gep.ll#L23): Invalid memory access via a pointer with nullary provenance. | ❌ UB at `%gep_oob` |
| [`ub/load_noundef_ub_poison.ll`](llubi-tests/ub/load_noundef_ub_poison.ll) | returned `void` | ❌ UB at [line 7](llubi-tests/ub/load_noundef_ub_poison.ll#L7): The value loaded contains undefined bits. | ❌ UB at `assume` |
| [`ub/load_noundef_ub_undef.ll`](llubi-tests/ub/load_noundef_ub_undef.ll) | returned `void` | ❌ UB at [line 7](llubi-tests/ub/load_noundef_ub_undef.ll#L7): The value loaded contains undefined bits. | ❌ UB at `assume` |
| [`ub/metadata_noundef_ub.ll`](llubi-tests/ub/metadata_noundef_ub.ll) | returned `void` | ❌ UB at [line 7](llubi-tests/ub/metadata_noundef_ub.ll#L7): The value poison violates !noundef metadata. | ❌ UB at `assume` |

## Fix next

The operations `veir-interpret` stops at in the most tests, and why: their types,
or what the verifier or parser says. The collapsed table below lists all of them.

| # | Operation | Tests affected | Why |
| -: | -- | -: | -- |
| 1 | `llvm.call` | 20/102 | `(!llvm.ptr) -> ()` ×16, `() -> i32`, `() -> i16`, … |
| 2 | `llvm.intr.assume` | 12/102 | `(i1, !llvm.ptr, i32) -> ()` ×3, `(i1, !llvm.ptr) -> ()` ×2, `(i1) -> ()` ×2, … |
| 3 | `llvm.mlir.constant` | 7/102 | `() -> vector<2xi32>` ×2, `() -> vector<4xi32>` ×2, `() -> vector<4xi1>`, … |
| 4 | `llvm.fadd` | 7/102 | verifier says `Expected operand 0 to have floating point type` ×6, `(f32, f32) -> f32` |
| 5 | `llvm.mlir.poison` | 4/102 | `() -> f32` ×3, `() -> !llvm.struct<(i32, i32)>` |

<details>
<summary>All operations `veir-interpret` stops at (26), with their tests</summary>

| Operation | Why | Tests |
| -- | -- | -- |
| `llvm.call` | `(!llvm.ptr) -> ()` | [`clean/byval.ll`](llubi-tests/clean/byval.ll), [`ub/attribute_dereferenceable_ub_nullary_provenance.ll`](llubi-tests/ub/attribute_dereferenceable_ub_nullary_provenance.ll), [`ub/attribute_dereferenceable_ub_oob1.ll`](llubi-tests/ub/attribute_dereferenceable_ub_oob1.ll), [`ub/attribute_dereferenceable_ub_oob2.ll`](llubi-tests/ub/attribute_dereferenceable_ub_oob2.ll), [`ub/attribute_dereferenceable_ub_oob3.ll`](llubi-tests/ub/attribute_dereferenceable_ub_oob3.ll), [`ub/attribute_dereferenceable_ub_poison.ll`](llubi-tests/ub/attribute_dereferenceable_ub_poison.ll), [`ub/byval_misalign.ll`](llubi-tests/ub/byval_misalign.ll), [`ub/byval_misalign_callsite.ll`](llubi-tests/ub/byval_misalign_callsite.ll), [`ub/byval_mismatch1.ll`](llubi-tests/ub/byval_mismatch1.ll), [`ub/byval_mismatch2.ll`](llubi-tests/ub/byval_mismatch2.ll), [`ub/byval_mismatch3.ll`](llubi-tests/ub/byval_mismatch3.ll), [`ub/byval_null.ll`](llubi-tests/ub/byval_null.ll), [`ub/byval_oversize.ll`](llubi-tests/ub/byval_oversize.ll), [`ub/byval_poison.ll`](llubi-tests/ub/byval_poison.ll), [`ub/call_mismatched_signature.ll`](llubi-tests/ub/call_mismatched_signature.ll), [`ub/call_poison.ll`](llubi-tests/ub/call_poison.ll) |
| `llvm.call` | `() -> i32` | [`clean/alloca.ll`](llubi-tests/clean/alloca.ll) |
| `llvm.call` | `() -> i16` | [`clean/reset_return_value_slot.ll`](llubi-tests/clean/reset_return_value_slot.ll) |
| `llvm.call` | `(i32) -> ()` | [`ub/attribute_noundef_ub.ll`](llubi-tests/ub/attribute_noundef_ub.ll) |
| `llvm.call` | `(!llvm.ptr) -> !llvm.ptr` | [`ub/byval_lifetime.ll`](llubi-tests/ub/byval_lifetime.ll) |
| `llvm.intr.assume` | `(i1, !llvm.ptr, i32) -> ()` | [`ub/assume_misalign.ll`](llubi-tests/ub/assume_misalign.ll), [`ub/assume_nondereferenceable.ll`](llubi-tests/ub/assume_nondereferenceable.ll), [`ub/assume_poison_align.ll`](llubi-tests/ub/assume_poison_align.ll) |
| `llvm.intr.assume` | `(i1, !llvm.ptr) -> ()` | [`clean/assume_operand_bundles.ll`](llubi-tests/clean/assume_operand_bundles.ll), [`ub/assume_null.ll`](llubi-tests/ub/assume_null.ll) |
| `llvm.intr.assume` | `(i1) -> ()` | [`ub/assume_false.ll`](llubi-tests/ub/assume_false.ll), [`ub/assume_poison.ll`](llubi-tests/ub/assume_poison.ll) |
| `llvm.intr.assume` | `(i1, !llvm.ptr, i32, i32) -> ()` | [`ub/assume_non_pow2_align_offset.ll`](llubi-tests/ub/assume_non_pow2_align_offset.ll), [`ub/assume_pow2_align_offset.ll`](llubi-tests/ub/assume_pow2_align_offset.ll) |
| `llvm.intr.assume` | `(i1, !llvm.ptr, i64) -> ()` | [`ub/assume_invalid_align.ll`](llubi-tests/ub/assume_invalid_align.ll) |
| `llvm.intr.assume` | `(i1, !llvm.ptr<1>, i32) -> ()` | [`ub/assume_misalign_all_ones.ll`](llubi-tests/ub/assume_misalign_all_ones.ll) |
| `llvm.intr.assume` | `(i1, !llvm.ptr<1>) -> ()` | [`ub/assume_null_all_ones.ll`](llubi-tests/ub/assume_null_all_ones.ll) |
| `llvm.mlir.constant` | `() -> vector<2xi32>` | [`clean/bitcast_be.ll`](llubi-tests/clean/bitcast_be.ll), [`clean/bitcast_le.ll`](llubi-tests/clean/bitcast_le.ll) |
| `llvm.mlir.constant` | `() -> vector<4xi32>` | [`clean/intr_vector_reduce.ll`](llubi-tests/clean/intr_vector_reduce.ll), [`clean/loadstore_overaligned.ll`](llubi-tests/clean/loadstore_overaligned.ll) |
| `llvm.mlir.constant` | `() -> vector<4xi1>` | [`clean/intr_experimental_vector.ll`](llubi-tests/clean/intr_experimental_vector.ll) |
| `llvm.mlir.constant` | `() -> vector<6xi32>` | [`clean/intr_vector_manip.ll`](llubi-tests/clean/intr_vector_manip.ll) |
| `llvm.mlir.constant` | `() -> vector<8xi32>` | [`clean/metadata.ll`](llubi-tests/clean/metadata.ll) |
| `llvm.fadd` | verifier says `Expected operand 0 to have floating point type` | [`clean/fp_arith_bfloat.ll`](llubi-tests/clean/fp_arith_bfloat.ll), [`clean/fp_arith_double.ll`](llubi-tests/clean/fp_arith_double.ll), [`clean/fp_arith_float.ll`](llubi-tests/clean/fp_arith_float.ll), [`clean/fp_arith_fp128.ll`](llubi-tests/clean/fp_arith_fp128.ll), [`clean/fp_arith_fp80.ll`](llubi-tests/clean/fp_arith_fp80.ll), [`clean/fp_arith_half.ll`](llubi-tests/clean/fp_arith_half.ll) |
| `llvm.fadd` | `(f32, f32) -> f32` | [`clean/fp_denorm.ll`](llubi-tests/clean/fp_denorm.ll) |
| `llvm.mlir.poison` | `() -> f32` | [`clean/intr_fp_fptoi_sat.ll`](llubi-tests/clean/intr_fp_fptoi_sat.ll), [`clean/intr_fp_is_fpclass.ll`](llubi-tests/clean/intr_fp_is_fpclass.ll), [`clean/intr_fp_minmax.ll`](llubi-tests/clean/intr_fp_minmax.ll) |
| `llvm.mlir.poison` | `() -> !llvm.struct<(i32, i32)>` | [`clean/struct.ll`](llubi-tests/clean/struct.ll) |
| **parser** | `vector element type expected` at `vector<[4]xi32>` | [`clean/gep.ll`](llubi-tests/clean/gep.ll), [`clean/vector.ll`](llubi-tests/clean/vector.ll) |
| **parser** | `vector element type expected` at `vector<[2]x!llvm.ptr>` | [`clean/global_constexpr_initializer.ll`](llubi-tests/clean/global_constexpr_initializer.ll) |
| `llvm.add` | verifier says `Expected operand 0 to have integer type` | [`clean/int_arith.ll`](llubi-tests/clean/int_arith.ll), [`clean/inttoptr_ptrtoint_constantexpr.ll`](llubi-tests/clean/inttoptr_ptrtoint_constantexpr.ll), [`clean/undef.ll`](llubi-tests/clean/undef.ll) |
| `llvm.mlir.undef` | `() -> vector<2xi32>` | [`clean/intr_arith_overflow.ll`](llubi-tests/clean/intr_arith_overflow.ll) |
| `llvm.mlir.undef` | `() -> !llvm.struct<(i32, i32)>` | [`ub/attribute_noundef_agg_ub.ll`](llubi-tests/ub/attribute_noundef_agg_ub.ll) |
| `llvm.mlir.undef` | `() -> vector<2xi4>` | [`ub/load_noundef_ub_poison_padding.ll`](llubi-tests/ub/load_noundef_ub_poison_padding.ll) |
| **other** | `unsupported value of global @g` | [`clean/byval_padding.ll`](llubi-tests/clean/byval_padding.ll) |
| **other** | `unsupported value of global @constant_dst` | [`ub/intr_memory_constant_ub.ll`](llubi-tests/ub/intr_memory_constant_ub.ll) |
| `llvm.fdiv` | `(f32, f32) -> f32` | [`clean/fp_fastmath.ll`](llubi-tests/clean/fp_fastmath.ll), [`clean/fp_phi_select.ll`](llubi-tests/clean/fp_phi_select.ll) |
| `llvm.inttoptr` | `(i8) -> !llvm.ptr` | [`clean/inttoptr.ll`](llubi-tests/clean/inttoptr.ll) |
| `llvm.inttoptr` | verifier says `Expected the pointer side to have !llvm.ptr type` | [`clean/ptrtoaddr.ll`](llubi-tests/clean/ptrtoaddr.ll) |
| `llvm.ptrtoaddr` | `(!llvm.ptr) -> i64` | [`clean/ptrtoaddr_after_ptrtoint.ll`](llubi-tests/clean/ptrtoaddr_after_ptrtoint.ll), [`ub/ptrtoaddr_no_expose.ll`](llubi-tests/ub/ptrtoaddr_no_expose.ll) |
| `llvm.intr.lifetime.start` | `(!llvm.ptr) -> ()` | [`ub/store_dead.ll`](llubi-tests/ub/store_dead.ll), [`ub/store_dead_gep.ll`](llubi-tests/ub/store_dead_gep.ll) |
| `llvm.sitofp` | verifier says `Expected operand 0 to have integer type` | [`clean/fp_cast.ll`](llubi-tests/clean/fp_cast.ll) |
| `llvm.fcmp` | `(f32, f32) -> i1` | [`clean/fp_cmp.ll`](llubi-tests/clean/fp_cmp.ll) |
| `llvm.icmp` | verifier says `Expected operand 0 to have integer or pointer type` | [`clean/icmp_ptr.ll`](llubi-tests/clean/icmp_ptr.ll) |
| `llvm.intr.sadd.sat` | verifier says `Expected operand 0 to have integer type` | [`clean/intr_arith_sat.ll`](llubi-tests/clean/intr_arith_sat.ll) |
| `llvm.intr.bitreverse` | verifier says `Expected operand 0 to have integer type` | [`clean/intr_bit_manip.ll`](llubi-tests/clean/intr_bit_manip.ll) |
| `llvm.intr.fmuladd` | verifier says `Expected operand 0 to have floating point type` | [`clean/intr_fp_fma.ll`](llubi-tests/clean/intr_fp_fma.ll) |
| `llvm.intr.fabs` | verifier says `Expected operand 0 to have floating point type` | [`clean/intr_fp_unary.ll`](llubi-tests/clean/intr_fp_unary.ll) |
| `llvm.intr.abs` | verifier says `Expected operand 0 to have integer type` | [`clean/intr_int_arith.ll`](llubi-tests/clean/intr_int_arith.ll) |
| `llvm.intr.memset.inline` | `(!llvm.ptr, i8) -> ()` | [`clean/intr_memory.ll`](llubi-tests/clean/intr_memory.ll) |
| `llvm.intr.ssa.copy` | `(i32) -> i32` | [`clean/intr_passthrough.ll`](llubi-tests/clean/intr_passthrough.ll) |
| `llvm.intr.vscale` | `() -> i32` | [`clean/intr_vscale.ll`](llubi-tests/clean/intr_vscale.ll) |
| `llvm.alloca` | `(i32) -> !llvm.ptr` | [`ub/alloca_poison_count.ll`](llubi-tests/ub/alloca_poison_count.ll) |
| `llvm.func` | verifier says `Expected the last operation of a block to be a terminator` | [`ub/indirectbr_poison.ll`](llubi-tests/ub/indirectbr_poison.ll) |

</details>

## Tests

✅, ⚪ and ❌ mark whether `veir-interpret` has the same result as `llubi` and `alive-exec`.

<details>
<summary>All 102 tests, those with a result first</summary>

| Test | veir-interpret | llubi | alive-exec |
| -- | -- | -- | -- |
| [`clean/gep-16-bit-addrspace.ll`](llubi-tests/clean/gep-16-bit-addrspace.ll) | returned `void` | ⚪ returned `void` | failed: `Severe Z3 error` |
| [`clean/global_external.ll`](llubi-tests/clean/global_external.ll) | returned `void` | ⚪ returned `void` | crashed |
| [`clean/main2.ll`](llubi-tests/clean/main2.ll) | returned `i32 0` | ✅ returned `i32 0` | ✅ returned `i32 0` |
| [`clean/noalias_scope.ll`](llubi-tests/clean/noalias_scope.ll) | returned `void` | ⚪ returned `void` | rejected: `Unsupported type: metadata` |
| [`ub/alloca_large_count.ll`](llubi-tests/ub/alloca_large_count.ll) | UB at `llvm.alloca` | ✅ UB at [line 5](llubi-tests/ub/alloca_large_count.ll#L5): Alloca with large array size that overflows uint64_t. Size: -1 | ✅ UB at `%alloc_dyn` |
| [`ub/alloca_size_overflow.ll`](llubi-tests/ub/alloca_size_overflow.ll) | UB at `llvm.alloca` | ✅ UB at [line 5](llubi-tests/ub/alloca_size_overflow.ll#L5): Alloca with allocation size that overflows uint64_t. Size: -1 | ✅ UB at `%alloc_dyn` |
| [`ub/br_poison.ll`](llubi-tests/ub/br_poison.ll) | UB at `llvm.cond_br` | ✅ UB at [line 6](llubi-tests/ub/br_poison.ll#L6): Branch on poison condition. | rejected: `Error in SMT solver: memout` |
| [`ub/global_constant_store.ll`](llubi-tests/ub/global_constant_store.ll) | returned `void` | ❌ UB at [line 6](llubi-tests/ub/global_constant_store.ll#L6): Try to write to a constant memory object: ptr 0x8 [@constant]. | ❌ UB at `store` |
| [`ub/inttoptr_generation.ll`](llubi-tests/ub/inttoptr_generation.ll) | UB at `llvm.store` | ✅ UB at [line 19](llubi-tests/ub/inttoptr_generation.ll#L19): Invalid memory access via a pointer with nullary provenance. | failed: `Severe Z3 error` |
| [`ub/inttoptr_generation2.ll`](llubi-tests/ub/inttoptr_generation2.ll) | UB at `llvm.store` | ✅ UB at [line 22](llubi-tests/ub/inttoptr_generation2.ll#L22): Invalid memory access via a pointer with nullary provenance. | failed: `Severe Z3 error` |
| [`ub/inttoptr_gep.ll`](llubi-tests/ub/inttoptr_gep.ll) | returned `void` | ❌ UB at [line 23](llubi-tests/ub/inttoptr_gep.ll#L23): Invalid memory access via a pointer with nullary provenance. | ❌ UB at `%gep_oob` |
| [`ub/inttoptr_multiobj.ll`](llubi-tests/ub/inttoptr_multiobj.ll) | UB at `llvm.store` | ✅ UB at [line 23](llubi-tests/ub/inttoptr_multiobj.ll#L23): Invalid memory access via a pointer with nullary provenance. | ✅ UB at `%gep2` |
| [`ub/inttoptr_multiobj2.ll`](llubi-tests/ub/inttoptr_multiobj2.ll) | UB at `llvm.store` | ✅ UB at [line 24](llubi-tests/ub/inttoptr_multiobj2.ll#L24): Invalid memory access via a pointer with nullary provenance. | ✅ UB at `%gep2` |
| [`ub/inttoptr_oob.ll`](llubi-tests/ub/inttoptr_oob.ll) | UB at `llvm.store` | ✅ UB at [line 16](llubi-tests/ub/inttoptr_oob.ll#L16): Invalid memory access via a pointer with nullary provenance. | ✅ UB at `%ptr_inbounds_resolved` |
| [`ub/inttoptr_oob2.ll`](llubi-tests/ub/inttoptr_oob2.ll) | UB at `llvm.store` | ✅ UB at [line 18](llubi-tests/ub/inttoptr_oob2.ll#L18): Invalid memory access via a pointer with nullary provenance. | ✅ UB at `%ptr_inbounds_resolved` |
| [`ub/load_noundef_ub_poison.ll`](llubi-tests/ub/load_noundef_ub_poison.ll) | returned `void` | ❌ UB at [line 7](llubi-tests/ub/load_noundef_ub_poison.ll#L7): The value loaded contains undefined bits. | ❌ UB at `assume` |
| [`ub/load_noundef_ub_undef.ll`](llubi-tests/ub/load_noundef_ub_undef.ll) | returned `void` | ❌ UB at [line 7](llubi-tests/ub/load_noundef_ub_undef.ll#L7): The value loaded contains undefined bits. | ❌ UB at `assume` |
| [`ub/metadata_noundef_ub.ll`](llubi-tests/ub/metadata_noundef_ub.ll) | returned `void` | ❌ UB at [line 7](llubi-tests/ub/metadata_noundef_ub.ll#L7): The value poison violates !noundef metadata. | ❌ UB at `assume` |
| [`ub/switch_poison.ll`](llubi-tests/ub/switch_poison.ll) | UB at `llvm.switch` | ✅ UB: Switch on poison condition. | rejected: `Error in SMT solver: memout` |
| [`ub/unreachable.ll`](llubi-tests/ub/unreachable.ll) | UB at `llvm.unreachable` | ✅ UB at [line 5](llubi-tests/ub/unreachable.ll#L5): Unreachable code. | ✅ UB at `assume` |
| [`clean/alloca.ll`](llubi-tests/clean/alloca.ll) | `llvm.call`: `() -> i32` | returned `void` | failed: `Severe Z3 error` |
| [`clean/assume_operand_bundles.ll`](llubi-tests/clean/assume_operand_bundles.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr) -> ()` | returned `void` | rejected: `Unsupported instruction:   call void @llvm.assume(i1 true) [ "dereferenceable_or_null"(ptr %alloc, i32 4)` |
| [`clean/bitcast_be.ll`](llubi-tests/clean/bitcast_be.ll) | `llvm.mlir.constant`: `() -> vector<2xi32>` | returned `void` | rejected: `Unsupported type: b64` |
| [`clean/bitcast_le.ll`](llubi-tests/clean/bitcast_le.ll) | `llvm.mlir.constant`: `() -> vector<2xi32>` | returned `void` | rejected: `Unsupported type: b64` |
| [`clean/byval.ll`](llubi-tests/clean/byval.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | returned `void` | UB |
| [`clean/byval_padding.ll`](llubi-tests/clean/byval_padding.ll) | **other**: `unsupported value of global @g` | returned `void` | crashed |
| [`clean/fp_arith_bfloat.ll`](llubi-tests/clean/fp_arith_bfloat.ll) | `llvm.fadd`: verifier says `Expected operand 0 to have floating point type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/fp_arith_double.ll`](llubi-tests/clean/fp_arith_double.ll) | `llvm.fadd`: verifier says `Expected operand 0 to have floating point type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/fp_arith_float.ll`](llubi-tests/clean/fp_arith_float.ll) | `llvm.fadd`: verifier says `Expected operand 0 to have floating point type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/fp_arith_fp128.ll`](llubi-tests/clean/fp_arith_fp128.ll) | `llvm.fadd`: verifier says `Expected operand 0 to have floating point type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/fp_arith_fp80.ll`](llubi-tests/clean/fp_arith_fp80.ll) | `llvm.fadd`: verifier says `Expected operand 0 to have floating point type` | returned `void` | rejected: `Unsupported type: x86_fp80` |
| [`clean/fp_arith_half.ll`](llubi-tests/clean/fp_arith_half.ll) | `llvm.fadd`: verifier says `Expected operand 0 to have floating point type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/fp_cast.ll`](llubi-tests/clean/fp_cast.ll) | `llvm.sitofp`: verifier says `Expected operand 0 to have integer type` | returned `void` | crashed |
| [`clean/fp_cmp.ll`](llubi-tests/clean/fp_cmp.ll) | `llvm.fcmp`: `(f32, f32) -> i1` | returned `void` | failed: `Severe Z3 error` |
| [`clean/fp_denorm.ll`](llubi-tests/clean/fp_denorm.ll) | `llvm.fadd`: `(f32, f32) -> f32` | returned `void` | failed: `Severe Z3 error` |
| [`clean/fp_fastmath.ll`](llubi-tests/clean/fp_fastmath.ll) | `llvm.fdiv`: `(f32, f32) -> f32` | returned `void` | failed: `Severe Z3 error` |
| [`clean/fp_phi_select.ll`](llubi-tests/clean/fp_phi_select.ll) | `llvm.fdiv`: `(f32, f32) -> f32` | returned `void` | failed: `Severe Z3 error` |
| [`clean/gep.ll`](llubi-tests/clean/gep.ll) | **parser**: `vector element type expected` at `vector<[4]xi32>` | returned `void` | failed: `Severe Z3 error` |
| [`clean/global_constexpr_initializer.ll`](llubi-tests/clean/global_constexpr_initializer.ll) | **parser**: `vector element type expected` at `vector<[2]x!llvm.ptr>` | returned `void` | rejected: `program doesn't type check!` |
| [`clean/icmp_ptr.ll`](llubi-tests/clean/icmp_ptr.ll) | `llvm.icmp`: verifier says `Expected operand 0 to have integer or pointer type` | returned `void` | crashed |
| [`clean/int_arith.ll`](llubi-tests/clean/int_arith.ll) | `llvm.add`: verifier says `Expected operand 0 to have integer type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_arith_overflow.ll`](llubi-tests/clean/intr_arith_overflow.ll) | `llvm.mlir.undef`: `() -> vector<2xi32>` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_arith_sat.ll`](llubi-tests/clean/intr_arith_sat.ll) | `llvm.intr.sadd.sat`: verifier says `Expected operand 0 to have integer type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_bit_manip.ll`](llubi-tests/clean/intr_bit_manip.ll) | `llvm.intr.bitreverse`: verifier says `Expected operand 0 to have integer type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_experimental_vector.ll`](llubi-tests/clean/intr_experimental_vector.ll) | `llvm.mlir.constant`: `() -> vector<4xi1>` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_fp_fma.ll`](llubi-tests/clean/intr_fp_fma.ll) | `llvm.intr.fmuladd`: verifier says `Expected operand 0 to have floating point type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_fp_fptoi_sat.ll`](llubi-tests/clean/intr_fp_fptoi_sat.ll) | `llvm.mlir.poison`: `() -> f32` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_fp_is_fpclass.ll`](llubi-tests/clean/intr_fp_is_fpclass.ll) | `llvm.mlir.poison`: `() -> f32` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_fp_minmax.ll`](llubi-tests/clean/intr_fp_minmax.ll) | `llvm.mlir.poison`: `() -> f32` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_fp_unary.ll`](llubi-tests/clean/intr_fp_unary.ll) | `llvm.intr.fabs`: verifier says `Expected operand 0 to have floating point type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_int_arith.ll`](llubi-tests/clean/intr_int_arith.ll) | `llvm.intr.abs`: verifier says `Expected operand 0 to have integer type` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_memory.ll`](llubi-tests/clean/intr_memory.ll) | `llvm.intr.memset.inline`: `(!llvm.ptr, i8) -> ()` | returned `void` | UB at `memcpy` |
| [`clean/intr_passthrough.ll`](llubi-tests/clean/intr_passthrough.ll) | `llvm.intr.ssa.copy`: `(i32) -> i32` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_vector_manip.ll`](llubi-tests/clean/intr_vector_manip.ll) | `llvm.mlir.constant`: `() -> vector<6xi32>` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_vector_reduce.ll`](llubi-tests/clean/intr_vector_reduce.ll) | `llvm.mlir.constant`: `() -> vector<4xi32>` | returned `void` | failed: `Severe Z3 error` |
| [`clean/intr_vscale.ll`](llubi-tests/clean/intr_vscale.ll) | `llvm.intr.vscale`: `() -> i32` | returned `void` | failed: `Severe Z3 error` |
| [`clean/inttoptr.ll`](llubi-tests/clean/inttoptr.ll) | `llvm.inttoptr`: `(i8) -> !llvm.ptr` | returned `void` | failed: `Severe Z3 error` |
| [`clean/inttoptr_ptrtoint_constantexpr.ll`](llubi-tests/clean/inttoptr_ptrtoint_constantexpr.ll) | `llvm.add`: verifier says `Expected operand 0 to have integer type` | returned `void` | crashed |
| [`clean/loadstore_overaligned.ll`](llubi-tests/clean/loadstore_overaligned.ll) | `llvm.mlir.constant`: `() -> vector<4xi32>` | returned `void` | failed: `Severe Z3 error` |
| [`clean/metadata.ll`](llubi-tests/clean/metadata.ll) | `llvm.mlir.constant`: `() -> vector<8xi32>` | returned `void` | rejected: `Unsupported metadata: 47` |
| [`clean/ptrtoaddr.ll`](llubi-tests/clean/ptrtoaddr.ll) | `llvm.inttoptr`: verifier says `Expected the pointer side to have !llvm.ptr type` | returned `void` | rejected: `Unsupported instruction:   %wide1 = inttoptr i64 4294967301 to ptr addrspace(1)` |
| [`clean/ptrtoaddr_after_ptrtoint.ll`](llubi-tests/clean/ptrtoaddr_after_ptrtoint.ll) | `llvm.ptrtoaddr`: `(!llvm.ptr) -> i64` | returned `void` | failed: `Severe Z3 error` |
| [`clean/reset_return_value_slot.ll`](llubi-tests/clean/reset_return_value_slot.ll) | `llvm.call`: `() -> i16` | returned `void` | failed: `Severe Z3 error` |
| [`clean/struct.ll`](llubi-tests/clean/struct.ll) | `llvm.mlir.poison`: `() -> !llvm.struct<(i32, i32)>` | returned `void` | failed: `Severe Z3 error` |
| [`clean/undef.ll`](llubi-tests/clean/undef.ll) | `llvm.add`: verifier says `Expected operand 0 to have integer type` | returned `void` | crashed |
| [`clean/vector.ll`](llubi-tests/clean/vector.ll) | **parser**: `vector element type expected` at `vector<[4]xi32>` | returned `void` | failed: `Severe Z3 error` |
| [`ub/alloca_poison_count.ll`](llubi-tests/ub/alloca_poison_count.ll) | `llvm.alloca`: `(i32) -> !llvm.ptr` | UB at [line 5](llubi-tests/ub/alloca_poison_count.ll#L5): Alloca with poison array size. | UB at `%alloc_dyn` |
| [`ub/assume_false.ll`](llubi-tests/ub/assume_false.ll) | `llvm.intr.assume`: `(i1) -> ()` | UB at [line 5](llubi-tests/ub/assume_false.ll#L5): Assume on false or poison condition. | UB at `assume` |
| [`ub/assume_invalid_align.ll`](llubi-tests/ub/assume_invalid_align.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr, i64) -> ()` | UB at [line 9](llubi-tests/ub/assume_invalid_align.ll#L9): The pointer ptr 0x8 [alloc] violates align(4294967296) assumption. | UB at `assume` |
| [`ub/assume_misalign.ll`](llubi-tests/ub/assume_misalign.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr, i32) -> ()` | UB at [line 6](llubi-tests/ub/assume_misalign.ll#L6): The pointer ptr 0x8 [alloc] violates align(2048) assumption. | UB at `assume` |
| [`ub/assume_misalign_all_ones.ll`](llubi-tests/ub/assume_misalign_all_ones.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr<1>, i32) -> ()` | UB at [line 7](llubi-tests/ub/assume_misalign_all_ones.ll#L7): The pointer ptr 0xFFFFFFFFFFFFFFFF [nullary] violates align(2048) assumption. | rejected: `Unsupported instruction:   call void @llvm.assume(i1 true) [ "align"(ptr addrspace(1) null, i32 2048) ]` |
| [`ub/assume_non_pow2_align_offset.ll`](llubi-tests/ub/assume_non_pow2_align_offset.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr, i32, i32) -> ()` | UB at [line 9](llubi-tests/ub/assume_non_pow2_align_offset.ll#L9): Assume on pointer ptr 0x8 [alloc] with a nonzero adjusted address and a non-power-of-two alignment 17. | UB at `assume` |
| [`ub/assume_nondereferenceable.ll`](llubi-tests/ub/assume_nondereferenceable.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr, i32) -> ()` | UB at [line 6](llubi-tests/ub/assume_nondereferenceable.ll#L6): The pointer ptr 0x8 [alloc] violates dereferenceable(2048) assumption. | UB at `assume` |
| [`ub/assume_null.ll`](llubi-tests/ub/assume_null.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr) -> ()` | UB at [line 5](llubi-tests/ub/assume_null.ll#L5): The pointer ptr 0x0 [nullary] violates nonnull assumption. | UB at `assume` |
| [`ub/assume_null_all_ones.ll`](llubi-tests/ub/assume_null_all_ones.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr<1>) -> ()` | UB at [line 10](llubi-tests/ub/assume_null_all_ones.ll#L10): The pointer ptr 0xFFFFFFFFFFFFFFFF [nullary] violates nonnull assumption. | rejected: `Unsupported instruction:   %res = load ptr addrspace(1), ptr %storage, align 8` |
| [`ub/assume_poison.ll`](llubi-tests/ub/assume_poison.ll) | `llvm.intr.assume`: `(i1) -> ()` | UB at [line 5](llubi-tests/ub/assume_poison.ll#L5): The value poison violates noundef attribute. | UB at `assume` |
| [`ub/assume_poison_align.ll`](llubi-tests/ub/assume_poison_align.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr, i32) -> ()` | UB at [line 5](llubi-tests/ub/assume_poison_align.ll#L5): Assume on poison pointer. | UB at `assume` |
| [`ub/assume_pow2_align_offset.ll`](llubi-tests/ub/assume_pow2_align_offset.ll) | `llvm.intr.assume`: `(i1, !llvm.ptr, i32, i32) -> ()` | UB at [line 9](llubi-tests/ub/assume_pow2_align_offset.ll#L9): The pointer ptr 0x8 [alloc] violates align(16) assumption. | UB at `assume` |
| [`ub/attribute_dereferenceable_ub_nullary_provenance.ll`](llubi-tests/ub/attribute_dereferenceable_ub_nullary_provenance.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 11](llubi-tests/ub/attribute_dereferenceable_ub_nullary_provenance.ll#L11): The value ptr 0xE82FEEACEEB98B3E [nullary] violates dereferenceable(4) attribute. | UB |
| [`ub/attribute_dereferenceable_ub_oob1.ll`](llubi-tests/ub/attribute_dereferenceable_ub_oob1.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 10](llubi-tests/ub/attribute_dereferenceable_ub_oob1.ll#L10): The value ptr 0x8 [alloc] violates dereferenceable(8) attribute. | UB |
| [`ub/attribute_dereferenceable_ub_oob2.ll`](llubi-tests/ub/attribute_dereferenceable_ub_oob2.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 11](llubi-tests/ub/attribute_dereferenceable_ub_oob2.ll#L11): The value ptr 0x7 [alloc + -1] violates dereferenceable(2) attribute. | UB |
| [`ub/attribute_dereferenceable_ub_oob3.ll`](llubi-tests/ub/attribute_dereferenceable_ub_oob3.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 11](llubi-tests/ub/attribute_dereferenceable_ub_oob3.ll#L11): The value ptr 0xA [alloc + 2] violates dereferenceable(3) attribute. | UB |
| [`ub/attribute_dereferenceable_ub_poison.ll`](llubi-tests/ub/attribute_dereferenceable_ub_poison.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 9](llubi-tests/ub/attribute_dereferenceable_ub_poison.ll#L9): The value poison violates dereferenceable(4) attribute. | UB |
| [`ub/attribute_noundef_agg_ub.ll`](llubi-tests/ub/attribute_noundef_agg_ub.ll) | `llvm.mlir.undef`: `() -> !llvm.struct<(i32, i32)>` | UB at [line 9](llubi-tests/ub/attribute_noundef_agg_ub.ll#L9): The value { i32 0, poison } violates noundef attribute. | rejected: `Unsupported attribute:` |
| [`ub/attribute_noundef_ub.ll`](llubi-tests/ub/attribute_noundef_ub.ll) | `llvm.call`: `(i32) -> ()` | UB at [line 10](llubi-tests/ub/attribute_noundef_ub.ll#L10): The value poison violates noundef attribute. | UB |
| [`ub/byval_lifetime.ll`](llubi-tests/ub/byval_lifetime.ll) | `llvm.call`: `(!llvm.ptr) -> !llvm.ptr` | UB at [line 11](llubi-tests/ub/byval_lifetime.ll#L11): Try to access a dead memory object at address 0x10. | failed: `Severe Z3 error` |
| [`ub/byval_misalign.ll`](llubi-tests/ub/byval_misalign.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 10](llubi-tests/ub/byval_misalign.ll#L10): Misaligned memory access. Address: 0x8, Required alignment: 16. | UB |
| [`ub/byval_misalign_callsite.ll`](llubi-tests/ub/byval_misalign_callsite.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 10](llubi-tests/ub/byval_misalign_callsite.ll#L10): Misaligned memory access. Address: 0x8, Required alignment: 16. | UB |
| [`ub/byval_mismatch1.ll`](llubi-tests/ub/byval_mismatch1.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 10](llubi-tests/ub/byval_mismatch1.ll#L10): Mismatched byval attribute between callee and callsite. | failed: `Severe Z3 error` |
| [`ub/byval_mismatch2.ll`](llubi-tests/ub/byval_mismatch2.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 10](llubi-tests/ub/byval_mismatch2.ll#L10): Mismatched byval attribute between callee and callsite. | failed: `Severe Z3 error` |
| [`ub/byval_mismatch3.ll`](llubi-tests/ub/byval_mismatch3.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 10](llubi-tests/ub/byval_mismatch3.ll#L10): Mismatched byval attribute between callee and callsite. | failed: `Severe Z3 error` |
| [`ub/byval_null.ll`](llubi-tests/ub/byval_null.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 9](llubi-tests/ub/byval_null.ll#L9): Invalid memory access via a pointer with nullary provenance. | UB |
| [`ub/byval_oversize.ll`](llubi-tests/ub/byval_oversize.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 10](llubi-tests/ub/byval_oversize.ll#L10): Memory access is out of bounds. Accessed size: 4, Address: 0x8, Object base: 0x8, Object size: 1. | UB |
| [`ub/byval_poison.ll`](llubi-tests/ub/byval_poison.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 9](llubi-tests/ub/byval_poison.ll#L9): Invalid poison byval pointer argument. | UB |
| [`ub/call_mismatched_signature.ll`](llubi-tests/ub/call_mismatched_signature.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 9](llubi-tests/ub/call_mismatched_signature.ll#L9): Indirect call through a function pointer with mismatched signature. Expected: void (), Actual: i32 () | failed: `Severe Z3 error` |
| [`ub/call_poison.ll`](llubi-tests/ub/call_poison.ll) | `llvm.call`: `(!llvm.ptr) -> ()` | UB at [line 6](llubi-tests/ub/call_poison.ll#L6): Indirect call through poison function pointer. | UB |
| [`ub/indirectbr_poison.ll`](llubi-tests/ub/indirectbr_poison.ll) | `llvm.func`: verifier says `Expected the last operation of a block to be a terminator` | UB at [line 6](llubi-tests/ub/indirectbr_poison.ll#L6): Indirect branch on poison. | rejected: `Unsupported instruction:   indirectbr ptr poison, [label %exit]` |
| [`ub/intr_memory_constant_ub.ll`](llubi-tests/ub/intr_memory_constant_ub.ll) | **other**: `unsupported value of global @constant_dst` | UB at [line 7](llubi-tests/ub/intr_memory_constant_ub.ll#L7): Try to write to a constant memory object: ptr 0x8 [@constant_dst]. | UB at `memset` |
| [`ub/load_noundef_ub_poison_padding.ll`](llubi-tests/ub/load_noundef_ub_poison_padding.ll) | `llvm.mlir.undef`: `() -> vector<2xi4>` | UB at [line 7](llubi-tests/ub/load_noundef_ub_poison_padding.ll#L7): The value loaded contains undefined bits. | UB at `assume` |
| [`ub/ptrtoaddr_no_expose.ll`](llubi-tests/ub/ptrtoaddr_no_expose.ll) | `llvm.ptrtoaddr`: `(!llvm.ptr) -> i64` | UB at [line 9](llubi-tests/ub/ptrtoaddr_no_expose.ll#L9): Invalid memory access via a pointer with nullary provenance. | failed: `Severe Z3 error` |
| [`ub/store_dead.ll`](llubi-tests/ub/store_dead.ll) | `llvm.intr.lifetime.start`: `(!llvm.ptr) -> ()` | UB at [line 9](llubi-tests/ub/store_dead.ll#L9): Try to access a dead memory object at address 0x8. | UB at `store` |
| [`ub/store_dead_gep.ll`](llubi-tests/ub/store_dead_gep.ll) | `llvm.intr.lifetime.start`: `(!llvm.ptr) -> ()` | UB at [line 9](llubi-tests/ub/store_dead_gep.ll#L9): Try to access a dead memory object at address 0x9. | UB at `store` |

</details>

## Manifest

| Component | Version | SHA-256 |
| -- | -- | -- |
| veir-interpret | [`61e57f884662`](https://github.com/opencompl/veir/commit/61e57f884662b6406db349bfbc154fe63677a87d) | `7c2406573ae30834ca19364fbfcacc1c21e09f7c757a43e3c6fb348f2f532a5a` |
| alive-exec | version v21.0-118-gd1533abb-dirty | `f7498df7a22508f22fd2de3f81e08ed5a3214c8e9e8e4555fad8db050a6b83d1` |
| llubi | LLVM version 23.1.0-rc1 | `1acd08617c94e77035ea3dbd8e3ad270ae1f73bafcabef884e981cffb834fce2` |
| mlir-translate | LLVM version 23.1.0-rc1 | `34403b40057d9708b425463f45d84a2c239dc15264da6c1e63ce1973ff975bb8` |
| corpus.tar.gz |  | `9c27c23fe92d74578bd24f656e76dce8643f6bc90f762be31d2b25d21004a2f1` |
