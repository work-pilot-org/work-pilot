# PowerShell Script: Build & Push WorkPilot Docker Images to Azure Container Registry
param(
    [Parameter(Mandatory=$true)]
    [string]$AcrName,

    [string]$Tag = "latest"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Building and Pushing WorkPilot Images to ACR: $AcrName" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Authenticate with ACR
Write-Host "`n--> Logging in to Azure Container Registry: $AcrName..." -ForegroundColor Yellow
az acr login --name $AcrName

$LoginServer = "$AcrName.azurecr.io"

# 2. Service list: Name -> Dockerfile path, Context path, and Target
$Services = @(
    @{ Name = "auth-service"; Dockerfile = "auth-service/Dockerfile"; Context = "."; Target = "prod" },
    @{ Name = "hr-service"; Dockerfile = "hr-service/Dockerfile"; Context = "."; Target = "prod" },
    @{ Name = "it-service"; Dockerfile = "it-service/Dockerfile"; Context = "."; Target = "prod" },
    @{ Name = "workflow-service"; Dockerfile = "workflow-service/Dockerfile"; Context = "."; Target = "prod" },
    @{ Name = "notification-service"; Dockerfile = "notification-service/Dockerfile"; Context = "."; Target = "prod" },
    @{ Name = "analytics-service"; Dockerfile = "analytics-service/Dockerfile"; Context = "."; Target = "prod" },
    @{ Name = "ai-service"; Dockerfile = "ai-service/Dockerfile"; Context = "."; Target = "prod" },
    @{ Name = "frontend"; Dockerfile = "frontend/Dockerfile"; Context = "./frontend"; Target = "prod" },
    @{ Name = "prometheus"; Dockerfile = "monitoring/prometheus/Dockerfile"; Context = "."; Target = "" },
    @{ Name = "grafana"; Dockerfile = "monitoring/grafana/Dockerfile"; Context = "."; Target = "" }
)

foreach ($svc in $Services) {
    $ImageName = "$LoginServer/workpilot/$($svc.Name):$Tag"
    Write-Host "`n--> Building $($svc.Name)..." -ForegroundColor Green
    
    if ($svc.Target) {
        docker build -f $svc.Dockerfile -t $ImageName --target $svc.Target $svc.Context
    } else {
        docker build -f $svc.Dockerfile -t $ImageName $svc.Context
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker build failed for $($svc.Name)"
    }

    Write-Host "--> Pushing $($svc.Name) to ACR..." -ForegroundColor Green
    docker push $ImageName
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker push failed for $($svc.Name)"
    }
}

Write-Host "`nAll images successfully built and pushed to $LoginServer!" -ForegroundColor Cyan
