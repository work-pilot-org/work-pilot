output "resource_group_name" {
  description = "Name of the provisioned or targeted Azure Resource Group"
  value       = local.rg_name
}

output "acr_login_server" {
  description = "Azure Container Registry login server"
  value       = azurerm_container_registry.acr.login_server
}

output "postgres_fqdn" {
  description = "Fully qualified domain name of PostgreSQL Flexible Server"
  value       = azurerm_postgresql_flexible_server.postgres.fqdn
}

output "database_url_template" {
  description = "Application database connection URL string (credentials masked)"
  value       = "postgresql://${var.db_admin_username}:<DB_PASSWORD>@${azurerm_postgresql_flexible_server.postgres.fqdn}:5432/${azurerm_postgresql_flexible_server_database.workpilot_db.name}?sslmode=require"
}

output "container_app_environment_domain" {
  description = "Default domain for Azure Container Apps Environment"
  value       = azurerm_container_app_environment.env.default_domain
}

# --- Service Public URLs ---
output "frontend_url" {
  description = "Public URL for Next.js Frontend"
  value       = "https://${azurerm_container_app.frontend.latest_revision_fqdn}"
}

output "auth_service_url" {
  description = "Public URL for Auth Service"
  value       = "https://${azurerm_container_app.auth_service.latest_revision_fqdn}"
}

output "hr_service_url" {
  description = "Public URL for HR Service"
  value       = "https://${azurerm_container_app.hr_service.latest_revision_fqdn}"
}

output "it_service_url" {
  description = "Public URL for IT Service"
  value       = "https://${azurerm_container_app.it_service.latest_revision_fqdn}"
}

output "workflow_service_url" {
  description = "Public URL for Workflow Service"
  value       = "https://${azurerm_container_app.workflow_service.latest_revision_fqdn}"
}

output "notification_service_url" {
  description = "Public URL for Notification Service"
  value       = "https://${azurerm_container_app.notification_service.latest_revision_fqdn}"
}

output "analytics_service_url" {
  description = "Public URL for Analytics Service"
  value       = "https://${azurerm_container_app.analytics_service.latest_revision_fqdn}"
}

output "ai_service_url" {
  description = "Public URL for AI Service"
  value       = "https://${azurerm_container_app.ai_service.latest_revision_fqdn}"
}

# --- Monitoring URLs ---
output "grafana_url" {
  description = "Public URL for Grafana Monitoring Dashboards"
  value       = "https://${azurerm_container_app.grafana.latest_revision_fqdn}"
}

output "prometheus_internal_url" {
  description = "Internal URL for Prometheus"
  value       = "http://prometheus.${azurerm_container_app_environment.env.default_domain}"
}

