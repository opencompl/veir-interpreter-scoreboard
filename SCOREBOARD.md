# Veir-Interpreter Scoreboard

We run `veir-interpret` on the 102 tests in `llubi-tests` and compare with the
results of `llubi`.

| Verdict | Tests |
|---|---:|
| PASS | 14 (13.7%) |
| MISMATCH | 5 (4.9%) |
| UNSUPPORTED | 83 (81.4%) |
| TIMEOUT | 0 (0.0%) |

## Mismatches

`veir-interpret` fully executed these tests, but has a different result than `llubi`!

| Test | llubi | veir-interpret | Verdict |
|---|---|---|---|
| `ub/global_constant_store.ll` | `Immediate UB detected: Try to write to a constant memory object: ptr 0x8 [@constant].` | returned `void` | MISMATCH |
| `ub/inttoptr_gep.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | returned `void` | MISMATCH |
| `ub/load_noundef_ub_poison.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | returned `void` | MISMATCH |
| `ub/load_noundef_ub_undef.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | returned `void` | MISMATCH |
| `ub/metadata_noundef_ub.ll` | `Immediate UB detected: The value poison violates !noundef metadata.` | returned `void` | MISMATCH |

## Unsupported

| Reason | Count | Tests |
|---|---:|---|
| **interpreter**: failed at `llvm.call` | 20 | `clean/alloca.ll`, `clean/byval.ll`, `clean/reset_return_value_slot.ll`, `ub/attribute_dereferenceable_ub_nullary_provenance.ll`, `ub/attribute_dereferenceable_ub_oob1.ll`, `ub/attribute_dereferenceable_ub_oob2.ll`, `ub/attribute_dereferenceable_ub_oob3.ll`, `ub/attribute_dereferenceable_ub_poison.ll`, `ub/attribute_noundef_ub.ll`, `ub/byval_lifetime.ll`, `ub/byval_misalign.ll`, `ub/byval_misalign_callsite.ll`, `ub/byval_mismatch1.ll`, `ub/byval_mismatch2.ll`, `ub/byval_mismatch3.ll`, `ub/byval_null.ll`, `ub/byval_oversize.ll`, `ub/byval_poison.ll`, `ub/call_mismatched_signature.ll`, `ub/call_poison.ll` |
| **interpreter**: failed at `llvm.intr.assume` | 10 | `clean/assume_operand_bundles.ll`, `ub/assume_false.ll`, `ub/assume_invalid_align.ll`, `ub/assume_misalign.ll`, `ub/assume_non_pow2_align_offset.ll`, `ub/assume_nondereferenceable.ll`, `ub/assume_null.ll`, `ub/assume_poison.ll`, `ub/assume_poison_align.ll`, `ub/assume_pow2_align_offset.ll` |
| **interpreter**: failed at `llvm.mlir.constant` | 7 | `clean/bitcast_be.ll`, `clean/bitcast_le.ll`, `clean/intr_experimental_vector.ll`, `clean/intr_vector_manip.ll`, `clean/intr_vector_reduce.ll`, `clean/loadstore_overaligned.ll`, `clean/metadata.ll` |
| **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | 6 | `clean/fp_arith_bfloat.ll`, `clean/fp_arith_double.ll`, `clean/fp_arith_float.ll`, `clean/fp_arith_fp128.ll`, `clean/fp_arith_fp80.ll`, `clean/fp_arith_half.ll` |
| **interpreter**: failed at `llvm.mlir.poison` | 4 | `clean/intr_fp_fptoi_sat.ll`, `clean/intr_fp_is_fpclass.ll`, `clean/intr_fp_minmax.ll`, `clean/struct.ll` |
| **parser**: `vector element type expected` | 3 | `clean/gep.ll`, `clean/global_constexpr_initializer.ll`, `clean/vector.ll` |
| **verifier**: `llvm.add: Expected operand 0 to have integer type` | 3 | `clean/int_arith.ll`, `clean/inttoptr_ptrtoint_constantexpr.ll`, `clean/undef.ll` |
| **interpreter**: failed at `llvm.mlir.undef` | 3 | `clean/intr_arith_overflow.ll`, `ub/attribute_noundef_agg_ub.ll`, `ub/load_noundef_ub_poison_padding.ll` |
| **parser**: `Expected punctuation '}'` | 3 | `clean/ptrtoaddr.ll`, `ub/assume_misalign_all_ones.ll`, `ub/assume_null_all_ones.ll` |
| crashed with exit status 1 | 2 | `clean/byval_padding.ll`, `ub/intr_memory_constant_ub.ll` |
| **interpreter**: failed at `llvm.fdiv` | 2 | `clean/fp_fastmath.ll`, `clean/fp_phi_select.ll` |
| **interpreter**: failed at `llvm.ptrtoaddr` | 2 | `clean/ptrtoaddr_after_ptrtoint.ll`, `ub/ptrtoaddr_no_expose.ll` |
| **interpreter**: failed at `llvm.intr.lifetime.start` | 2 | `ub/store_dead.ll`, `ub/store_dead_gep.ll` |
| **verifier**: `llvm.sitofp: Expected operand 0 to have integer type` | 1 | `clean/fp_cast.ll` |
| **interpreter**: failed at `llvm.fcmp` | 1 | `clean/fp_cmp.ll` |
| **interpreter**: failed at `llvm.fadd` | 1 | `clean/fp_denorm.ll` |
| **interpreter**: failed at `llvm.getelementptr` | 1 | `clean/gep-16-bit-addrspace.ll` |
| **verifier**: `llvm.icmp: Expected operand 0 to have integer or pointer type` | 1 | `clean/icmp_ptr.ll` |
| **verifier**: `llvm.intr.sadd.sat: Expected operand 0 to have integer type` | 1 | `clean/intr_arith_sat.ll` |
| **verifier**: `llvm.intr.bitreverse: Expected operand 0 to have integer type` | 1 | `clean/intr_bit_manip.ll` |
| **verifier**: `llvm.intr.fmuladd: Expected operand 0 to have floating point type` | 1 | `clean/intr_fp_fma.ll` |
| **verifier**: `llvm.intr.fabs: Expected operand 0 to have floating point type` | 1 | `clean/intr_fp_unary.ll` |
| **verifier**: `llvm.intr.abs: Expected operand 0 to have integer type` | 1 | `clean/intr_int_arith.ll` |
| **interpreter**: failed at `llvm.intr.memset.inline` | 1 | `clean/intr_memory.ll` |
| **interpreter**: failed at `llvm.intr.ssa.copy` | 1 | `clean/intr_passthrough.ll` |
| **interpreter**: failed at `llvm.intr.vscale` | 1 | `clean/intr_vscale.ll` |
| **interpreter**: failed at `llvm.inttoptr` | 1 | `clean/inttoptr.ll` |
| **interpreter**: failed at `llvm.alloca` | 1 | `ub/alloca_poison_count.ll` |
| **verifier**: `llvm.func: Expected the last operation of a block to be a terminator` | 1 | `ub/indirectbr_poison.ll` |

## All tests

<details>
<summary>Show all tests</summary>

| Test | llubi | veir-interpret | Verdict |
|---|---|---|---|
| `clean/alloca.ll` | returned `void` | **interpreter**: failed at `llvm.call` (line 15) | UNSUPPORTED |
| `clean/assume_operand_bundles.ll` | returned `void` | **interpreter**: failed at `llvm.intr.assume` (line 21) | UNSUPPORTED |
| `clean/bitcast_be.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.constant` (line 10) | UNSUPPORTED |
| `clean/bitcast_le.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.constant` (line 10) | UNSUPPORTED |
| `clean/byval.ll` | returned `void` | **interpreter**: failed at `llvm.call` (line 25) | UNSUPPORTED |
| `clean/byval_padding.ll` | returned `void` | crashed with exit status 1 | UNSUPPORTED |
| `clean/fp_arith_bfloat.ll` | returned `void` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_double.ll` | returned `void` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_float.ll` | returned `void` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_fp128.ll` | returned `void` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_fp80.ll` | returned `void` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_half.ll` | returned `void` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_cast.ll` | returned `void` | **verifier**: `llvm.sitofp: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/fp_cmp.ll` | returned `void` | **interpreter**: failed at `llvm.fcmp` (line 6) | UNSUPPORTED |
| `clean/fp_denorm.ll` | returned `void` | **interpreter**: failed at `llvm.fadd` (line 6) | UNSUPPORTED |
| `clean/fp_fastmath.ll` | returned `void` | **interpreter**: failed at `llvm.fdiv` (line 7) | UNSUPPORTED |
| `clean/fp_phi_select.ll` | returned `void` | **interpreter**: failed at `llvm.fdiv` (line 7) | UNSUPPORTED |
| `clean/gep-16-bit-addrspace.ll` | returned `void` | **interpreter**: failed at `llvm.getelementptr` (line 6) | UNSUPPORTED |
| `clean/gep.ll` | returned `void` | **parser**: `vector element type expected` (line 46) | UNSUPPORTED |
| `clean/global_constexpr_initializer.ll` | returned `void` | **parser**: `vector element type expected` (line 128) | UNSUPPORTED |
| `clean/global_external.ll` | returned `void` | returned `void` | PASS |
| `clean/icmp_ptr.ll` | returned `void` | **verifier**: `llvm.icmp: Expected operand 0 to have integer or pointer type` | UNSUPPORTED |
| `clean/int_arith.ll` | returned `void` | **verifier**: `llvm.add: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/intr_arith_overflow.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.undef` (line 8) | UNSUPPORTED |
| `clean/intr_arith_sat.ll` | returned `void` | **verifier**: `llvm.intr.sadd.sat: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/intr_bit_manip.ll` | returned `void` | **verifier**: `llvm.intr.bitreverse: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/intr_experimental_vector.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.constant` (line 5) | UNSUPPORTED |
| `clean/intr_fp_fma.ll` | returned `void` | **verifier**: `llvm.intr.fmuladd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/intr_fp_fptoi_sat.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.poison` (line 7) | UNSUPPORTED |
| `clean/intr_fp_is_fpclass.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.poison` (line 14) | UNSUPPORTED |
| `clean/intr_fp_minmax.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.poison` (line 9) | UNSUPPORTED |
| `clean/intr_fp_unary.ll` | returned `void` | **verifier**: `llvm.intr.fabs: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/intr_int_arith.ll` | returned `void` | **verifier**: `llvm.intr.abs: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/intr_memory.ll` | returned `void` | **interpreter**: failed at `llvm.intr.memset.inline` (line 28) | UNSUPPORTED |
| `clean/intr_passthrough.ll` | returned `void` | **interpreter**: failed at `llvm.intr.ssa.copy` (line 6) | UNSUPPORTED |
| `clean/intr_vector_manip.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.constant` (line 3) | UNSUPPORTED |
| `clean/intr_vector_reduce.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.constant` (line 3) | UNSUPPORTED |
| `clean/intr_vscale.ll` | returned `void` | **interpreter**: failed at `llvm.intr.vscale` (line 3) | UNSUPPORTED |
| `clean/inttoptr.ll` | returned `void` | **interpreter**: failed at `llvm.inttoptr` (line 8) | UNSUPPORTED |
| `clean/inttoptr_ptrtoint_constantexpr.ll` | returned `void` | **verifier**: `llvm.add: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/loadstore_overaligned.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.constant` (line 5) | UNSUPPORTED |
| `clean/main2.ll` | returned `i32 0` | returned `i32 0` | PASS |
| `clean/metadata.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.constant` (line 16) | UNSUPPORTED |
| `clean/noalias_scope.ll` | returned `void` | returned `void` | PASS |
| `clean/ptrtoaddr.ll` | returned `void` | **parser**: `Expected punctuation '}'` (line 5) | UNSUPPORTED |
| `clean/ptrtoaddr_after_ptrtoint.ll` | returned `void` | **interpreter**: failed at `llvm.ptrtoaddr` (line 7) | UNSUPPORTED |
| `clean/reset_return_value_slot.ll` | returned `void` | **interpreter**: failed at `llvm.call` (line 3) | UNSUPPORTED |
| `clean/struct.ll` | returned `void` | **interpreter**: failed at `llvm.mlir.poison` (line 3) | UNSUPPORTED |
| `clean/undef.ll` | returned `void` | **verifier**: `llvm.add: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/vector.ll` | returned `void` | **parser**: `vector element type expected` (line 9) | UNSUPPORTED |
| `ub/alloca_large_count.ll` | `Immediate UB detected: Alloca with large array size that overflows uint64_t. Size: -1` | UB at `%1 = "llvm.alloca"(%0) <{alignment = 4 : i64, elem_type = i32}> : (i128) -> !llvm.ptr` (line 4) | PASS |
| `ub/alloca_poison_count.ll` | `Immediate UB detected: Alloca with poison array size.` | **interpreter**: failed at `llvm.alloca` (line 4) | UNSUPPORTED |
| `ub/alloca_size_overflow.ll` | `Immediate UB detected: Alloca with allocation size that overflows uint64_t. Size: -1` | UB at `%1 = "llvm.alloca"(%0) <{alignment = 4 : i64, elem_type = i32}> : (i64) -> !llvm.ptr` (line 4) | PASS |
| `ub/assume_false.ll` | `Immediate UB detected: Assume on false or poison condition.` | **interpreter**: failed at `llvm.intr.assume` (line 4) | UNSUPPORTED |
| `ub/assume_invalid_align.ll` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates align(4294967296) assumption.` | **interpreter**: failed at `llvm.intr.assume` (line 9) | UNSUPPORTED |
| `ub/assume_misalign.ll` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates align(2048) assumption.` | **interpreter**: failed at `llvm.intr.assume` (line 7) | UNSUPPORTED |
| `ub/assume_misalign_all_ones.ll` | `Immediate UB detected: The pointer ptr 0xFFFFFFFFFFFFFFFF [nullary] violates align(2048) assumption.` | **parser**: `Expected punctuation '}'` (line 4) | UNSUPPORTED |
| `ub/assume_non_pow2_align_offset.ll` | `Immediate UB detected: Assume on pointer ptr 0x8 [alloc] with a nonzero adjusted address and a non-power-of-two alignment 17.` | **interpreter**: failed at `llvm.intr.assume` (line 13) | UNSUPPORTED |
| `ub/assume_nondereferenceable.ll` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates dereferenceable(2048) assumption.` | **interpreter**: failed at `llvm.intr.assume` (line 7) | UNSUPPORTED |
| `ub/assume_null.ll` | `Immediate UB detected: The pointer ptr 0x0 [nullary] violates nonnull assumption.` | **interpreter**: failed at `llvm.intr.assume` (line 5) | UNSUPPORTED |
| `ub/assume_null_all_ones.ll` | `Immediate UB detected: The pointer ptr 0xFFFFFFFFFFFFFFFF [nullary] violates nonnull assumption.` | **parser**: `Expected punctuation '}'` (line 8) | UNSUPPORTED |
| `ub/assume_poison.ll` | `Immediate UB detected: The value poison violates noundef attribute.` | **interpreter**: failed at `llvm.intr.assume` (line 4) | UNSUPPORTED |
| `ub/assume_poison_align.ll` | `Immediate UB detected: Assume on poison pointer.` | **interpreter**: failed at `llvm.intr.assume` (line 6) | UNSUPPORTED |
| `ub/assume_pow2_align_offset.ll` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates align(16) assumption.` | **interpreter**: failed at `llvm.intr.assume` (line 14) | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_nullary_provenance.ll` | `Immediate UB detected: The value ptr 0xE82FEEACEEB98B3E [nullary] violates dereferenceable(4) attribute.` | **interpreter**: failed at `llvm.call` (line 10) | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_oob1.ll` | `Immediate UB detected: The value ptr 0x8 [alloc] violates dereferenceable(8) attribute.` | **interpreter**: failed at `llvm.call` (line 9) | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_oob2.ll` | `Immediate UB detected: The value ptr 0x7 [alloc + -1] violates dereferenceable(2) attribute.` | **interpreter**: failed at `llvm.call` (line 11) | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_oob3.ll` | `Immediate UB detected: The value ptr 0xA [alloc + 2] violates dereferenceable(3) attribute.` | **interpreter**: failed at `llvm.call` (line 11) | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_poison.ll` | `Immediate UB detected: The value poison violates dereferenceable(4) attribute.` | **interpreter**: failed at `llvm.call` (line 8) | UNSUPPORTED |
| `ub/attribute_noundef_agg_ub.ll` | `Immediate UB detected: The value { i32 0, poison } violates noundef attribute.` | **interpreter**: failed at `llvm.mlir.undef` (line 9) | UNSUPPORTED |
| `ub/attribute_noundef_ub.ll` | `Immediate UB detected: The value poison violates noundef attribute.` | **interpreter**: failed at `llvm.call` (line 8) | UNSUPPORTED |
| `ub/br_poison.ll` | `Immediate UB detected: Branch on poison condition.` | UB at `"llvm.cond_br"(%0)[^bb1, ^bb1] <{operandSegmentSizes = array<i32: 1, 0, 0>}> : (i1) -> ()` (line 4) | PASS |
| `ub/byval_lifetime.ll` | `Immediate UB detected: Try to access a dead memory object at address 0x10.` | **interpreter**: failed at `llvm.call` (line 10) | UNSUPPORTED |
| `ub/byval_misalign.ll` | `Immediate UB detected: Misaligned memory access. Address: 0x8, Required alignment: 16.` | **interpreter**: failed at `llvm.call` (line 9) | UNSUPPORTED |
| `ub/byval_misalign_callsite.ll` | `Immediate UB detected: Misaligned memory access. Address: 0x8, Required alignment: 16.` | **interpreter**: failed at `llvm.call` (line 9) | UNSUPPORTED |
| `ub/byval_mismatch1.ll` | `Immediate UB detected: Mismatched byval attribute between callee and callsite.` | **interpreter**: failed at `llvm.call` (line 9) | UNSUPPORTED |
| `ub/byval_mismatch2.ll` | `Immediate UB detected: Mismatched byval attribute between callee and callsite.` | **interpreter**: failed at `llvm.call` (line 9) | UNSUPPORTED |
| `ub/byval_mismatch3.ll` | `Immediate UB detected: Mismatched byval attribute between callee and callsite.` | **interpreter**: failed at `llvm.call` (line 9) | UNSUPPORTED |
| `ub/byval_null.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | **interpreter**: failed at `llvm.call` (line 8) | UNSUPPORTED |
| `ub/byval_oversize.ll` | `Immediate UB detected: Memory access is out of bounds. Accessed size: 4, Address: 0x8, Object base: 0x8, Object size: 1.` | **interpreter**: failed at `llvm.call` (line 9) | UNSUPPORTED |
| `ub/byval_poison.ll` | `Immediate UB detected: Invalid poison byval pointer argument.` | **interpreter**: failed at `llvm.call` (line 8) | UNSUPPORTED |
| `ub/call_mismatched_signature.ll` | `Immediate UB detected: Indirect call through a function pointer with mismatched signature. Expected: void (), Actual: i32 ()` | **interpreter**: failed at `llvm.call` (line 8) | UNSUPPORTED |
| `ub/call_poison.ll` | `Immediate UB detected: Indirect call through poison function pointer.` | **interpreter**: failed at `llvm.call` (line 4) | UNSUPPORTED |
| `ub/global_constant_store.ll` | `Immediate UB detected: Try to write to a constant memory object: ptr 0x8 [@constant].` | returned `void` | MISMATCH |
| `ub/indirectbr_poison.ll` | `Immediate UB detected: Indirect branch on poison.` | **verifier**: `llvm.func: Expected the last operation of a block to be a terminator` | UNSUPPORTED |
| `ub/intr_memory_constant_ub.ll` | `Immediate UB detected: Try to write to a constant memory object: ptr 0x8 [@constant_dst].` | crashed with exit status 1 | UNSUPPORTED |
| `ub/inttoptr_generation.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | UB at `"llvm.store"(%2, %7) <{alignment = 4 : i64, ordering = 0 : i64}> : (i32, !llvm.ptr) -> ()` (line 12) | PASS |
| `ub/inttoptr_generation2.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | UB at `"llvm.store"(%2, %9) <{alignment = 4 : i64, ordering = 0 : i64}> : (i32, !llvm.ptr) -> ()` (line 14) | PASS |
| `ub/inttoptr_gep.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | returned `void` | MISMATCH |
| `ub/inttoptr_multiobj.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | UB at `"llvm.store"(%3, %11) <{alignment = 2 : i64, ordering = 0 : i64}> : (i16, !llvm.ptr) -> ()` (line 16) | PASS |
| `ub/inttoptr_multiobj2.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | UB at `"llvm.store"(%1, %8) <{alignment = 4 : i64, ordering = 0 : i64}> : (i32, !llvm.ptr) -> ()` (line 14) | PASS |
| `ub/inttoptr_oob.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | UB at `"llvm.store"(%3, %7) <{alignment = 4 : i64, ordering = 0 : i64}> : (i64, !llvm.ptr) -> ()` (line 13) | PASS |
| `ub/inttoptr_oob2.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | UB at `"llvm.store"(%3, %8) <{alignment = 4 : i64, ordering = 0 : i64}> : (i64, !llvm.ptr) -> ()` (line 14) | PASS |
| `ub/load_noundef_ub_poison.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | returned `void` | MISMATCH |
| `ub/load_noundef_ub_poison_padding.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | **interpreter**: failed at `llvm.mlir.undef` (line 6) | UNSUPPORTED |
| `ub/load_noundef_ub_undef.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | returned `void` | MISMATCH |
| `ub/metadata_noundef_ub.ll` | `Immediate UB detected: The value poison violates !noundef metadata.` | returned `void` | MISMATCH |
| `ub/ptrtoaddr_no_expose.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | **interpreter**: failed at `llvm.ptrtoaddr` (line 6) | UNSUPPORTED |
| `ub/store_dead.ll` | `Immediate UB detected: Try to access a dead memory object at address 0x8.` | **interpreter**: failed at `llvm.intr.lifetime.start` (line 6) | UNSUPPORTED |
| `ub/store_dead_gep.ll` | `Immediate UB detected: Try to access a dead memory object at address 0x9.` | **interpreter**: failed at `llvm.intr.lifetime.start` (line 7) | UNSUPPORTED |
| `ub/switch_poison.ll` | `Immediate UB detected: Switch on poison condition.` | UB at `"llvm.switch"(%0)[^bb1] <{case_operand_segments = array<i32>, operandSegmentSizes = array<i32: 1, 0, 0>}> : (i32) -> ()` (line 4) | PASS |
| `ub/unreachable.ll` | `Immediate UB detected: Unreachable code.` | UB at `"llvm.unreachable"() : () -> ()` (line 3) | PASS |

</details>

## Manifest

| Component | Version | SHA-256 |
|---|---|---|
| veir-interpret | [`c8b505cfee36`](https://github.com/opencompl/veir/commit/c8b505cfee36079468542ddcff46e637b27faead) | `0f09b54f29b8a5648d01f30bedf334a4c104089a464d511b69d59ca1f53f33be` |
| llubi | LLVM version 23.1.0-rc1 | `1acd08617c94e77035ea3dbd8e3ad270ae1f73bafcabef884e981cffb834fce2` |
| mlir-translate | LLVM version 23.1.0-rc1 | `34403b40057d9708b425463f45d84a2c239dc15264da6c1e63ce1973ff975bb8` |
| corpus.tar.gz |  | `c81112457ef97ba8597d761fe5b3bad8c3197b2ff4b2bdf8a9dc9d7cbf5ca5d7` |
