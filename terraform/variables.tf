variable "project_name" {
  type        = string
  description = "Project name prefix used for all resources"
  default     = "workpilot"
}

variable "environment" {
  type        = string
  description = "Deployment environment name (dev, staging, prod)"
  default     = "dev"
}

variable "location" {
  type        = string
  description = "Azure region to deploy resources in"
  default     = "eastus"
}

variable "resource_group_name" {
  type        = string
  description = "Name of existing Azure Resource Group to use (e.g., 'workpilot-rg'). If left empty, a new one named <project_name>-<environment>-rg will be managed."
  default     = ""
}

# -------------------------------------------------------------
# Database configuration
# -------------------------------------------------------------
variable "db_admin_username" {
  type        = string
  description = "Administrator username for PostgreSQL Flexible Server"
  default     = "workpilotadmin"
}

variable "db_admin_password" {
  type        = string
  description = "Administrator password for PostgreSQL. If left empty, a secure password will be generated automatically."
  default     = ""
  sensitive   = true
}

variable "db_sku_name" {
  type        = string
  description = "PostgreSQL Flexible Server compute tier (e.g., B_Standard_B1ms for low-cost dev)"
  default     = "B_Standard_B1ms"
}

variable "db_storage_mb" {
  type        = number
  description = "Storage size in MB for PostgreSQL Flexible Server (minimum is 32768 MB = 32 GB)"
  default     = 32768
}

# -------------------------------------------------------------
# Secrets and API Keys
# -------------------------------------------------------------
variable "jwt_secret_key" {
  type        = string
  description = "Secret key used for JWT signing across services. If left empty, an auto-generated random key will be used."
  default     = ""
  sensitive   = true
}

variable "gemini_api_key" {
  type        = string
  description = "Google Gemini API key required by ai-service"
  default     = ""
  sensitive   = true
}

variable "resend_api_key" {
  type        = string
  description = "Resend API key for sending emails via notification-service"
  default     = ""
  sensitive   = true
}

variable "email_from" {
  type        = string
  description = "Sender email address for notification-service"
  default     = "notifications@workpilot.com"
}

# -------------------------------------------------------------
# Container Image Registry & Tags
# -------------------------------------------------------------
variable "image_tag" {
  type        = string
  description = "Container image tag deployed for all services"
  default     = "latest"
}

# -------------------------------------------------------------
# Dev cost-saving options
# -------------------------------------------------------------
variable "container_min_replicas" {
  type        = number
  description = "Minimum replicas for Container Apps. Set to 0 to enable scale-to-zero when idle (saves costs for dev)."
  default     = 0
}

variable "container_max_replicas" {
  type        = number
  description = "Maximum replicas for Container Apps during traffic"
  default     = 2
}

# -------------------------------------------------------------
# Monitoring configuration
# -------------------------------------------------------------
variable "grafana_admin_user" {
  type        = string
  description = "Grafana admin username"
  default     = "admin"
}

variable "grafana_admin_password" {
  type        = string
  description = "Grafana admin password"
  default     = "AdminSecure123!"
  sensitive   = true
}

