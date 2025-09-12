#!/usr/bin/env pwsh

# PowerShell equivalent of Makefile commands

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "stop", "logs", "build", "clean", "help")]
    [string]$Command = "help"
)

switch ($Command) {
    "run" {
        Write-Host "Starting containers..." -ForegroundColor Green
        docker-compose up -d
    }
    "stop" {
        Write-Host "Stopping containers..." -ForegroundColor Yellow
        docker-compose down
    }
    "logs" {
        Write-Host "Showing logs..." -ForegroundColor Blue
        docker-compose logs -f recipe-bot
    }
    "build" {
        Write-Host "Building and starting containers..." -ForegroundColor Green
        docker-compose up --build -d
    }
    "clean" {
        Write-Host "Cleaning up containers and volumes..." -ForegroundColor Red
        docker-compose down --volumes --remove-orphans
    }
    "help" {
        Write-Host "Available commands:" -ForegroundColor Cyan
        Write-Host "  run    - Start containers (docker-compose up -d)"
        Write-Host "  stop   - Stop containers (docker-compose down)"
        Write-Host "  logs   - Show container logs"
        Write-Host "  build  - Build and start containers"
        Write-Host "  clean  - Remove containers and volumes"
        Write-Host ""
        Write-Host "Usage: .\run.ps1 [command]"
        Write-Host "Example: .\run.ps1 run"
    }
}
