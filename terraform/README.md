# WorkPilot AI — Microsoft Azure Deployment Guide

This guide describes how to deploy the entire **WorkPilot AI** stack to Microsoft Azure with the minimum required infrastructure using Terraform, Azure Container Apps, Azure Container Registry, and Azure Database for PostgreSQL Flexible Server.

---

## 1. Azure Concepts vs AWS Equivalents

| Azure Concept | AWS Equivalent | Purpose in WorkPilot |
| :--- | :--- | :--- |
| **Resource Group (`azurerm_resource_group`)** | Resource Group | A logical container for all deployed resources. Simplifies lifecycle tracking and enables 1-click teardown. |
| **Azure Container Registry (`azurerm_container_registry`)** | AWS ECR | Private Docker registry storing the 7 microservice images and Next.js frontend image. |
| **Azure Container Apps (`azurerm_container_app`)** | AWS ECS (Fargate) / App Runner | Fully managed serverless container runtime. Automatically handles HTTPS endpoints, internal service discovery, and scale-to-zero. |
| **Container Apps Environment (`azurerm_container_app_environment`)** | ECS Cluster / VPC Envelope | Shared secure boundary for all Container Apps. Provides internal DNS resolution (`<service-name>.<domain>`) and centralized logging. |
| **Log Analytics Workspace (`azurerm_log_analytics_workspace`)** | CloudWatch Log Group | Centralized log ingestion required by Container Apps. Configured with a 30-day retention to keep dev costs minimal. |
| **PostgreSQL Flexible Server (`azurerm_postgresql_flexible_server`)** | AWS RDS for PostgreSQL | Fully managed PostgreSQL 16 engine supporting WorkPilot's multi-tenant schemas (`SET search_path`). |

---

## 2. Prerequisites

1. **Azure CLI**: [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
2. **Terraform CLI**: [Install Terraform (>= 1.5.0)](https://developer.hashicorp.com/terraform/install)
3. **Docker Desktop**: Running locally to build and push container images.
4. **Azure Subscription**: Active subscription with permissions to create Resource Groups (`Contributor` or `Owner`).

---

## 3. Step-by-Step Deployment Walkthrough

### Step 1: Azure CLI Login
Open your terminal (PowerShell or Bash) and log in:

```bash
az login
```

If you have multiple subscriptions, select the active one:
```bash
az account list --output table
az account set --subscription "<YOUR_SUBSCRIPTION_ID_OR_NAME>"
```

---

### Step 2: Configure Terraform Variables
Navigate to the `terraform/` directory:

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:
- `gemini_api_key`: Your Google Gemini API Key (required by `ai-service`).
- `resend_api_key`: Your Resend API key (optional/recommended for `notification-service`).
- `location`: Azure region (default: `eastus`).
- Optional: Set custom `db_admin_password` or allow Terraform to generate a secure random password automatically.

---

### Step 3: Initialize and Provision ACR & Infrastructure
First, initialize Terraform:

```bash
terraform init
```

Check the planned changes:
```bash
terraform plan -out=tfplan
```

Apply the infrastructure (note: initial run creates the Resource Group, ACR, PostgreSQL DB, and Container Apps):
```bash
terraform apply tfplan
```

> **Note on Initial Container Startup**: Container Apps will attempt to pull the images tagged `:latest`. Before building and pushing your real repository images, follow Step 4 below.

---

### Step 4: Build and Push Monorepo Images to ACR
After `terraform apply` finishes, note the `acr_login_server` output (e.g. `workpilotdevacrx1y2z3.azurecr.io`).

Extract the registry name (the part before `.azurecr.io`):
```powershell
# In PowerShell:
$AcrName = (terraform output -raw acr_login_server).Split('.')[0]

# Run the build & push script from the repository root:
cd ..
.\terraform\scripts\build_and_push.ps1 -AcrName $AcrName
```

Or in Linux / macOS Bash:
```bash
ACR_NAME=$(terraform output -raw acr_login_server | cut -d'.' -f1)
cd ..
./terraform/scripts/build_and_push.sh "$ACR_NAME"
```

This builds all production multi-stage targets:
- `auth-service`
- `hr-service`
- `it-service`
- `workflow-service`
- `notification-service`
- `analytics-service`
- `ai-service`
- `frontend` (Next.js standalone)

---

### Step 5: Database Migrations
WorkPilot uses Alembic and SQL schema isolation. Once the PostgreSQL server is up and reachable, execute migrations:

1. Obtain the database connection string from Terraform:
   ```bash
   cd terraform
   terraform output database_url_template
   ```
2. Run database migrations for the services from your local machine or CI/CD runner:
   ```bash
   # From the repository root with DATABASE_URL set:
   cd auth-service && uv run alembic upgrade head
   cd ../workflow-service && uv run alembic upgrade head
   cd ../notification-service && uv run alembic upgrade head
   cd ../analytics-service && uv run python run_mig.py
   ```

---

## 4. Verification

After deployment, display the public endpoints:

```bash
cd terraform
terraform output
```

Verify services via curl or browser:

```bash
# Test Auth Service
curl -i https://<auth_service_url>/

# Test HR Service Health
curl -i https://<hr_service_url>/health

# Test Frontend
curl -i https://<frontend_url>/
```

---

## 5. Cost Control & Teardown

### Cost Optimization Features in this Setup
- **Scale to Zero**: `container_min_replicas = 0` is set for all compute apps except `analytics-service` and `redpanda`. When no HTTP traffic arrives, containers scale to 0 vCPU/RAM, incurring $0 container compute costs.
- **Burstable PostgreSQL**: Configured with `B_Standard_B1ms` (~$15/month) instead of expensive multi-zone General Purpose instances.
- **Single Log Retention**: Log Analytics set to 30 days retention to avoid log storage costs.
- **No Redis Charges**: Redis was eliminated from active requirements, saving ~$16–$55/month.

### Safe Cleanup / Destroy
To destroy all created resources and completely eliminate any further billing:

```bash
cd terraform
terraform destroy
```

Confirm by typing `yes` when prompted. Because all resources are grouped in a dedicated Resource Group, deleting them leaves zero orphaned Azure assets.
