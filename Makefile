PYTHON ?= python3
PROJECT := scripts/i2n.py

.PHONY: help status inventory todo baseline-check baseline-refresh validate check rust-check install-hooks all

help:
	@$(PYTHON) $(PROJECT) --help

status:
	@$(PYTHON) $(PROJECT) status

inventory:
	@$(PYTHON) $(PROJECT) inventory --write

todo:
	@$(PYTHON) $(PROJECT) checklist --write

baseline-check:
	@$(PYTHON) $(PROJECT) baseline verify

baseline-refresh:
	@$(PYTHON) $(PROJECT) baseline capture --write

validate:
	@$(PYTHON) $(PROJECT) validate

check: validate

rust-check:
	cargo fmt --all -- --check
	cargo clippy --workspace --all-targets -- -D warnings
	cargo test --workspace

install-hooks:
	@$(PYTHON) scripts/install_hooks.py

all:
	@$(PYTHON) $(PROJECT) all --write
