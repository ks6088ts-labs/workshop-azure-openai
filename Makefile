# Git
GIT_REVISION ?= $(shell git rev-parse --short HEAD)
GIT_TAG ?= $(shell git describe --tags --abbrev=0 --always | sed -e s/v//g)

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

.PHONY: info
info: ## show information
	@echo "GIT_REVISION: $(GIT_REVISION)"
	@echo "GIT_TAG: $(GIT_TAG)"

.PHONY: install-deps-dev
install-deps-dev: ## install dependencies for development
	uv sync --all-extras
	uv run pre-commit install

.PHONY: install-deps
install-deps: ## install dependencies for production
	uv sync --no-dev

.PHONY: format-check
format-check: ## format check
	uv run ruff format --check --verbose

.PHONY: format
format: ## format code
	uv run ruff format --verbose

.PHONY: fix
fix: format ## apply auto-fixes
	uv run ruff check --fix

.PHONY: lint
lint: ## lint
	uv run ruff check .

.PHONY: test
test: ## run tests
	uv run pytest --capture=no -vv

.PHONY: ci-test
ci-test: install-deps-dev format-check lint test ## run CI tests

# ---
# Docker
# ---
DOCKER_REPO_NAME ?= ks6088ts
DOCKER_IMAGE_NAME ?= workshop-azure-openai
DOCKER_COMMAND ?= python --version

# Tools
TOOLS_DIR ?= $(HOME)/.local/bin
TRIVY_VERSION ?= 0.49.1

.PHONY: docker-build
docker-build: ## build Docker image
	docker build \
		-t $(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(GIT_TAG) \
		--build-arg GIT_REVISION=$(GIT_REVISION) \
		--build-arg GIT_TAG=$(GIT_TAG) \
		.

.PHONY: docker-run
docker-run: ## run Docker container
	docker run --rm $(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(GIT_TAG) $(DOCKER_COMMAND)

.PHONY: docker-lint
docker-lint: ## lint Dockerfile
	docker run --rm -i hadolint/hadolint < Dockerfile

.PHONY: docker-scan
docker-scan: ## scan Docker image
	@# https://aquasecurity.github.io/trivy/v0.18.3/installation/#install-script
	@which trivy || curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b $(TOOLS_DIR) v$(TRIVY_VERSION)
	trivy image $(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(GIT_TAG)

.PHONY: ci-test-docker
ci-test-docker: docker-lint docker-build docker-run ## run CI test for Docker

.PHONY: update
update: ## update packages
	uv lock --upgrade

# ---
# Docs
# ---

.PHONY: docs
docs: ## build documentation
	uv run mkdocs build

.PHONY: docs-serve
docs-serve: ## serve documentation
	uv run mkdocs serve

.PHONY: ci-test-docs
ci-test-docs: docs ## run CI test for documentation
