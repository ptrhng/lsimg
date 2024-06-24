default: help

## help: Show help
.PHONY: help
help: Makefile
	@printf "\n\033[1mUsage: make <TARGETS> ...\033[0m\n\n\033[1mTargets:\033[0m\n\n"
	@sed -n 's/^## //p' $< | awk -F':' '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' | sort | sed -e 's/^/  /'

.PHONY: all
all: typecheck test lint format

## typecheck: Run type check
.PHONY: typecheck
typecheck:
	poetry run mypy
	@echo

## format: Format code
.PHONY: format
format:
	poetry run ruff format
	@echo

## lint: Run linters and fix lint errors
.PHONY: lint
lint:
	poetry run ruff check --fix
	@echo

## test: Run tests
.PHONY: test
test:
	poetry run pytest -v
	@echo
