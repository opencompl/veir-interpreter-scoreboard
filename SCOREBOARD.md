# Veir-Interpreter Scoreboard

We run `veir-interpret` on the 102 tests in `llubi-tests` and compare with the
results of `llubi`.

| Verdict | Tests |
|---|---:|
| PASS | 7 (6.9%) |
| MISMATCH | 3 (2.9%) |
| UNSUPPORTED | 92 (90.2%) |
| TIMEOUT | 0 (0.0%) |

## Mismatches

`veir-interpret` fully executed these tests, but has a different result than `llubi`!

| Test | llubi | veir-interpret | Verdict |
|---|---|---|---|
| `ub/load_noundef_ub_poison.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | returned `void` | MISMATCH |
| `ub/load_noundef_ub_undef.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | returned `void` | MISMATCH |
| `ub/metadata_noundef_ub.ll` | `Immediate UB detected: The value poison violates !noundef metadata.` | returned `void` | MISMATCH |

## Unsupported

| Reason | Count | Tests |
|---|---:|---|
| **interpreter**: failed at `llvm.call` | 19 | `clean/alloca.ll`, `clean/byval.ll`, `clean/reset_return_value_slot.ll`, `ub/attribute_dereferenceable_ub_nullary_provenance.ll`, `ub/attribute_dereferenceable_ub_oob1.ll`, `ub/attribute_dereferenceable_ub_oob2.ll`, `ub/attribute_dereferenceable_ub_oob3.ll`, `ub/attribute_dereferenceable_ub_poison.ll`, `ub/attribute_noundef_ub.ll`, `ub/byval_lifetime.ll`, `ub/byval_misalign.ll`, `ub/byval_misalign_callsite.ll`, `ub/byval_mismatch1.ll`, `ub/byval_mismatch2.ll`, `ub/byval_mismatch3.ll`, `ub/byval_null.ll`, `ub/byval_oversize.ll`, `ub/byval_poison.ll`, `ub/call_poison.ll` |
| **interpreter**: failed at `llvm.intr.assume` | 8 | `clean/assume_operand_bundles.ll`, `ub/assume_false.ll`, `ub/assume_invalid_align.ll`, `ub/assume_misalign.ll`, `ub/assume_nondereferenceable.ll`, `ub/assume_null.ll`, `ub/assume_poison.ll`, `ub/assume_poison_align.ll` |
| **interpreter**: failed at `llvm.mlir.constant` | 7 | `clean/bitcast_be.ll`, `clean/bitcast_le.ll`, `clean/intr_experimental_vector.ll`, `clean/intr_vector_manip.ll`, `clean/intr_vector_reduce.ll`, `clean/loadstore_overaligned.ll`, `clean/metadata.ll` |
| **interpreter**: failed at `llvm.ptrtoint` | 7 | `clean/ptrtoaddr_after_ptrtoint.ll`, `ub/inttoptr_generation2.ll`, `ub/inttoptr_gep.ll`, `ub/inttoptr_multiobj.ll`, `ub/inttoptr_multiobj2.ll`, `ub/inttoptr_oob.ll`, `ub/inttoptr_oob2.ll` |
| **verifier**: `llvm.fadd: Expected operand 0 to have floating point type` | 6 | `clean/fp_arith_bfloat.ll`, `clean/fp_arith_double.ll`, `clean/fp_arith_float.ll`, `clean/fp_arith_fp128.ll`, `clean/fp_arith_fp80.ll`, `clean/fp_arith_half.ll` |
| **interpreter**: failed at `llvm.mlir.addressof` | 5 | `clean/byval_padding.ll`, `clean/global_external.ll`, `ub/call_mismatched_signature.ll`, `ub/global_constant_store.ll`, `ub/intr_memory_constant_ub.ll` |
| **interpreter**: failed at `llvm.mlir.poison` | 4 | `clean/intr_fp_fptoi_sat.ll`, `clean/intr_fp_is_fpclass.ll`, `clean/intr_fp_minmax.ll`, `clean/struct.ll` |
| **interpreter**: failed at `llvm.inttoptr` | 4 | `clean/inttoptr.ll`, `ub/assume_non_pow2_align_offset.ll`, `ub/assume_pow2_align_offset.ll`, `ub/inttoptr_generation.ll` |
| **parser**: `vector element type expected` | 3 | `clean/gep.ll`, `clean/global_constexpr_initializer.ll`, `clean/vector.ll` |
| **verifier**: `llvm.add: Expected operand 0 to have integer type` | 3 | `clean/int_arith.ll`, `clean/inttoptr_ptrtoint_constantexpr.ll`, `clean/undef.ll` |
| **interpreter**: failed at `llvm.mlir.undef` | 3 | `clean/intr_arith_overflow.ll`, `ub/attribute_noundef_agg_ub.ll`, `ub/load_noundef_ub_poison_padding.ll` |
| **parser**: `Expected punctuation '}'` | 3 | `clean/ptrtoaddr.ll`, `ub/assume_misalign_all_ones.ll`, `ub/assume_null_all_ones.ll` |
| **interpreter**: failed at `llvm.fdiv` | 2 | `clean/fp_fastmath.ll`, `clean/fp_phi_select.ll` |
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
| **interpreter**: failed at `llvm.intr.memset` | 1 | `clean/intr_memory.ll` |
| **interpreter**: failed at `llvm.intr.ssa.copy` | 1 | `clean/intr_passthrough.ll` |
| **interpreter**: failed at `llvm.intr.vscale` | 1 | `clean/intr_vscale.ll` |
| **interpreter**: failed at `llvm.alloca` | 1 | `ub/alloca_poison_count.ll` |
| **verifier**: `llvm.func: Expected the last operation of a block to be a terminator` | 1 | `ub/indirectbr_poison.ll` |
| **interpreter**: failed at `llvm.ptrtoaddr` | 1 | `ub/ptrtoaddr_no_expose.ll` |

## All tests

<details>
<summary>Show all tests</summary>

| Test | llubi | veir-interpret | Verdict |
|---|---|---|---|
| `clean/alloca.ll` | returned `void` | `Error while interpreting module at: %21 = "llvm.call"() <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "callee" = @count, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 0, 0>}> : () -> i32` | UNSUPPORTED |
| `clean/assume_operand_bundles.ll` | returned `void` | `Error while interpreting module at: "llvm.intr.assume"(%18, %24) <{"op_bundle_sizes" = array<i32: 1>, "op_bundle_tags" = ["nonnull"]}> : (i1, !llvm.ptr) -> ()` | UNSUPPORTED |
| `clean/bitcast_be.ll` | returned `void` | `Error while interpreting module at: %14 = "llvm.mlir.constant"() <{"value" = dense<[0, 1]> : vector<2xi32>}> : () -> vector<2xi32>` | UNSUPPORTED |
| `clean/bitcast_le.ll` | returned `void` | `Error while interpreting module at: %14 = "llvm.mlir.constant"() <{"value" = dense<[0, 1]> : vector<2xi32>}> : () -> vector<2xi32>` | UNSUPPORTED |
| `clean/byval.ll` | returned `void` | `Error while interpreting module at: "llvm.call"(%27) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "arg_attrs" = [{"llvm.byval" = i32}], "callee" = @write, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `clean/byval_padding.ll` | returned `void` | `Error while interpreting module at: %23 = "llvm.mlir.addressof"() <{"global_name" = @g}> : () -> !llvm.ptr` | UNSUPPORTED |
| `clean/fp_arith_bfloat.ll` | returned `void` | `Error verifying input program: llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_double.ll` | returned `void` | `Error verifying input program: llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_float.ll` | returned `void` | `Error verifying input program: llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_fp128.ll` | returned `void` | `Error verifying input program: llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_fp80.ll` | returned `void` | `Error verifying input program: llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_arith_half.ll` | returned `void` | `Error verifying input program: llvm.fadd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/fp_cast.ll` | returned `void` | `Error verifying input program: llvm.sitofp: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/fp_cmp.ll` | returned `void` | `Error while interpreting module at: %10 = "llvm.fcmp"(%7, %7) <{"fastmathFlags" = #llvm.fastmath<none>, "predicate" = 1 : i64}> : (f32, f32) -> i1` | UNSUPPORTED |
| `clean/fp_denorm.ll` | returned `void` | `Error while interpreting module at: %10 = "llvm.fadd"(%7, %8) <{"fastmathFlags" = #llvm.fastmath<none>}> : (f32, f32) -> f32` | UNSUPPORTED |
| `clean/fp_fastmath.ll` | returned `void` | `Error while interpreting module at: %11 = "llvm.fdiv"(%7, %7) <{"fastmathFlags" = #llvm.fastmath<nnan>}> : (f32, f32) -> f32` | UNSUPPORTED |
| `clean/fp_phi_select.ll` | returned `void` | `Error while interpreting module at: %11 = "llvm.fdiv"(%7, %7) <{"fastmathFlags" = #llvm.fastmath<none>}> : (f32, f32) -> f32` | UNSUPPORTED |
| `clean/gep-16-bit-addrspace.ll` | returned `void` | `Error while interpreting module at: %10 = "llvm.getelementptr"(%9, %8) <{"elem_type" = !llvm.struct<"s", (array<65536 x i8>, i8)>, "noWrapFlags" = 0 : i32, "rawConstantIndices" = array<i32: -2147483648, 1>}> : (!llvm.ptr, i32) -> !llvm.ptr` | UNSUPPORTED |
| `clean/gep.ll` | returned `void` | `Error: corpus/llubi-tests/clean/gep.mlir:46:62: error: vector element type expected` | UNSUPPORTED |
| `clean/global_constexpr_initializer.ll` | returned `void` | `Error: corpus/llubi-tests/clean/global_constexpr_initializer.mlir:128:45: error: vector element type expected` | UNSUPPORTED |
| `clean/global_external.ll` | returned `void` | `Error while interpreting module at: %14 = "llvm.mlir.addressof"() <{"global_name" = @external_ptr}> : () -> !llvm.ptr` | UNSUPPORTED |
| `clean/icmp_ptr.ll` | returned `void` | `Error verifying input program: llvm.icmp: Expected operand 0 to have integer or pointer type` | UNSUPPORTED |
| `clean/int_arith.ll` | returned `void` | `Error verifying input program: llvm.add: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/intr_arith_overflow.ll` | returned `void` | `Error while interpreting module at: %12 = "llvm.mlir.undef"() : () -> vector<2xi32>` | UNSUPPORTED |
| `clean/intr_arith_sat.ll` | returned `void` | `Error verifying input program: llvm.intr.sadd.sat: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/intr_bit_manip.ll` | returned `void` | `Error verifying input program: llvm.intr.bitreverse: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/intr_experimental_vector.ll` | returned `void` | `Error while interpreting module at: %9 = "llvm.mlir.constant"() <{"value" = dense<[false, false, true, false]> : vector<4xi1>}> : () -> vector<4xi1>` | UNSUPPORTED |
| `clean/intr_fp_fma.ll` | returned `void` | `Error verifying input program: llvm.intr.fmuladd: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/intr_fp_fptoi_sat.ll` | returned `void` | `Error while interpreting module at: %11 = "llvm.mlir.poison"() : () -> f32` | UNSUPPORTED |
| `clean/intr_fp_is_fpclass.ll` | returned `void` | `Error while interpreting module at: %18 = "llvm.mlir.poison"() : () -> f32` | UNSUPPORTED |
| `clean/intr_fp_minmax.ll` | returned `void` | `Error while interpreting module at: %13 = "llvm.mlir.poison"() : () -> f32` | UNSUPPORTED |
| `clean/intr_fp_unary.ll` | returned `void` | `Error verifying input program: llvm.intr.fabs: Expected operand 0 to have floating point type` | UNSUPPORTED |
| `clean/intr_int_arith.ll` | returned `void` | `Error verifying input program: llvm.intr.abs: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/intr_memory.ll` | returned `void` | `Error while interpreting module at: "llvm.intr.memset"(%27, %8, %9) <{"isVolatile" = 0 : i1}> : (!llvm.ptr, i8, i16) -> ()` | UNSUPPORTED |
| `clean/intr_passthrough.ll` | returned `void` | `Error while interpreting module at: %10 = "llvm.intr.ssa.copy"(%7) : (i32) -> i32` | UNSUPPORTED |
| `clean/intr_vector_manip.ll` | returned `void` | `Error while interpreting module at: %7 = "llvm.mlir.constant"() <{"value" = dense<[0, 1, 2, 3, 4, 5]> : vector<6xi32>}> : () -> vector<6xi32>` | UNSUPPORTED |
| `clean/intr_vector_reduce.ll` | returned `void` | `Error while interpreting module at: %7 = "llvm.mlir.constant"() <{"value" = dense<[1, 2, 3, 4]> : vector<4xi32>}> : () -> vector<4xi32>` | UNSUPPORTED |
| `clean/intr_vscale.ll` | returned `void` | `Error while interpreting module at: %7 = "llvm.intr.vscale"() : () -> i32` | UNSUPPORTED |
| `clean/inttoptr.ll` | returned `void` | `Error while interpreting module at: %11 = "llvm.inttoptr"(%7) : (i64) -> !llvm.ptr` | UNSUPPORTED |
| `clean/inttoptr_ptrtoint_constantexpr.ll` | returned `void` | `Error verifying input program: llvm.add: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/loadstore_overaligned.ll` | returned `void` | `Error while interpreting module at: %9 = "llvm.mlir.constant"() <{"value" = dense<0> : vector<4xi32>}> : () -> vector<4xi32>` | UNSUPPORTED |
| `clean/main2.ll` | returned `i32 0` | returned `i32 0` | PASS |
| `clean/metadata.ll` | returned `void` | `Error while interpreting module at: %22 = "llvm.mlir.constant"() <{"value" = dense<[0, 1, 2, 3, 4, 5, 6, 7]> : vector<8xi32>}> : () -> vector<8xi32>` | UNSUPPORTED |
| `clean/noalias_scope.ll` | returned `void` | returned `void` | PASS |
| `clean/ptrtoaddr.ll` | returned `void` | `Error: corpus/llubi-tests/clean/ptrtoaddr.mlir:5:50: error: Expected punctuation '}'` | UNSUPPORTED |
| `clean/ptrtoaddr_after_ptrtoint.ll` | returned `void` | `Error while interpreting module at: %10 = "llvm.ptrtoint"(%9) : (!llvm.ptr) -> i64` | UNSUPPORTED |
| `clean/reset_return_value_slot.ll` | returned `void` | `Error while interpreting module at: %7 = "llvm.call"() <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "callee" = @func1, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 0, 0>}> : () -> i16` | UNSUPPORTED |
| `clean/struct.ll` | returned `void` | `Error while interpreting module at: %7 = "llvm.mlir.poison"() : () -> !llvm.struct<(i32, i32)>` | UNSUPPORTED |
| `clean/undef.ll` | returned `void` | `Error verifying input program: llvm.add: Expected operand 0 to have integer type` | UNSUPPORTED |
| `clean/vector.ll` | returned `void` | `Error: corpus/llubi-tests/clean/vector.mlir:9:46: error: vector element type expected` | UNSUPPORTED |
| `ub/alloca_large_count.ll` | `Immediate UB detected: Alloca with large array size that overflows uint64_t. Size: -1` | `Undefined behavior at: %8 = "llvm.alloca"(%7) <{"alignment" = 4 : i64, "elem_type" = i32}> : (i128) -> !llvm.ptr` | PASS |
| `ub/alloca_poison_count.ll` | `Immediate UB detected: Alloca with poison array size.` | `Error while interpreting module at: %8 = "llvm.alloca"(%7) <{"alignment" = 4 : i64, "elem_type" = i32}> : (i32) -> !llvm.ptr` | UNSUPPORTED |
| `ub/alloca_size_overflow.ll` | `Immediate UB detected: Alloca with allocation size that overflows uint64_t. Size: -1` | `Undefined behavior at: %8 = "llvm.alloca"(%7) <{"alignment" = 4 : i64, "elem_type" = i32}> : (i64) -> !llvm.ptr` | PASS |
| `ub/assume_false.ll` | `Immediate UB detected: Assume on false or poison condition.` | `Error while interpreting module at: "llvm.intr.assume"(%7) <{"op_bundle_sizes" = array<i32>, "op_bundle_tags" = []}> : (i1) -> ()` | UNSUPPORTED |
| `ub/assume_invalid_align.ll` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates align(4294967296) assumption.` | `Error while interpreting module at: "llvm.intr.assume"(%8, %9, %10) <{"op_bundle_sizes" = array<i32: 2>, "op_bundle_tags" = ["align"]}> : (i1, !llvm.ptr, i64) -> ()` | UNSUPPORTED |
| `ub/assume_misalign.ll` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates align(2048) assumption.` | `Error while interpreting module at: "llvm.intr.assume"(%8, %10, %9) <{"op_bundle_sizes" = array<i32: 2>, "op_bundle_tags" = ["align"]}> : (i1, !llvm.ptr, i32) -> ()` | UNSUPPORTED |
| `ub/assume_misalign_all_ones.ll` | `Immediate UB detected: The pointer ptr 0xFFFFFFFFFFFFFFFF [nullary] violates align(2048) assumption.` | `Error: corpus/llubi-tests/ub/assume_misalign_all_ones.mlir:4:46: error: Expected punctuation '}'` | UNSUPPORTED |
| `ub/assume_non_pow2_align_offset.ll` | `Immediate UB detected: Assume on pointer ptr 0x8 [alloc] with a nonzero adjusted address and a non-power-of-two alignment 17.` | `Error while interpreting module at: %16 = "llvm.inttoptr"(%8) : (i64) -> !llvm.ptr` | UNSUPPORTED |
| `ub/assume_nondereferenceable.ll` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates dereferenceable(2048) assumption.` | `Error while interpreting module at: "llvm.intr.assume"(%8, %10, %9) <{"op_bundle_sizes" = array<i32: 2>, "op_bundle_tags" = ["dereferenceable"]}> : (i1, !llvm.ptr, i32) -> ()` | UNSUPPORTED |
| `ub/assume_null.ll` | `Immediate UB detected: The pointer ptr 0x0 [nullary] violates nonnull assumption.` | `Error while interpreting module at: "llvm.intr.assume"(%7, %8) <{"op_bundle_sizes" = array<i32: 1>, "op_bundle_tags" = ["nonnull"]}> : (i1, !llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/assume_null_all_ones.ll` | `Immediate UB detected: The pointer ptr 0xFFFFFFFFFFFFFFFF [nullary] violates nonnull assumption.` | `Error: corpus/llubi-tests/ub/assume_null_all_ones.mlir:8:96: error: Expected punctuation '}'` | UNSUPPORTED |
| `ub/assume_poison.ll` | `Immediate UB detected: The value poison violates noundef attribute.` | `Error while interpreting module at: "llvm.intr.assume"(%7) <{"op_bundle_sizes" = array<i32>, "op_bundle_tags" = []}> : (i1) -> ()` | UNSUPPORTED |
| `ub/assume_poison_align.ll` | `Immediate UB detected: Assume on poison pointer.` | `Error while interpreting module at: "llvm.intr.assume"(%7, %8, %9) <{"op_bundle_sizes" = array<i32: 2>, "op_bundle_tags" = ["align"]}> : (i1, !llvm.ptr, i32) -> ()` | UNSUPPORTED |
| `ub/assume_pow2_align_offset.ll` | `Immediate UB detected: The pointer ptr 0x8 [alloc] violates align(16) assumption.` | `Error while interpreting module at: %17 = "llvm.inttoptr"(%8) : (i64) -> !llvm.ptr` | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_nullary_provenance.ll` | `Immediate UB detected: The value ptr 0xE82FEEACEEB98B3E [nullary] violates dereferenceable(4) attribute.` | `Error while interpreting module at: "llvm.call"(%13) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_oob1.ll` | `Immediate UB detected: The value ptr 0x8 [alloc] violates dereferenceable(8) attribute.` | `Error while interpreting module at: "llvm.call"(%12) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_oob2.ll` | `Immediate UB detected: The value ptr 0x7 [alloc + -1] violates dereferenceable(2) attribute.` | `Error while interpreting module at: "llvm.call"(%14) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_oob3.ll` | `Immediate UB detected: The value ptr 0xA [alloc + 2] violates dereferenceable(3) attribute.` | `Error while interpreting module at: "llvm.call"(%14) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/attribute_dereferenceable_ub_poison.ll` | `Immediate UB detected: The value poison violates dereferenceable(4) attribute.` | `Error while interpreting module at: "llvm.call"(%11) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/attribute_noundef_agg_ub.ll` | `Immediate UB detected: The value { i32 0, poison } violates noundef attribute.` | `Error while interpreting module at: %13 = "llvm.mlir.undef"() : () -> !llvm.struct<(i32, i32)>` | UNSUPPORTED |
| `ub/attribute_noundef_ub.ll` | `Immediate UB detected: The value poison violates noundef attribute.` | `Error while interpreting module at: "llvm.call"(%11) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (i32) -> ()` | UNSUPPORTED |
| `ub/br_poison.ll` | `Immediate UB detected: Branch on poison condition.` | `Undefined behavior at: "llvm.cond_br"(%7) [^8, ^8] <{"operandSegmentSizes" = array<i32: 1, 0, 0>}> : (i1) -> ()` | PASS |
| `ub/byval_lifetime.ll` | `Immediate UB detected: Try to access a dead memory object at address 0x10.` | `Error while interpreting module at: %14 = "llvm.call"(%13) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "arg_attrs" = [{"llvm.byval" = i32}], "callee" = @identity, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> !llvm.ptr` | UNSUPPORTED |
| `ub/byval_misalign.ll` | `Immediate UB detected: Misaligned memory access. Address: 0x8, Required alignment: 16.` | `Error while interpreting module at: "llvm.call"(%12) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "arg_attrs" = [{"llvm.byval" = i32}], "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/byval_misalign_callsite.ll` | `Immediate UB detected: Misaligned memory access. Address: 0x8, Required alignment: 16.` | `Error while interpreting module at: "llvm.call"(%12) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "arg_attrs" = [{"llvm.align" = 16 : i64, "llvm.byval" = i32}], "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/byval_mismatch1.ll` | `Immediate UB detected: Mismatched byval attribute between callee and callsite.` | `Error while interpreting module at: "llvm.call"(%12) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/byval_mismatch2.ll` | `Immediate UB detected: Mismatched byval attribute between callee and callsite.` | `Error while interpreting module at: "llvm.call"(%12) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "arg_attrs" = [{"llvm.byval" = i32}], "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/byval_mismatch3.ll` | `Immediate UB detected: Mismatched byval attribute between callee and callsite.` | `Error while interpreting module at: "llvm.call"(%12) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "arg_attrs" = [{"llvm.byval" = i32}], "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/byval_null.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `Error while interpreting module at: "llvm.call"(%11) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "arg_attrs" = [{"llvm.byval" = i32}], "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/byval_oversize.ll` | `Immediate UB detected: Memory access is out of bounds. Accessed size: 4, Address: 0x8, Object base: 0x8, Object size: 1.` | `Error while interpreting module at: "llvm.call"(%12) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "arg_attrs" = [{"llvm.byval" = i32}], "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/byval_poison.ll` | `Immediate UB detected: Invalid poison byval pointer argument.` | `Error while interpreting module at: "llvm.call"(%11) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "arg_attrs" = [{"llvm.byval" = i32}], "callee" = @callee, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/call_mismatched_signature.ll` | `Immediate UB detected: Indirect call through a function pointer with mismatched signature. Expected: void (), Actual: i32 ()` | `Error while interpreting module at: %12 = "llvm.mlir.addressof"() <{"global_name" = @foo}> : () -> !llvm.ptr` | UNSUPPORTED |
| `ub/call_poison.ll` | `Immediate UB detected: Indirect call through poison function pointer.` | `Error while interpreting module at: "llvm.call"(%7) <{"CConv" = #llvm.cconv<ccc>, "TailCallKind" = #llvm.tailcallkind<none>, "fastmathFlags" = #llvm.fastmath<none>, "op_bundle_sizes" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0>}> : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/global_constant_store.ll` | `Immediate UB detected: Try to write to a constant memory object: ptr 0x8 [@constant].` | `Error while interpreting module at: %10 = "llvm.mlir.addressof"() <{"global_name" = @constant}> : () -> !llvm.ptr` | UNSUPPORTED |
| `ub/indirectbr_poison.ll` | `Immediate UB detected: Indirect branch on poison.` | `Error verifying input program: llvm.func: Expected the last operation of a block to be a terminator` | UNSUPPORTED |
| `ub/intr_memory_constant_ub.ll` | `Immediate UB detected: Try to write to a constant memory object: ptr 0x8 [@constant_dst].` | `Error while interpreting module at: %9 = "llvm.mlir.addressof"() <{"global_name" = @constant_dst}> : () -> !llvm.ptr` | UNSUPPORTED |
| `ub/inttoptr_generation.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `Error while interpreting module at: %11 = "llvm.inttoptr"(%8) : (i64) -> !llvm.ptr` | UNSUPPORTED |
| `ub/inttoptr_generation2.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `Error while interpreting module at: %12 = "llvm.ptrtoint"(%11) : (!llvm.ptr) -> i64` | UNSUPPORTED |
| `ub/inttoptr_gep.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `Error while interpreting module at: %12 = "llvm.ptrtoint"(%10) : (!llvm.ptr) -> i64` | UNSUPPORTED |
| `ub/inttoptr_multiobj.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `Error while interpreting module at: %13 = "llvm.ptrtoint"(%11) : (!llvm.ptr) -> i64` | UNSUPPORTED |
| `ub/inttoptr_multiobj2.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `Error while interpreting module at: %11 = "llvm.ptrtoint"(%9) : (!llvm.ptr) -> i64` | UNSUPPORTED |
| `ub/inttoptr_oob.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `Error while interpreting module at: %12 = "llvm.ptrtoint"(%11) : (!llvm.ptr) -> i64` | UNSUPPORTED |
| `ub/inttoptr_oob2.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `Error while interpreting module at: %13 = "llvm.ptrtoint"(%11) : (!llvm.ptr) -> i64` | UNSUPPORTED |
| `ub/load_noundef_ub_poison.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | returned `void` | MISMATCH |
| `ub/load_noundef_ub_poison_padding.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | `Error while interpreting module at: %10 = "llvm.mlir.undef"() : () -> vector<2xi4>` | UNSUPPORTED |
| `ub/load_noundef_ub_undef.ll` | `Immediate UB detected: The value loaded contains undefined bits.` | returned `void` | MISMATCH |
| `ub/metadata_noundef_ub.ll` | `Immediate UB detected: The value poison violates !noundef metadata.` | returned `void` | MISMATCH |
| `ub/ptrtoaddr_no_expose.ll` | `Immediate UB detected: Invalid memory access via a pointer with nullary provenance.` | `Error while interpreting module at: %10 = "llvm.ptrtoaddr"(%9) : (!llvm.ptr) -> i64` | UNSUPPORTED |
| `ub/store_dead.ll` | `Immediate UB detected: Try to access a dead memory object at address 0x8.` | `Error while interpreting module at: "llvm.intr.lifetime.start"(%9) : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/store_dead_gep.ll` | `Immediate UB detected: Try to access a dead memory object at address 0x9.` | `Error while interpreting module at: "llvm.intr.lifetime.start"(%10) : (!llvm.ptr) -> ()` | UNSUPPORTED |
| `ub/switch_poison.ll` | `Immediate UB detected: Switch on poison condition.` | `Undefined behavior at: "llvm.switch"(%7) [^8] <{"case_operand_segments" = array<i32>, "operandSegmentSizes" = array<i32: 1, 0, 0>}> : (i32) -> ()` | PASS |
| `ub/unreachable.ll` | `Immediate UB detected: Unreachable code.` | `Undefined behavior at: "llvm.unreachable"() : () -> ()` | PASS |

</details>

## Manifest

| Component | Version | SHA-256 |
|---|---|---|
| veir-interpret | [`cf8ccdb49e6c`](https://github.com/opencompl/veir/commit/cf8ccdb49e6cec14f7ec3214f0fb799234f902bd) | `9c66a2a9e6b7bbaad4bc2b68424a6bdf5dd66b33640e87ddeecf4934477e51bc` |
| llubi | LLVM version 23.1.0-rc1 | `1acd08617c94e77035ea3dbd8e3ad270ae1f73bafcabef884e981cffb834fce2` |
| mlir-translate | LLVM version 23.1.0-rc1 | `34403b40057d9708b425463f45d84a2c239dc15264da6c1e63ce1973ff975bb8` |
| corpus.tar.gz |  | `c81112457ef97ba8597d761fe5b3bad8c3197b2ff4b2bdf8a9dc9d7cbf5ca5d7` |
