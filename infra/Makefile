# Parameters
SOURCE_FILES ?= $(shell find . -type f -name '*.bicep' -print)
OUT_DIR ?= ./artifacts
BICEP_MAIN ?= ./main.bicep
BICEP_PARAMETERS ?= ./main.bicepparam

# Git
GIT_REVISION ?= $(shell git rev-parse --short HEAD)
GIT_TAG ?= $(shell git describe --tags --abbrev=0 --always | sed -e s/v//g)

# Azure
SUBSCRIPTION_ID ?= $(shell az account show --query id --output tsv)
SUBSCRIPTION_NAME ?= $(shell az account show --query name --output tsv)
TENANT_ID ?= $(shell az account show --query tenantId --output tsv)
OBJECT_ID ?= $(shell az account show --query user.name --output tsv)
USER_ID ?= $(shell az ad user show --id $(OBJECT_ID) --query id --output tsv)
RESOURCE_GROUP_NAME ?= rg-workshop-azure-openai
LOCATION ?= japaneast
DEPLOYMENT_NAME ?= main

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

.PHONY: info
info: ## show information
	@echo "GIT_REVISION: $(GIT_REVISION)"
	@echo "GIT_TAG: $(GIT_TAG)"
	@echo "SUBSCRIPTION_ID: $(SUBSCRIPTION_ID)"
	@echo "SUBSCRIPTION_NAME: $(SUBSCRIPTION_NAME)"
	@echo "TENANT_ID: $(TENANT_ID)"
	@echo "OBJECT_ID: $(OBJECT_ID)"
	@echo "USER_ID: $(USER_ID)"

.PHONY: install-deps-dev
install-deps-dev: ## install dependencies for development
	@which az || echo "Please install Azure CLI: https://github.com/Azure/azure-cli#installation"
	@az bicep upgrade

.PHONY: format
format: ## format codes
	@$(foreach file,$(SOURCE_FILES),az bicep format --file $(file) --insert-final-newline;)

.PHONY: lint
lint: ## lint codes
	@echo "lint: Skip since not implemented yet"

.PHONY: build
build: ## build a bicep file
	@mkdir -p $(OUT_DIR)
	@az bicep build \
		--file $(BICEP_MAIN) \
		--outfile $(OUT_DIR)/azuredeploy.json

.PHONY: test
test: deployment-what-if ## test codes

.PHONY: ci-test
ci-test: install-deps-dev lint build test ## ci test

.PHONY: create-resource-group
create-resource-group: ## create resource group
	az group create \
		--name $(RESOURCE_GROUP_NAME) \
		--location $(LOCATION)

.PHONY: delete-resource-group
delete-resource-group: ## delete resource group
	az group delete --name $(RESOURCE_GROUP_NAME) --yes --no-wait

.PHONY: deployment-what-if
deployment-what-if: ## execute a deployment What-If operation at resource group scope
	az deployment group what-if \
		--resource-group $(RESOURCE_GROUP_NAME) \
		--template-file $(BICEP_MAIN) \
		--parameters $(BICEP_PARAMETERS)

.PHONY: deployment-create
deployment-create: ## start a deployment at resource group
	az deployment group create \
		--resource-group $(RESOURCE_GROUP_NAME) \
		--template-file $(BICEP_MAIN) \
		--parameters $(BICEP_PARAMETERS)

.PHONY: deployment-output
deployment-output: ## show deployment output
	az deployment group show \
		--resource-group $(RESOURCE_GROUP_NAME) \
		--name $(DEPLOYMENT_NAME) \
		--query properties.outputs.deploymentInfo.value

.PHONY: deploy
deploy: create-resource-group deployment-what-if deployment-create ## deploy resources

.PHONY: destroy
destroy: delete-resource-group ## destroy resources

# Generate deployment credentials: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-github-actions?tabs=userlevel%2CCLI#generate-deployment-credentials
.PHONY: create-for-rbac
create-for-rbac: ## create service principal for RBAC
	az ad sp create-for-rbac \
		--name test-baseline-environment-on-azure-bicep \
		--role contributor \
		--scopes /subscriptions/$(SUBSCRIPTION_ID)/resourceGroups/$(RESOURCE_GROUP_NAME) \
		--sdk-auth > $(OUT_DIR)/azure-credentials.json

# Configure the GitHub secrets: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-github-actions?tabs=userlevel%2CCLI#configure-the-github-secrets
.PHONY: configure-github-secrets
configure-github-secrets: ## configure GitHub secrets
	gh secret set AZURE_CREDENTIALS < $(OUT_DIR)/azure-credentials.json
	gh secret set AZURE_SUBSCRIPTION --body $(SUBSCRIPTION_ID)
	gh secret set AZURE_RG --body $(RESOURCE_GROUP_NAME)
