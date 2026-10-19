# -------------------------------------------------------------
# WorkPilot Azure Infrastructure
# Minimum complete configuration for fast and reproducible deployment
# -------------------------------------------------------------

# Generates random suffix to ensure globally unique names (ACR, Key Vault, Postgres, Container Apps)
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "random_password" "db_password" {
  length           = 20
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "random_password" "jwt_secret" {
  length  = 32
  special = false
}

locals {
  name_prefix   = "${var.project_name}-${var.environment}"
  safe_prefix   = replace(local.name_prefix, "-", "")
  unique_suffix = random_string.suffix.result

  # Use provided password or generate one
  db_password = var.db_admin_password != "" ? var.db_admin_password : random_password.db_password.result
  jwt_secret  = var.jwt_secret_key != "" ? var.jwt_secret_key : random_password.jwt_secret.result

  # Common resource tags
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# -------------------------------------------------------------
# 1. Resource Group
# (Creates a new resource group or imports/uses an existing one like workpilot-rg)
# -------------------------------------------------------------
resource "azurerm_resource_group" "main" {
  count    = var.resource_group_name == "" ? 1 : 0
  name     = "${local.name_prefix}-rg"
  location = var.location
  tags     = local.common_tags
}

data "azurerm_resource_group" "existing" {
  count = var.resource_group_name != "" ? 1 : 0
  name  = var.resource_group_name
}

locals {
  rg_name     = var.resource_group_name != "" ? data.azurerm_resource_group.existing[0].name : azurerm_resource_group.main[0].name
  rg_location = var.resource_group_name != "" ? data.azurerm_resource_group.existing[0].location : azurerm_resource_group.main[0].location
}

# -------------------------------------------------------------
# 2. Azure Container Registry (ACR)
# (Equivalent to AWS ECR - stores Docker images for backend & frontend)
# -------------------------------------------------------------
resource "azurerm_container_registry" "acr" {
  name                = "${local.safe_prefix}acr${local.unique_suffix}"
  resource_group_name = local.rg_name
  location            = local.rg_location
  sku                 = "Basic"
  admin_enabled       = true # Enabled for quick, credential-based image pull by Container Apps
  tags                = local.common_tags
}

# -------------------------------------------------------------
# 3. Log Analytics Workspace
# (Equivalent to AWS CloudWatch Logs - required by Azure Container Apps)
# -------------------------------------------------------------
resource "azurerm_log_analytics_workspace" "logs" {
  name                = "${local.name_prefix}-law-${local.unique_suffix}"
  resource_group_name = local.rg_name
  location            = local.rg_location
  sku                 = "PerGB2018"
  retention_in_days   = 30 # Kept minimal for development cost control
  tags                = local.common_tags
}

# -------------------------------------------------------------
# 4. Azure Container Apps Environment
# (Equivalent to AWS ECS Cluster - managed serverless Kubernetes envelope)
# -------------------------------------------------------------
resource "azurerm_container_app_environment" "env" {
  name                       = "${local.name_prefix}-cae-${local.unique_suffix}"
  resource_group_name        = local.rg_name
  location                   = local.rg_location
  log_analytics_workspace_id = azurerm_log_analytics_workspace.logs.id
  tags                       = local.common_tags
}

# -------------------------------------------------------------
# 5. Azure Database for PostgreSQL Flexible Server
# (Equivalent to AWS RDS for PostgreSQL - stores multi-tenant schemas)
# -------------------------------------------------------------
resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = "${local.name_prefix}-psql-${local.unique_suffix}"
  resource_group_name    = local.rg_name
  location               = local.rg_location
  version                = "16"
  administrator_login    = var.db_admin_username
  administrator_password = local.db_password
  zone                   = "1"

  storage_mb = var.db_storage_mb
  sku_name   = var.db_sku_name # B_Standard_B1ms is cost-effective burstable tier

  backup_retention_days = 7

  tags = local.common_tags
}

# Allow Azure internal services (e.g. Container Apps) to connect to PostgreSQL
# Azure special IP 0.0.0.0 allows Azure services when not using VNet peering
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.postgres.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# Primary application database
resource "azurerm_postgresql_flexible_server_database" "workpilot_db" {
  name      = "workpilot"
  server_id = azurerm_postgresql_flexible_server.postgres.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Dedicated database for AI service history/tools if separated
resource "azurerm_postgresql_flexible_server_database" "workpilot_ai_db" {
  name      = "workpilot_ai"
  server_id = azurerm_postgresql_flexible_server.postgres.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Calculated connection strings
locals {
  db_host = azurerm_postgresql_flexible_server.postgres.fqdn
  db_user = var.db_admin_username
  db_pass = local.db_password

  database_url    = "postgresql://${local.db_user}:${local.db_pass}@${local.db_host}:5432/${azurerm_postgresql_flexible_server_database.workpilot_db.name}?sslmode=require"
  ai_database_url = "postgresql://${local.db_user}:${local.db_pass}@${local.db_host}:5432/${azurerm_postgresql_flexible_server_database.workpilot_ai_db.name}?sslmode=require"
}

# -------------------------------------------------------------
# 6. Redpanda / Kafka Event Broker Container App
# (Shared broker for hr/it/workflow events consumed by analytics-service)
# -------------------------------------------------------------
resource "azurerm_container_app" "redpanda" {
  name                         = "redpanda"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  ingress {
    external_enabled = false # Internal to the Container Apps environment only
    target_port      = 29092
    transport        = "tcp"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 1 # Keep at 1 for broker uptime
    max_replicas = 1

    container {
      name   = "redpanda"
      image  = "docker.redpanda.com/redpandadata/redpanda:v23.2.19"
      cpu    = 0.5
      memory = "1.0Gi"

      command = [
        "redpanda",
        "start",
        "--smp", "1",
        "--memory", "1G",
        "--reserve-memory", "0M",
        "--overprovisioned",
        "--node-id", "0",
        "--kafka-addr", "PLAINTEXT://0.0.0.0:29092",
        "--advertise-kafka-addr", "PLAINTEXT://redpanda:29092"
      ]
    }
  }
}

# -------------------------------------------------------------
# 7. Internal Ingress URLs for Inter-Service Communication
# Container Apps in the same environment can communicate via <app-name>.<domain>
# -------------------------------------------------------------
locals {
  auth_internal_url         = "http://auth-service.${azurerm_container_app_environment.env.default_domain}"
  hr_internal_url           = "http://hr-service.${azurerm_container_app_environment.env.default_domain}"
  it_internal_url           = "http://it-service.${azurerm_container_app_environment.env.default_domain}"
  workflow_internal_url     = "http://workflow-service.${azurerm_container_app_environment.env.default_domain}"
  notification_internal_url = "http://notification-service.${azurerm_container_app_environment.env.default_domain}"
  analytics_internal_url    = "http://analytics-service.${azurerm_container_app_environment.env.default_domain}"
  ai_internal_url           = "http://ai-service.${azurerm_container_app_environment.env.default_domain}"
  kafka_url                 = "redpanda:29092"
}

# -------------------------------------------------------------
# 8. Microservices: Azure Container Apps
# -------------------------------------------------------------

# --- Auth Service ---
resource "azurerm_container_app" "auth_service" {
  name                         = "auth-service"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  secret {
    name  = "database-url"
    value = local.database_url
  }

  secret {
    name  = "jwt-secret"
    value = local.jwt_secret
  }

  ingress {
    external_enabled = true # Needed so users and frontend browser can authenticate
    target_port      = 8000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = var.container_min_replicas
    max_replicas = var.container_max_replicas

    container {
      name   = "auth-service"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/auth-service:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APP_NAME"
        value = "WorkPilot Auth Service"
      }
      env {
        name  = "DEBUG"
        value = "false"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "SECRET_KEY"
        secret_name = "jwt-secret"
      }
      env {
        name  = "ALGORITHM"
        value = "HS256"
      }
      env {
        name  = "ACCESS_TOKEN_EXPIRE_MINUTES"
        value = "1440"
      }
      env {
        name  = "ANALYTICS_SERVICE_URL"
        value = local.analytics_internal_url
      }
      env {
        name  = "KAFKA_URL"
        value = local.kafka_url
      }

      readiness_probe {
        port      = 8000
        path      = "/"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 8000
        path      = "/"
        transport = "HTTP"
      }
    }
  }
}

# --- HR Service ---
resource "azurerm_container_app" "hr_service" {
  name                         = "hr-service"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  secret {
    name  = "database-url"
    value = local.database_url
  }

  secret {
    name  = "jwt-secret"
    value = local.jwt_secret
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = var.container_min_replicas
    max_replicas = var.container_max_replicas

    container {
      name   = "hr-service"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/hr-service:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APP_NAME"
        value = "WorkPilot HR Service"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "SECRET_KEY"
        secret_name = "jwt-secret"
      }
      env {
        name  = "KAFKA_URL"
        value = local.kafka_url
      }
      env {
        name  = "AUTH_SERVICE_URL"
        value = local.auth_internal_url
      }

      readiness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
    }
  }
}

# --- IT Service ---
resource "azurerm_container_app" "it_service" {
  name                         = "it-service"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  secret {
    name  = "database-url"
    value = local.database_url
  }

  secret {
    name  = "jwt-secret"
    value = local.jwt_secret
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = var.container_min_replicas
    max_replicas = var.container_max_replicas

    container {
      name   = "it-service"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/it-service:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APP_NAME"
        value = "WorkPilot IT Service"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "SECRET_KEY"
        secret_name = "jwt-secret"
      }
      env {
        name  = "KAFKA_URL"
        value = local.kafka_url
      }
      env {
        name  = "HR_SERVICE_URL"
        value = local.hr_internal_url
      }

      readiness_probe {
        port      = 8000
        path      = "/"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 8000
        path      = "/"
        transport = "HTTP"
      }
    }
  }
}

# --- Workflow Service ---
resource "azurerm_container_app" "workflow_service" {
  name                         = "workflow-service"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  secret {
    name  = "database-url"
    value = local.database_url
  }

  secret {
    name  = "jwt-secret"
    value = local.jwt_secret
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = var.container_min_replicas
    max_replicas = var.container_max_replicas

    container {
      name   = "workflow-service"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/workflow-service:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APP_NAME"
        value = "WorkPilot Workflow Service"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "SECRET_KEY"
        secret_name = "jwt-secret"
      }
      env {
        name  = "KAFKA_URL"
        value = local.kafka_url
      }

      readiness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
    }
  }
}

# --- Notification Service ---
resource "azurerm_container_app" "notification_service" {
  name                         = "notification-service"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  secret {
    name  = "database-url"
    value = local.database_url
  }

  secret {
    name  = "jwt-secret"
    value = local.jwt_secret
  }

  secret {
    name  = "resend-api-key"
    value = var.resend_api_key != "" ? var.resend_api_key : "dummy_resend_key"
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = var.container_min_replicas
    max_replicas = var.container_max_replicas

    container {
      name   = "notification-service"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/notification-service:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APP_NAME"
        value = "WorkPilot Notification Service"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "SECRET_KEY"
        secret_name = "jwt-secret"
      }
      env {
        name        = "RESEND_API_KEY"
        secret_name = "resend-api-key"
      }
      env {
        name  = "EMAIL_FROM"
        value = var.email_from
      }

      readiness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
    }
  }
}

# --- Analytics Service ---
resource "azurerm_container_app" "analytics_service" {
  name                         = "analytics-service"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  secret {
    name  = "database-url"
    value = local.database_url
  }

  secret {
    name  = "jwt-secret"
    value = local.jwt_secret
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 1 # Keep at least 1 replica to listen to Kafka broker streams
    max_replicas = var.container_max_replicas

    container {
      name   = "analytics-service"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/analytics-service:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APP_NAME"
        value = "WorkPilot Analytics Service"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "SECRET_KEY"
        secret_name = "jwt-secret"
      }
      env {
        name  = "KAFKA_URL"
        value = local.kafka_url
      }

      readiness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
    }
  }
}

# --- AI Service ---
resource "azurerm_container_app" "ai_service" {
  name                         = "ai-service"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  secret {
    name  = "database-url"
    value = local.ai_database_url
  }

  secret {
    name  = "gemini-api-key"
    value = var.gemini_api_key != "" ? var.gemini_api_key : "dummy_gemini_key_configure_in_vars"
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = var.container_min_replicas
    max_replicas = var.container_max_replicas

    container {
      name   = "ai-service"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/ai-service:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APP_NAME"
        value = "WorkPilot AI Service"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "GEMINI_API_KEY"
        secret_name = "gemini-api-key"
      }
      env {
        name  = "HR_SERVICE_URL"
        value = local.hr_internal_url
      }
      env {
        name  = "IT_SERVICE_URL"
        value = local.it_internal_url
      }
      env {
        name  = "WORKFLOW_SERVICE_URL"
        value = local.workflow_internal_url
      }

      readiness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 8000
        path      = "/health"
        transport = "HTTP"
      }
    }
  }
}

# -------------------------------------------------------------
# 9. Next.js Frontend Container App
# (Runs Next.js standalone container with internal rewrites and SSR support)
# -------------------------------------------------------------
resource "azurerm_container_app" "frontend" {
  name                         = "frontend"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  ingress {
    external_enabled = true # Public entrypoint for users
    target_port      = 3000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = var.container_min_replicas
    max_replicas = var.container_max_replicas

    container {
      name   = "frontend"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/frontend:${var.image_tag}"
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name  = "NODE_ENV"
        value = "production"
      }
      env {
        name  = "NEXT_PUBLIC_AUTH_SERVICE_URL"
        value = "https://${azurerm_container_app.auth_service.latest_revision_fqdn}"
      }
      env {
        name  = "ANALYTICS_INTERNAL_URL"
        value = local.analytics_internal_url
      }
      env {
        name  = "AI_INTERNAL_URL"
        value = local.ai_internal_url
      }

      readiness_probe {
        port      = 3000
        path      = "/"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 3000
        path      = "/"
        transport = "HTTP"
      }
    }
  }
}

# -------------------------------------------------------------
# 9. Monitoring: Prometheus & Grafana Container Apps
# -------------------------------------------------------------

# --- Prometheus Container App ---
resource "azurerm_container_app" "prometheus" {
  name                         = "prometheus"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  ingress {
    external_enabled = false # Accessible internally to Grafana and within CAE
    target_port      = 9090
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 1
    max_replicas = 1

    container {
      name   = "prometheus"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/prometheus:${var.image_tag}"
      cpu    = 0.5
      memory = "1.0Gi"

      readiness_probe {
        port      = 9090
        path      = "/-/ready"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 9090
        path      = "/-/healthy"
        transport = "HTTP"
      }
    }
  }
}

# --- Grafana Container App ---
resource "azurerm_container_app" "grafana" {
  name                         = "grafana"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"
  tags                         = local.common_tags

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  secret {
    name  = "grafana-admin-password"
    value = var.grafana_admin_password
  }

  ingress {
    external_enabled = true # Public dashboard access with auth
    target_port      = 3000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 1
    max_replicas = 1

    container {
      name   = "grafana"
      image  = "${azurerm_container_registry.acr.login_server}/workpilot/grafana:${var.image_tag}"
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name  = "GF_SECURITY_ADMIN_USER"
        value = var.grafana_admin_user
      }
      env {
        name        = "GF_SECURITY_ADMIN_PASSWORD"
        secret_name = "grafana-admin-password"
      }
      env {
        name  = "GF_USERS_ALLOW_SIGN_UP"
        value = "false"
      }
      env {
        name  = "PROMETHEUS_URL"
        value = "http://prometheus.${azurerm_container_app_environment.env.default_domain}"
      }

      readiness_probe {
        port      = 3000
        path      = "/api/health"
        transport = "HTTP"
      }
      liveness_probe {
        port      = 3000
        path      = "/api/health"
        transport = "HTTP"
      }
    }
  }
}

