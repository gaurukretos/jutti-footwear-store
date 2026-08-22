param(
    [Parameter(Mandatory = $true)]
    [string]$PostgresPassword,

    [string]$PostgresPort = "5432"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Dabi Jutti House - Database Setup ===" -ForegroundColor Cyan

$env:POSTGRES_PASSWORD = $PostgresPassword
$env:POSTGRES_PORT = $PostgresPort

Set-Location $projectRoot
python scripts/create_db.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Port 5432 failed? Trying PostgreSQL 16 on port 5433..." -ForegroundColor Yellow
    $env:POSTGRES_PORT = "5433"
    python scripts/create_db.py
}

if ($LASTEXITCODE -eq 0) {
    python manage.py migrate
    python manage.py seed_data
    Write-Host ""
    Write-Host "All done! Run: python manage.py runserver" -ForegroundColor Green
}
