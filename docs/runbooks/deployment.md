# Deployment Runbook

## Prerequisites
- Azure CLI installed and logged in (`az login`)
- Contributor access on Azure subscription
- Python 3.11+ installed locally

## Phase 1 — Network Deployment
```bash
az group create --name rg-migration-project --location eastus
az deployment group create \
  --resource-group rg-migration-project \
  --template-file infra/bicep/network.bicep
```

## Phase 2 — VM Deployment (On-Prem Simulation)
```bash
az deployment group create \
  --resource-group rg-migration-project \
  --template-file infra/bicep/vm.bicep
```

## Teardown
```bash
az group delete --name rg-migration-project --yes --no-wait
```
