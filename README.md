# Azure On-Premises to Cloud Migration

![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoftazure&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Bicep](https://img.shields.io/badge/Bicep-0078D4?style=flat&logo=microsoftazure&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)

## Problem Statement

Many organisations run critical workloads on ageing on-premises infrastructure — high maintenance cost, no scalability, no built-in disaster recovery. This project simulates a real-world lift-and-shift migration from an on-premises environment to Azure, demonstrating the full migration lifecycle from assessment through to production deployment and BCDR setup.

## Architecture

### Before Migration — Simulated On-Premises
![Before Architecture](docs/architecture/before-migration.png)

### After Migration — Azure Cloud
![After Architecture](docs/architecture/after-migration.png)

## What This Project Demonstrates

- Simulating an on-premises environment using Azure VM (Ubuntu 22.04)
- Running a Python Flask web application with SQLite database on the VM
- Azure Migrate assessment for migration readiness
- Database migration from SQLite to Azure SQL Database
- Application migration from VM to Azure App Service
- CI/CD pipeline with GitHub Actions for automated deployment
- Azure Backup with Recovery Services Vault for BCDR
- Azure Site Recovery for disaster recovery and failover
- Azure Monitor and Log Analytics for observability
- VNet with subnets and NSG rules for network security
- Infrastructure-as-Code using Azure Bicep

## Tech Stack

| Layer | Technology |
|---|---|
| Simulated On-Prem | Azure VM — Ubuntu 22.04 |
| Application | Python 3.11, Flask 3.0, Gunicorn |
| On-Prem Database | SQLite |
| Cloud Application Host | Azure App Service (Linux, P1v3) |
| Cloud Database | Azure SQL Database (General Purpose) |
| Networking | Azure VNet, Subnets, NSG |
| IaC | Azure Bicep |
| CI/CD | GitHub Actions |
| Backup | Azure Backup — Recovery Services Vault |
| Disaster Recovery | Azure Site Recovery |
| Monitoring | Azure Monitor, Log Analytics, Application Insights |
| Migration Assessment | Azure Migrate |

## Prerequisites

- Azure subscription (free tier or pay-as-you-go)
- Azure CLI >= 2.50 installed
- Python 3.11+
- Git

## Repository Structure

```text
azure-onprem-to-cloud-migration/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
├── docs/
│   ├── architecture/
│   │   ├── before-migration.png
│   │   ├── after-migration.png
│   │   └── diagrams.drawio     # Editable source
│   ├── screenshots/            # Portal screenshots by day
│   └── migration-report.md     # Full migration report
├── infra/
│   ├── bicep/
│   │   ├── network.bicep       # VNet, subnets, NSGs
│   │   ├── vm.bicep            # On-prem simulation VM
│   │   └── sql.bicep           # Azure SQL resources
│   └── nsg-rules/
│       └── nsg-rules.json      # Exported NSG rules
├── app/
│   ├── app.py                  # Flask application
│   ├── requirements.txt
│   └── startup.sh              # App Service startup script
├── scripts/
│   ├── vm-setup.sh             # VM post-deployment setup
│   ├── migrate-db.sh           # SQLite to Azure SQL migration
│   └── teardown.sh             # Resource cleanup
└── README.md
```

## Setup Guide

> Full step-by-step instructions in [docs/runbooks/deployment.md](docs/runbooks/deployment.md)

### Quick Start

```bash
# Clone repository
git clone https://github.com/tarunkumar212/azure-onprem-to-cloud-migration
cd azure-onprem-to-cloud-migration

# Login to Azure
az login

# Deploy network infrastructure
az deployment group create \
  --resource-group rg-migration-project \
  --template-file infra/bicep/network.bicep
```

## Migration Phases

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Foundation and repo setup | ✅ Complete — Day 1 |
| Phase 2 | Network layer — VNet, Subnets, NSG | ✅ Complete — Day 2 |
| Phase 3 | On-premises VM simulation | ✅ Complete — Day 3 |
| Phase 4 | Testing, validation, baseline metrics | ✅ Complete — Day 4 |
| Phase 5 | Azure Migrate assessment | ✅ Complete — Day 5 |
| Phase 6 | Azure SQL deployment and data migration | ✅ Complete — Day 6 |
| Phase 7 | App Service — Flask migration | 🔄 Tomorrow — Day 7 |
| Phase 8 | GitHub Actions CI/CD | ⏳ Planned — Day 8 |
| Phase 9 | Azure Backup | ⏳ Planned — Day 9 |
| Phase 10 | Azure Site Recovery | ⏳ Planned — Day 10 |
| Phase 11 | After-migration diagrams and analysis | ⏳ Planned — Day 11 |
| Phase 12 | Migration report | ⏳ Planned — Day 12 |
| Phase 13 | Documentation polish | ⏳ Planned — Day 13 |
| Phase 14 | LinkedIn post and project complete | ⏳ Planned — Day 14 |


## Before Migration State — Documented Day 4

This section captures the complete state of the on-premises 
system before migration begins. All metrics and data recorded 
here will be compared against the post-migration Azure system 
to validate migration success.

### Application Stack

| Component | Technology | Details |
|---|---|---|
| Operating System | Ubuntu 22.04 LTS | Azure VM Standard_B2s |
| Web Server | Nginx 1.18 | Reverse proxy on port 80 |
| App Server | Gunicorn | 2 workers on port 5000 |
| Framework | Python Flask 3.0 | Python 3.12 |
| Database | SQLite | File at /home/azureuser/flaskapp/app.db |

### API Endpoints Verified

| Endpoint | Method | Status | Response |
|---|---|---|---|
| / | GET | ✅ Working | HTML product page |
| /api/products | GET | ✅ Working | JSON array of products |
| /api/products | POST | ✅ Working | Creates new product |
| /health | GET | ✅ Working | JSON health status |
| /api/migration-log | GET | ✅ Working | JSON log entries |

### Database State

| Item | Detail |
|---|---|
| Database type | SQLite (file-based) |
| Tables | products, migration_log |
| Product records | 6 (5 original + 1 test) |
| Schema exported | docs/database-export.sql |
| Data exported | docs/database-export.sql |

### Performance Baseline

| Metric | Value |
|---|---|
| Tool | Apache Benchmark |
| Requests | 500 total, 10 concurrent |
| Requests per second | 1781.17 |
| Mean response time | PASTE YOUR NUMBER HERE ms |
| 95th percentile | PASTE YOUR NUMBER HERE ms |
| Failed requests | 0 |

### Known Limitations of On-Premises Setup

| Limitation | Impact | Solution After Migration |
|---|---|---|
| Single VM | If VM goes down, app is down | App Service has built-in HA |
| SQLite database | No concurrent writes, no backups | Azure SQL has HA and auto-backup |
| Manual scaling | Must resize VM manually | App Service auto-scales |
| Manual OS patching | Security risk if delayed | App Service manages OS |
| No disaster recovery | Data loss if disk fails | Azure Backup + Site Recovery |

### What Changes During Migration

| Layer | Before (On-Premises) | After (Azure Cloud) |
|---|---|---|
| App hosting | Azure VM + Nginx + Gunicorn | Azure App Service |
| Database | SQLite on VM disk | Azure SQL Database |
| Deployment | Manual SSH and copy | GitHub Actions CI/CD |
| Monitoring | Basic Azure Monitor | Full observability stack |
| BCDR | None | Backup + Site Recovery |




## Azure Migrate Assessment Results

**Project:** migrate-onprem-assessment
**Assessment:** assessment-onprem-vm
**Assessment type:** Import-based (CSV)
**Target:** Azure VM (Lift and Shift)
**Date:** Day 5 of migration project

### Readiness Result

| Check | Result |
|---|---|
| Overall readiness | Ready with conditions |
| OS compatibility | ✅ Passed |
| Boot type | ✅ Passed |
| Storage | ✅ Passed |
| Compute | ✅ Passed |
| Security | ✅ Passed |
| Migration issues | Minor warnings only (see screenshot) |

### What "Ready with Conditions" Means

The VM passed all 5 core readiness checks. The "conditions" 
are informational warnings from using import-based assessment 
without a live agent — no performance history was available 
so Azure used the CSV specs directly.

This does not block migration. All critical checks passed.

### Why Azure VM is the Recommended Target

Azure Migrate recommends Azure VM (lift and shift) because 
it assesses like-for-like replacement. Our actual migration 
decision is different — we chose App Service + Azure SQL 
(PaaS) over Azure VM (IaaS) for the following reasons:

| Factor | Azure VM (Migrate Recommendation) | Our Choice: App Service + SQL |
|---|---|---|
| OS management | Manual patching required | Fully managed by Azure |
| Scaling | Manual VM resize | Auto-scaling built in |
| Availability | Depends on VM uptime | 99.95% SLA built in |
| Cost | Fixed hourly regardless of traffic | Scales with actual usage |
| Operational overhead | High | Low |

### Assessment Recommendation vs Actual Decision

Azure Migrate recommended: Standard_D2s_v4 Azure VM
Our actual migration target: Azure App Service + Azure SQL

Reason for deviation: PaaS services (App Service + SQL) 
provide better reliability, scalability, and lower operational 
overhead than a direct VM lift-and-shift. The assessment 
confirms the workload is compatible with Azure — we simply 
chose a more modern deployment model than the tool suggested.



## Database Migration — SQLite to Azure SQL (Day 6)

### What Changed

| Item | Before — On-Premises | After — Azure Cloud |
|---|---|---|
| Database engine | SQLite 3 | Azure SQL Database |
| Location | VM disk — app.db file | Azure managed infrastructure |
| Backup | None | Automated every 5–10 minutes |
| High availability | None | 99.99% SLA |
| Concurrent writes | Not supported | Fully supported |
| Admin overhead | Manual | Fully managed by Azure |
| Region | East US (VM) | West US (SQL) |

### Data Type Mapping — SQLite to Azure SQL

| Column | SQLite Type | Azure SQL Type | Reason |
|---|---|---|---|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | INT IDENTITY(1,1) | SQL Server auto-increment |
| name | TEXT | NVARCHAR(255) | Unicode text with size limit |
| description | TEXT | NVARCHAR(500) | Unicode text with size limit |
| price | REAL | DECIMAL(10,2) | Precise decimal for money |
| stock | INTEGER | INT | Direct equivalent |
| created_at | TIMESTAMP | DATETIME2 | SQL Server datetime type |

### Migration Process

1. Schema exported from SQLite on Day 4 — docs/database-schema.sql
2. Azure SQL schema created with converted data types — docs/azure-sql-schema.sql
3. Data exported from SQLite on Day 4 — docs/database-export.sql
4. Migration script reads export file and rewrites INSERT statements
   to include column list required by Azure SQL IDENTITY columns
5. IDENTITY_INSERT enabled to preserve original IDs
6. Row count validated — 6 products, 1 migration log entry

### Validation Result

| Check | SQLite | Azure SQL | Match |
|---|---|---|---|
| Products | 6 rows | 6 rows | ✅ |
| Migration log | 1 row | 1 row | ✅ |
| Data integrity | Spot checked | Spot checked | ✅ |

### Azure SQL Configuration

| Setting | Value |
|---|---|
| Logical server | sqlserver-migration-dev.database.windows.net |
| Database name | sqldb-migration-dev |
| Region | West US |
| Pricing tier | Basic — 5 DTUs |
| Max storage | 2 GB |
| Backup retention | 7 days built in |
| Connection security | TLS 1.2 encrypted |

### Security Approach

- Password stored as environment variable — never in code
- Never committed to GitHub
- Azure SQL firewall restricts to known IPs only
- All connections encrypted — Encrypt=yes in connection string
- Next improvement — Azure Key Vault (Project 2)



## Challenges and Lessons Learned

SQLite exports INSERT statements without column lists.
Azure SQL requires explicit column lists when inserting
into IDENTITY columns with IDENTITY_INSERT ON.

Fix — Python migration script rewrites each INSERT statement
to add the column list before running against Azure SQL.
This is documented in scripts/migrate_db.py.

## Cost Analysis

> Before vs after cost comparison will be added in Phase 4

## Author

**TARUN KUMAR S**
Network Developer at Wipro | AZ-900 | AZ-104
[LinkedIn](www.linkedin.com/in/tarun-kumar-s-0b40aa2a2) | [GitHub](https://github.com/tarunkumar212)
