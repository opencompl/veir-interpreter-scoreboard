################################################################################
# Configuration
################################################################################

VEIR_DIR ?= veir
CFLAGS ?= -O3 -fno-vectorize -fno-slp-vectorize

CLANG ?= clang
LLVM_LINK ?= llvm-link
OPT ?= opt
MLIR_TRANSLATE ?= mlir-translate
MLIR_OPT ?= mlir-opt
LLVM_PROFDATA ?= llvm-profdata
UV ?= uv
TAR ?= tar

SQLITE_LDLIBS := -ldl -lpthread -lm

################################################################################
# Layout
################################################################################

CORPUS := corpus
HARNESS_DIRS := minimal-harnesses sqlite-harnesses

HARNESSES := $(sort $(shell find $(HARNESS_DIRS) -type f -name '*.c'))
NAMES := $(HARNESSES:.c=)
MLIR := $(addprefix $(CORPUS)/,$(addsuffix .mlir,$(NAMES)))
LLVM_PROFILES := $(addprefix $(CORPUS)/,$(addsuffix .llvm-profile.csv,$(NAMES)))
VEIR_STATUSES := $(addprefix $(CORPUS)/,$(addsuffix .veir-status,$(NAMES)))

LLVM_STATS := $(CORPUS)/llvm-profile.csv
ARCHIVE := corpus.tar.gz
ARCHIVE_CONTENTS := $(patsubst $(CORPUS)/%,%,$(MLIR) $(LLVM_STATS))
MANIFEST := manifest.json
SCOREBOARD := SCOREBOARD.md

################################################################################
# Basic Make Behavior
################################################################################

.DEFAULT_GOAL := scoreboard

.DELETE_ON_ERROR:
.SECONDARY:

.PHONY: \
	refresh-corpus \
	check-corpus \
	unpack-corpus \
	veir-output \
	scoreboard \
	print-python-config \
	clean \
	FORCE

################################################################################
# Public Targets
################################################################################

refresh-corpus: $(ARCHIVE) scripts/corpus_manifest.py
	$(UV) run scripts/corpus_manifest.py manifest \
		--archive $(ARCHIVE) \
		--manifest $(MANIFEST)

check-corpus: scripts/corpus_manifest.py
	$(UV) run scripts/corpus_manifest.py check \
		--archive $(ARCHIVE) \
		--manifest $(MANIFEST)

unpack-corpus: check-corpus
	@mkdir -p $(CORPUS)
	$(TAR) --extract --gzip --file=$(ARCHIVE) --directory=$(CORPUS)

veir-output: $(VEIR_STATUSES)

scoreboard: check-corpus veir-output scripts/bench.py
	$(UV) run scripts/bench.py scoreboard \
		--corpus $(CORPUS) \
		--veir-source $(VEIR_DIR) \
		--output $(SCOREBOARD)

print-python-config:
	@printf '%s\n' \
		'clang=$(CLANG)' \
		'llvm_link=$(LLVM_LINK)' \
		'opt=$(OPT)' \
		'mlir_translate=$(MLIR_TRANSLATE)' \
		'mlir_opt=$(MLIR_OPT)' \
		'llvm_profdata=$(LLVM_PROFDATA)' \
		'cflags=$(CFLAGS)' \
		'harnesses=$(HARNESSES)'

clean:
	rm -rf $(CORPUS) $(ARCHIVE) $(SCOREBOARD) $(MANIFEST)

################################################################################
# Internal targets
################################################################################

# LLVM Bitcode

$(CORPUS)/sqlite/sqlite3.bc: sqlite/sqlite3.c sqlite/sqlite3.h
	@mkdir -p $(@D)
	$(CLANG) $(CFLAGS) -I sqlite -emit-llvm -c $< -o $@

$(CORPUS)/minimal-harnesses/%.harness.bc: minimal-harnesses/%.c
	@mkdir -p $(@D)
	$(CLANG) $(CFLAGS) -emit-llvm -c $< -o $@

$(CORPUS)/sqlite-harnesses/%.harness.bc: sqlite-harnesses/%.c sqlite/sqlite3.h
	@mkdir -p $(@D)
	$(CLANG) $(CFLAGS) -I sqlite -emit-llvm -c $< -o $@

$(CORPUS)/minimal-harnesses/%.bc: $(CORPUS)/minimal-harnesses/%.harness.bc
	$(LLVM_LINK) $< -o $@

$(CORPUS)/sqlite-harnesses/%.bc: \
		$(CORPUS)/sqlite-harnesses/%.harness.bc \
		$(CORPUS)/sqlite/sqlite3.bc
	$(LLVM_LINK) $^ -o $@

# MLIR

$(CORPUS)/%.raw.mlir: $(CORPUS)/%.bc
	$(MLIR_TRANSLATE) --import-llvm $< -o $@

$(CORPUS)/%.mlir: $(CORPUS)/%.raw.mlir
	$(MLIR_OPT) \
		--mlir-print-op-generic \
		--mlir-print-local-scope \
		$< -o $@

# Native LLVM profiles

$(CORPUS)/%-instrumented.bc: $(CORPUS)/%.bc
	$(OPT) -passes=pgo-instr-gen,instrprof $< -o $@

$(CORPUS)/minimal-harnesses/%-instrumented: \
		$(CORPUS)/minimal-harnesses/%-instrumented.bc
	$(CLANG) -fprofile-instr-generate $< -o $@

$(CORPUS)/sqlite-harnesses/%-instrumented: \
		$(CORPUS)/sqlite-harnesses/%-instrumented.bc
	$(CLANG) -fprofile-instr-generate $< $(SQLITE_LDLIBS) -o $@

$(CORPUS)/%.llvm-profile.csv: \
		$(CORPUS)/%-instrumented \
		scripts/llvm_profile.py
	@mkdir -p $(@D)
	$(UV) run scripts/llvm_profile.py collect \
		--harness $*.c \
		--instrumented $< \
		--llvm-profdata $(LLVM_PROFDATA) \
		--output $@

$(LLVM_STATS): $(LLVM_PROFILES) scripts/llvm_profile.py
	@mkdir -p $(@D)
	$(UV) run scripts/llvm_profile.py merge \
		--output $@ \
		$(LLVM_PROFILES)

# Corpus Archive

$(ARCHIVE): $(MLIR) $(LLVM_STATS)
	$(TAR) --create --gzip \
		--file=$@ \
		--directory=$(CORPUS) \
		$(ARCHIVE_CONTENTS)

# VeIR execution
# veir-interpret currently doesn't log any statistics. This is just a placeholder.

$(CORPUS)/%.veir-status: unpack-corpus FORCE
	@mkdir -p $(@D)
	@module="$(CORPUS)/$*.mlir"; \
	status=0; \
	( \
		cd "$(VEIR_DIR)" && \
		lake exe veir-interpret "$$(realpath "$$OLDPWD/$$module")" \
	) > "$(@:.veir-status=.veir-output.txt)" 2>&1 || status=$$?; \
	printf '%s\n' "$$status" > "$@"

FORCE:
