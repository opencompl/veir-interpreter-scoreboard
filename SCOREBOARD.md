# Veir-Interpreter Scoreboard

We run `veir-interpret` on the tests in `llubi-tests` and compare its results with
`llubi` and Alive2's `alive-exec`, read the way VeIR's `Tools/llubi-interpret` and
`Tools/alive-interpret` read them. See [README.md](README.md).

**20/102** tests run to a result · **15/20** of those agree with `llubi` · **8/13** of those agree with `alive-exec` (7 where `alive-exec` has no result)

## Mismatches

`veir-interpret` ran these tests to a different result than `llubi` or `alive-exec`.

| Test | veir-interpret | llubi | alive-exec |
| -- | -- | -- | -- |
| `ub/global_constant_store.ll` | `Program output: #[]` | ❌ `Immediate UB detected: Try to write to a constant memory object: ptr 0x8 [@constant].` | ❌ `UB triggered` |
| `ub/inttoptr_gep.ll` | `Program output: #[]` | ❌ `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | ❌ `UB triggered` |
| `ub/load_noundef_ub_poison.ll` | `Program output: #[]` | ❌ `Immediate UB detected: The value loaded contains undefined bits.` | ❌ `UB triggered` |
| `ub/load_noundef_ub_undef.ll` | `Program output: #[]` | ❌ `Immediate UB detected: The value loaded contains undefined bits.` | ❌ `UB triggered` |
| `ub/metadata_noundef_ub.ll` | `Program output: #[]` | ❌ `Immediate UB detected: The value poison violates !noundef metadata.` | ❌ `UB triggered` |

## Fix next

Why `veir-interpret` gives no result, for the most tests. The collapsed table below
lists every reason, with its tests.

| # | Reason | Tests affected |
| -: | -- | -: |
| 1 | **interpreter**: failed at `llvm.call` | 20/102 |
| 2 | **interpreter**: failed at `llvm.intr.assume` | 10/102 |
| 3 | **interpreter**: failed at `llvm.mlir.constant` | 7/102 |
| 4 | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | 6/102 |
| 5 | **interpreter**: failed at `llvm.mlir.poison` | 4/102 |

<details>
<summary>All reasons (29), with their tests</summary>

| Reason | Tests |
| -- | -- |
| **interpreter**: failed at `llvm.call` | `clean/alloca.ll`, `clean/byval.ll`, `clean/reset_return_value_slot.ll`, `ub/attribute_dereferenceable_ub_nullary_provenance.ll`, `ub/attribute_dereferenceable_ub_oob1.ll`, `ub/attribute_dereferenceable_ub_oob2.ll`, `ub/attribute_dereferenceable_ub_oob3.ll`, `ub/attribute_dereferenceable_ub_poison.ll`, `ub/attribute_noundef_ub.ll`, `ub/byval_lifetime.ll`, `ub/byval_misalign.ll`, `ub/byval_misalign_callsite.ll`, `ub/byval_mismatch1.ll`, `ub/byval_mismatch2.ll`, `ub/byval_mismatch3.ll`, `ub/byval_null.ll`, `ub/byval_oversize.ll`, `ub/byval_poison.ll`, `ub/call_mismatched_signature.ll`, `ub/call_poison.ll` |
| **interpreter**: failed at `llvm.intr.assume` | `clean/assume_operand_bundles.ll`, `ub/assume_false.ll`, `ub/assume_invalid_align.ll`, `ub/assume_misalign.ll`, `ub/assume_non_pow2_align_offset.ll`, `ub/assume_nondereferenceable.ll`, `ub/assume_null.ll`, `ub/assume_poison.ll`, `ub/assume_poison_align.ll`, `ub/assume_pow2_align_offset.ll` |
| **interpreter**: failed at `llvm.mlir.constant` | `clean/bitcast_be.ll`, `clean/bitcast_le.ll`, `clean/intr_experimental_vector.ll`, `clean/intr_vector_manip.ll`, `clean/intr_vector_reduce.ll`, `clean/loadstore_overaligned.ll`, `clean/metadata.ll` |
| **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | `clean/fp_arith_bfloat.ll`, `clean/fp_arith_double.ll`, `clean/fp_arith_float.ll`, `clean/fp_arith_fp128.ll`, `clean/fp_arith_fp80.ll`, `clean/fp_arith_half.ll` |
| **interpreter**: failed at `llvm.mlir.poison` | `clean/intr_fp_fptoi_sat.ll`, `clean/intr_fp_is_fpclass.ll`, `clean/intr_fp_minmax.ll`, `clean/struct.ll` |
| **parser**: `vector element type expected` | `clean/gep.ll`, `clean/global_constexpr_initializer.ll`, `clean/vector.ll` |
| **verifier**: `llvm.add: Expected operand 0 to have integer type` | `clean/int_arith.ll`, `clean/inttoptr_ptrtoint_constantexpr.ll`, `clean/undef.ll` |
| **interpreter**: failed at `llvm.mlir.undef` | `clean/intr_arith_overflow.ll`, `ub/attribute_noundef_agg_ub.ll`, `ub/load_noundef_ub_poison_padding.ll` |
| **parser**: `Expected punctuation '}'` | `clean/ptrtoaddr.ll`, `ub/assume_misalign_all_ones.ll`, `ub/assume_null_all_ones.ll` |
| **interpreter**: failed at `llvm.fdiv` | `clean/fp_fastmath.ll`, `clean/fp_phi_select.ll` |
| **interpreter**: failed at `llvm.ptrtoaddr` | `clean/ptrtoaddr_after_ptrtoint.ll`, `ub/ptrtoaddr_no_expose.ll` |
| **interpreter**: failed at `llvm.intr.lifetime.start` | `ub/store_dead.ll`, `ub/store_dead_gep.ll` |
| **interpreter**: `unsupported value of global @g` | `clean/byval_padding.ll` |
| **verifier**: `llvm.sitofp: Expected operand 0 to have integer type` | `clean/fp_cast.ll` |
| **interpreter**: failed at `llvm.fcmp` | `clean/fp_cmp.ll` |
| **interpreter**: failed at `llvm.fadd` | `clean/fp_denorm.ll` |
| **verifier**: `llvm.icmp: Expected operand 0 to have integer or pointer type` | `clean/icmp_ptr.ll` |
| **verifier**: `llvm.intr.sadd.sat: Expected operand 0 to have integer type` | `clean/intr_arith_sat.ll` |
| **verifier**: `llvm.intr.bitreverse: Expected operand 0 to have integer type` | `clean/intr_bit_manip.ll` |
| **verifier**: `llvm.intr.fmuladd: Expected operand 0 to have floating point type` | `clean/intr_fp_fma.ll` |
| **verifier**: `llvm.intr.fabs: Expected operand 0 to have floating point type` | `clean/intr_fp_unary.ll` |
| **verifier**: `llvm.intr.abs: Expected operand 0 to have integer type` | `clean/intr_int_arith.ll` |
| **interpreter**: failed at `llvm.intr.memset.inline` | `clean/intr_memory.ll` |
| **interpreter**: failed at `llvm.intr.ssa.copy` | `clean/intr_passthrough.ll` |
| **interpreter**: failed at `llvm.intr.vscale` | `clean/intr_vscale.ll` |
| **interpreter**: failed at `llvm.inttoptr` | `clean/inttoptr.ll` |
| **interpreter**: failed at `llvm.alloca` | `ub/alloca_poison_count.ll` |
| **verifier**: `llvm.func: Expected the last operation of a block to be a terminator` | `ub/indirectbr_poison.ll` |
| **interpreter**: `unsupported value of global @constant_dst` | `ub/intr_memory_constant_ub.ll` |

</details>

## Tests

✅ and ❌ mark whether `veir-interpret` has the same result as `llubi` and `alive-exec`.

<details>
<summary>All 102 tests, those with a result first</summary>

| Test | veir-interpret | llubi | alive-exec |
| -- | -- | -- | -- |
| `clean/gep-16-bit-addrspace.ll` | `Program output: #[]` | ✅ `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/global_external.ll` | `Program output: #[]` | ✅ `Program output: #[]` | crashed |
| `clean/main2.ll` | `Program output: #[0x00000000#32]` | ✅ `Program output: #[0x00000000#32]` | ✅ `Program output: #[0x00000000#32]` |
| `clean/noalias_scope.ll` | `Program output: #[]` | ✅ `Program output: #[]` | rejected: `Unsupported type: metadata` |
| `ub/alloca_large_count.ll` | UB at `%1 = "llvm.alloca"(%0) <{alignment = 4 : i64, elem_type = i32}> : (i128) -> !llvm.ptr` (line 4) | ✅ `Immediate UB detected: Alloca with large array size that overflows uint64_t. Size: -1` | ✅ `UB triggered` |
| `ub/alloca_size_overflow.ll` | UB at `%1 = "llvm.alloca"(%0) <{alignment = 4 : i64, elem_type = i32}> : (i64) -> !llvm.ptr` (line 4) | ✅ `Immediate UB detected: Alloca with allocation size that overflows uint64_t. Size: -1` | ✅ `UB triggered` |
| `ub/br_poison.ll` | UB at `"llvm.cond_br"(%0)[^bb1, ^bb1] <{operandSegmentSizes = array<i32: 1, 0, 0>}> : (i1) -> ()` (line 4) | ✅ `Immediate UB detected: Branch on poison condition.` | rejected: `Error in SMT solver: memout` |
| `ub/global_constant_store.ll` | `Program output: #[]` | ❌ `Immediate UB detected: Try to write to a constant memory object: ptr 0x8 [@constant].` | ❌ `UB triggered` |
| `ub/inttoptr_generation.ll` | UB at `"llvm.store"(%2, %7) <{alignment = 4 : i64, ordering = 0 : i64}> : (i32, !llvm.ptr) -> ()` (line 12) | ✅ `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | failed: `Severe Z3 error` |
| `ub/inttoptr_generation2.ll` | UB at `"llvm.store"(%2, %9) <{alignment = 4 : i64, ordering = 0 : i64}> : (i32, !llvm.ptr) -> ()` (line 14) | ✅ `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | failed: `Severe Z3 error` |
| `ub/inttoptr_gep.ll` | `Program output: #[]` | ❌ `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | ❌ `UB triggered` |
| `ub/inttoptr_multiobj.ll` | UB at `"llvm.store"(%3, %11) <{alignment = 2 : i64, ordering = 0 : i64}> : (i16, !llvm.ptr) -> ()` (line 16) | ✅ `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | ✅ `UB triggered` |
| `ub/inttoptr_multiobj2.ll` | UB at `"llvm.store"(%1, %8) <{alignment = 4 : i64, ordering = 0 : i64}> : (i32, !llvm.ptr) -> ()` (line 14) | ✅ `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | ✅ `UB triggered` |
| `ub/inttoptr_oob.ll` | UB at `"llvm.store"(%3, %7) <{alignment = 4 : i64, ordering = 0 : i64}> : (i64, !llvm.ptr) -> ()` (line 13) | ✅ `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | ✅ `UB triggered` |
| `ub/inttoptr_oob2.ll` | UB at `"llvm.store"(%3, %8) <{alignment = 4 : i64, ordering = 0 : i64}> : (i64, !llvm.ptr) -> ()` (line 14) | ✅ `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | ✅ `UB triggered` |
| `ub/load_noundef_ub_poison.ll` | `Program output: #[]` | ❌ `Immediate UB detected: The value loaded contains undefined bits.` | ❌ `UB triggered` |
| `ub/load_noundef_ub_undef.ll` | `Program output: #[]` | ❌ `Immediate UB detected: The value loaded contains undefined bits.` | ❌ `UB triggered` |
| `ub/metadata_noundef_ub.ll` | `Program output: #[]` | ❌ `Immediate UB detected: The value poison violates !noundef metadata.` | ❌ `UB triggered` |
| `ub/switch_poison.ll` | UB at `"llvm.switch"(%0)[^bb1] <{case_operand_segments = array<i32>, operandSegmentSizes = array<i32: 1, 0, 0>}> : (i32) -> ()` (line 4) | ✅ `Immediate UB detected: Switch on poison condition.` | rejected: `Error in SMT solver: memout` |
| `ub/unreachable.ll` | UB at `"llvm.unreachable"() : () -> ()` (line 3) | ✅ `Immediate UB detected: Unreachable code.` | ✅ `UB triggered` |
| `clean/alloca.ll` | **interpreter**: failed at `llvm.call` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/assume_operand_bundles.ll` | **interpreter**: failed at `llvm.intr.assume` | `Program output: #[]` | rejected: `Unsupported instruction:   call void @llvm.assume(i1 true) [ "dereferenceable_or_null"(ptr %alloc, i32 4)` |
| `clean/bitcast_be.ll` | **interpreter**: failed at `llvm.mlir.constant` | `Program output: #[]` | rejected: `Unsupported type: b64` |
| `clean/bitcast_le.ll` | **interpreter**: failed at `llvm.mlir.constant` | `Program output: #[]` | rejected: `Unsupported type: b64` |
| `clean/byval.ll` | **interpreter**: failed at `llvm.call` | `Program output: #[]` | `UB triggered` |
| `clean/byval_padding.ll` | **interpreter**: `unsupported value of global @g` | `Program output: #[]` | crashed |
| `clean/fp_arith_bfloat.ll` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/fp_arith_double.ll` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/fp_arith_float.ll` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/fp_arith_fp128.ll` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/fp_arith_fp80.ll` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | `Program output: #[]` | rejected: `Unsupported type: x86_fp80` |
| `clean/fp_arith_half.ll` | **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/fp_cast.ll` | **verifier**: `llvm.sitofp: Expected operand 0 to have integer type` | `Program output: #[]` | crashed |
| `clean/fp_cmp.ll` | **interpreter**: failed at `llvm.fcmp` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/fp_denorm.ll` | **interpreter**: failed at `llvm.fadd` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/fp_fastmath.ll` | **interpreter**: failed at `llvm.fdiv` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/fp_phi_select.ll` | **interpreter**: failed at `llvm.fdiv` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/gep.ll` | **parser**: `vector element type expected` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/global_constexpr_initializer.ll` | **parser**: `vector element type expected` | `Program output: #[]` | rejected: `program doesn't type check!` |
| `clean/icmp_ptr.ll` | **verifier**: `llvm.icmp: Expected operand 0 to have integer or pointer type` | `Program output: #[]` | crashed |
| `clean/int_arith.ll` | **verifier**: `llvm.add: Expected operand 0 to have integer type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_arith_overflow.ll` | **interpreter**: failed at `llvm.mlir.undef` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_arith_sat.ll` | **verifier**: `llvm.intr.sadd.sat: Expected operand 0 to have integer type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_bit_manip.ll` | **verifier**: `llvm.intr.bitreverse: Expected operand 0 to have integer type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_experimental_vector.ll` | **interpreter**: failed at `llvm.mlir.constant` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_fp_fma.ll` | **verifier**: `llvm.intr.fmuladd: Expected operand 0 to have floating point type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_fp_fptoi_sat.ll` | **interpreter**: failed at `llvm.mlir.poison` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_fp_is_fpclass.ll` | **interpreter**: failed at `llvm.mlir.poison` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_fp_minmax.ll` | **interpreter**: failed at `llvm.mlir.poison` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_fp_unary.ll` | **verifier**: `llvm.intr.fabs: Expected operand 0 to have floating point type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_int_arith.ll` | **verifier**: `llvm.intr.abs: Expected operand 0 to have integer type` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_memory.ll` | **interpreter**: failed at `llvm.intr.memset.inline` | `Program output: #[]` | `UB triggered` |
| `clean/intr_passthrough.ll` | **interpreter**: failed at `llvm.intr.ssa.copy` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_vector_manip.ll` | **interpreter**: failed at `llvm.mlir.constant` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_vector_reduce.ll` | **interpreter**: failed at `llvm.mlir.constant` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/intr_vscale.ll` | **interpreter**: failed at `llvm.intr.vscale` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/inttoptr.ll` | **interpreter**: failed at `llvm.inttoptr` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/inttoptr_ptrtoint_constantexpr.ll` | **verifier**: `llvm.add: Expected operand 0 to have integer type` | `Program output: #[]` | crashed |
| `clean/loadstore_overaligned.ll` | **interpreter**: failed at `llvm.mlir.constant` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/metadata.ll` | **interpreter**: failed at `llvm.mlir.constant` | `Program output: #[]` | rejected: `Unsupported metadata: 47` |
| `clean/ptrtoaddr.ll` | **parser**: `Expected punctuation '}'` | `Program output: #[]` | rejected: `Unsupported instruction:   %wide1 = inttoptr i64 4294967301 to ptr addrspace(1)` |
| `clean/ptrtoaddr_after_ptrtoint.ll` | **interpreter**: failed at `llvm.ptrtoaddr` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/reset_return_value_slot.ll` | **interpreter**: failed at `llvm.call` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/struct.ll` | **interpreter**: failed at `llvm.mlir.poison` | `Program output: #[]` | failed: `Severe Z3 error` |
| `clean/undef.ll` | **verifier**: `llvm.add: Expected operand 0 to have integer type` | `Program output: #[]` | crashed |
| `clean/vector.ll` | **parser**: `vector element type expected` | `Program output: #[]` | failed: `Severe Z3 error` |
| `ub/alloca_poison_count.ll` | **interpreter**: failed at `llvm.alloca` | `Immediate UB detected: Alloca with poison array size.` | `UB triggered` |
| `ub/assume_false.ll` | **interpreter**: failed at `llvm.intr.assume` | `Immediate UB detected: Assume on false or poison condition.` | `UB triggered` |
| `ub/assume_invalid_align.ll` | **interpreter**: failed at `llvm.intr.assume` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates align(4294967296) assumption.` | `UB triggered` |
| `ub/assume_misalign.ll` | **interpreter**: failed at `llvm.intr.assume` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates align(2048) assumption.` | `UB triggered` |
| `ub/assume_misalign_all_ones.ll` | **parser**: `Expected punctuation '}'` | `Immediate UB detected: The pointer ptr 0xFFFFFFFFFFFFFFFF [nullary] violates align(2048) assumption.` | rejected: `Unsupported instruction:   call void @llvm.assume(i1 true) [ "align"(ptr addrspace(1) null, i32 2048) ]` |
| `ub/assume_non_pow2_align_offset.ll` | **interpreter**: failed at `llvm.intr.assume` | `Immediate UB detected: Assume on pointer ptr 0x8 [alloc] with a nonzero adjusted address and a non-power-of-two alignment 17.` | `UB triggered` |
| `ub/assume_nondereferenceable.ll` | **interpreter**: failed at `llvm.intr.assume` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates dereferenceable(2048) assumption.` | `UB triggered` |
| `ub/assume_null.ll` | **interpreter**: failed at `llvm.intr.assume` | `Immediate UB detected: The pointer ptr 0x0 [nullary] violates nonnull assumption.` | `UB triggered` |
| `ub/assume_null_all_ones.ll` | **parser**: `Expected punctuation '}'` | `Immediate UB detected: The pointer ptr 0xFFFFFFFFFFFFFFFF [nullary] violates nonnull assumption.` | rejected: `Unsupported instruction:   %res = load ptr addrspace(1), ptr %storage, align 8` |
| `ub/assume_poison.ll` | **interpreter**: failed at `llvm.intr.assume` | `Immediate UB detected: The value poison violates noundef attribute.` | `UB triggered` |
| `ub/assume_poison_align.ll` | **interpreter**: failed at `llvm.intr.assume` | `Immediate UB detected: Assume on poison pointer.` | `UB triggered` |
| `ub/assume_pow2_align_offset.ll` | **interpreter**: failed at `llvm.intr.assume` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates align(16) assumption.` | `UB triggered` |
| `ub/attribute_dereferenceable_ub_nullary_provenance.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: The value ptr 0xE82FEEACEEB98B3E [nullary] violates dereferenceable(4) attribute.` | `UB triggered` |
| `ub/attribute_dereferenceable_ub_oob1.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: The value ptr 0x8 [alloc] violates dereferenceable(8) attribute.` | `UB triggered` |
| `ub/attribute_dereferenceable_ub_oob2.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: The value ptr 0x7 [alloc + -1] violates dereferenceable(2) attribute.` | `UB triggered` |
| `ub/attribute_dereferenceable_ub_oob3.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: The value ptr 0xA [alloc + 2] violates dereferenceable(3) attribute.` | `UB triggered` |
| `ub/attribute_dereferenceable_ub_poison.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: The value poison violates dereferenceable(4) attribute.` | `UB triggered` |
| `ub/attribute_noundef_agg_ub.ll` | **interpreter**: failed at `llvm.mlir.undef` | `Immediate UB detected: The value { i32 0, poison } violates noundef attribute.` | rejected: `Unsupported attribute:` |
| `ub/attribute_noundef_ub.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: The value poison violates noundef attribute.` | `UB triggered` |
| `ub/byval_lifetime.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Try to access a dead memory object at address 0x10.` | failed: `Severe Z3 error` |
| `ub/byval_misalign.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Misaligned memory access. Address: 0x8, Required alignment: 16.` | `UB triggered` |
| `ub/byval_misalign_callsite.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Misaligned memory access. Address: 0x8, Required alignment: 16.` | `UB triggered` |
| `ub/byval_mismatch1.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Mismatched byval attribute between callee and callsite.` | failed: `Severe Z3 error` |
| `ub/byval_mismatch2.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Mismatched byval attribute between callee and callsite.` | failed: `Severe Z3 error` |
| `ub/byval_mismatch3.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Mismatched byval attribute between callee and callsite.` | failed: `Severe Z3 error` |
| `ub/byval_null.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `UB triggered` |
| `ub/byval_oversize.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Memory access is out of bounds. Accessed size: 4, Address: 0x8, Object base: 0x8, Object size: 1.` | `UB triggered` |
| `ub/byval_poison.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Invalid poison byval pointer argument.` | `UB triggered` |
| `ub/call_mismatched_signature.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Indirect call through a function pointer with mismatched signature. Expected: void (), Actual: i32 ()` | failed: `Severe Z3 error` |
| `ub/call_poison.ll` | **interpreter**: failed at `llvm.call` | `Immediate UB detected: Indirect call through poison function pointer.` | `UB triggered` |
| `ub/indirectbr_poison.ll` | **verifier**: `llvm.func: Expected the last operation of a block to be a terminator` | `Immediate UB detected: Indirect branch on poison.` | rejected: `Unsupported instruction:   indirectbr ptr poison, [label %exit]` |
| `ub/intr_memory_constant_ub.ll` | **interpreter**: `unsupported value of global @constant_dst` | `Immediate UB detected: Try to write to a constant memory object: ptr 0x8 [@constant_dst].` | `UB triggered` |
| `ub/load_noundef_ub_poison_padding.ll` | **interpreter**: failed at `llvm.mlir.undef` | `Immediate UB detected: The value loaded contains undefined bits.` | `UB triggered` |
| `ub/ptrtoaddr_no_expose.ll` | **interpreter**: failed at `llvm.ptrtoaddr` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | failed: `Severe Z3 error` |
| `ub/store_dead.ll` | **interpreter**: failed at `llvm.intr.lifetime.start` | `Immediate UB detected: Try to access a dead memory object at address 0x8.` | `UB triggered` |
| `ub/store_dead_gep.ll` | **interpreter**: failed at `llvm.intr.lifetime.start` | `Immediate UB detected: Try to access a dead memory object at address 0x9.` | `UB triggered` |

</details>

## Manifest

| Component | Version | SHA-256 |
| -- | -- | -- |
| veir-interpret | [`1d28db9d434d`](https://github.com/opencompl/veir/commit/1d28db9d434d8bec78a006eafbaa86ec5db0cf23) | `8bb049d0ed87499878b5f8e9f2b7bd2caae0d045c1b1d41a5294df3502f4ba85` |
| alive-exec | version v21.0-118-gd1533abb-dirty | `f7498df7a22508f22fd2de3f81e08ed5a3214c8e9e8e4555fad8db050a6b83d1` |
| llubi | LLVM version 23.1.0-rc1 | `1acd08617c94e77035ea3dbd8e3ad270ae1f73bafcabef884e981cffb834fce2` |
| mlir-translate | LLVM version 23.1.0-rc1 | `34403b40057d9708b425463f45d84a2c239dc15264da6c1e63ce1973ff975bb8` |
| corpus.tar.gz |  | `9c27c23fe92d74578bd24f656e76dce8643f6bc90f762be31d2b25d21004a2f1` |
