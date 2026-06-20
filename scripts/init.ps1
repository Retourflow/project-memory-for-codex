param(
    [string]$ProjectPath = ".",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$SourceRoot = Split-Path -Parent $PSScriptRoot
$TargetRoot = (Resolve-Path -Path $ProjectPath).Path

New-Item -ItemType Directory -Force -Path "$TargetRoot/docs" | Out-Null
New-Item -ItemType Directory -Force -Path "$TargetRoot/scripts" | Out-Null

function Copy-ProjectMemoryFile {
    param(
        [string]$Source,
        [string]$Destination
    )

    if ((Test-Path $Destination) -and -not $Force) {
        Write-Host "Skipped existing file: $Destination"
        return
    }

    Copy-Item -Path $Source -Destination $Destination -Force
    Write-Host "Created: $Destination"
}

Copy-ProjectMemoryFile "$SourceRoot/templates/AGENTS.md" "$TargetRoot/AGENTS.md"
Copy-ProjectMemoryFile "$SourceRoot/templates/docs/PROJECT_CONTEXT.md" "$TargetRoot/docs/PROJECT_CONTEXT.md"
Copy-ProjectMemoryFile "$SourceRoot/templates/docs/CURRENT_STATE.md" "$TargetRoot/docs/CURRENT_STATE.md"
Copy-ProjectMemoryFile "$SourceRoot/templates/docs/ARCHITECTURE.md" "$TargetRoot/docs/ARCHITECTURE.md"
Copy-ProjectMemoryFile "$SourceRoot/templates/docs/DECISIONS.md" "$TargetRoot/docs/DECISIONS.md"
Copy-ProjectMemoryFile "$SourceRoot/templates/docs/CHANGELOG.md" "$TargetRoot/docs/CHANGELOG.md"
Copy-ProjectMemoryFile "$SourceRoot/scripts/validate.py" "$TargetRoot/scripts/validate.py"

Write-Host ""
Write-Host "Project memory initialized. Replace template statements with verified facts."
