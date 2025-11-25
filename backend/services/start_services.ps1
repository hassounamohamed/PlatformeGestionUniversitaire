# Helper script to start local services used by the project
# Usage: run this from the repo root or double-click in Explorer

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Start auth_service on 127.0.0.1:8001
$authPath = Join-Path $repoRoot 'auth_service'
Write-Host "Starting auth_service in $authPath on port 8001..."
Start-Process -FilePath python -ArgumentList '-m','uvicorn','run:app','--host','127.0.0.1','--port','8001' -WorkingDirectory $authPath

# Start emploi_service on 127.0.0.1:8004
$emploiPath = Join-Path $repoRoot 'emploi_service'
Write-Host "Starting emploi_service in $emploiPath on port 8004..."
Start-Process -FilePath python -ArgumentList '-m','uvicorn','run:app','--host','127.0.0.1','--port','8004' -WorkingDirectory $emploiPath

Write-Host 'Services launched. Use Task Manager to inspect python processes, or check logs in their consoles.'
