################################################################################
# Configuration
################################################################################

VEIR_DIR ?= veir
VEIR_TIMEOUT_SECONDS ?= 30

MLIR_TRANSLATE ?= mlir-translate
LLUBI ?= llubi
LAKE ?= lake
UV ?= uv
TAR ?= tar

################################################################################
# Layout
################################################################################

CORPUS := corpus
TEST_DIR := llubi-tests

TESTS := $(sort $(wildcard $(TEST_DIR)/*/*.ll))
NAMES := $(TESTS:.ll=)
MLIR := $(addprefix $(CORPUS)/,$(addsuffix .mlir,$(NAMES)))
LLUBI_TRACES := $(addprefix $(CORPUS)/,$(addsuffix .llubi-output.txt,$(NAMES)))
VEIR_TRACES := $(addprefix $(CORPUS)/,$(addsuffix .veir-output.txt,$(NAMES)))

ARCHIVE := corpus.tar.gz
ARCHIVE_CONTENTS := $(patsubst $(CORPUS)/%,%,$(MLIR) $(LLUBI_TRACES))
MANIFEST := manifest.json
UNPACKED := $(CORPUS)/.unpacked
SCOREBOARD := SCOREBOARD.md

VEIR_INTERPRET := $(VEIR_DIR)/.lake/build/bin/veir-interpret

################################################################################
# Basic Make Behavior
################################################################################

.DEFAULT_GOAL := scoreboard

.DELETE_ON_ERROR:
.SECONDARY:

.PHONY: \
	refresh-corpus \
	check-corpus \
	scoreboard \
	clean \
	FORCE

################################################################################
# Public Targets
################################################################################

refresh-corpus: $(MLIR) $(LLUBI_TRACES) scripts/corpus_manifest.py
	$(TAR) --create --gzip \
		--file=$(ARCHIVE) \
		--directory=$(CORPUS) \
		$(ARCHIVE_CONTENTS)
	$(UV) run scripts/corpus_manifest.py manifest \
		--archive $(ARCHIVE) \
		--manifest $(MANIFEST) \
		--tool mlir-translate=$(MLIR_TRANSLATE) \
		--tool llubi=$(LLUBI)

check-corpus: scripts/corpus_manifest.py
	$(UV) run scripts/corpus_manifest.py check \
		--archive $(ARCHIVE) \
		--manifest $(MANIFEST)

scoreboard: $(SCOREBOARD)

clean:
	rm -rf $(CORPUS)

################################################################################
# Internal targets
################################################################################

# MLIR

$(CORPUS)/%.mlir: %.ll
	@mkdir -p $(@D)
	$(MLIR_TRANSLATE) \
		--import-llvm \
		--mlir-print-op-generic \
		--mlir-print-local-scope \
		$< -o $@

# llubi execution

$(CORPUS)/%.llubi-output.txt: %.ll scripts/capture.py
	@mkdir -p $(@D)
	$(UV) run scripts/capture.py \
		--output $@ \
		-- $(LLUBI) --verbose $<

# Corpus Archive

$(UNPACKED): $(ARCHIVE) $(MANIFEST) scripts/corpus_manifest.py
	$(UV) run scripts/corpus_manifest.py check \
		--archive $(ARCHIVE) \
		--manifest $(MANIFEST)
	rm -rf $(CORPUS)
	@mkdir -p $(CORPUS)
	$(TAR) --extract --gzip --touch \
		--file=$(ARCHIVE) \
		--directory=$(CORPUS)
	touch $@

# VeIR execution

$(VEIR_INTERPRET): FORCE
	cd $(VEIR_DIR) && $(LAKE) build veir-interpret

$(CORPUS)/%.veir-output.txt: $(UNPACKED) $(VEIR_INTERPRET) scripts/capture.py
	$(UV) run scripts/capture.py \
		--output $@ \
		--timeout-seconds $(VEIR_TIMEOUT_SECONDS) \
		-- $(VEIR_INTERPRET) $(CORPUS)/$*.mlir

# Scoreboard

$(SCOREBOARD): $(VEIR_TRACES) scripts/scoreboard.py scripts/capture.py scripts/corpus_manifest.py
	$(UV) run scripts/scoreboard.py \
		--corpus $(CORPUS) \
		--veir-dir $(VEIR_DIR) \
		--veir-interpret $(VEIR_INTERPRET) \
		--manifest $(MANIFEST) \
		--output $@

FORCE:
