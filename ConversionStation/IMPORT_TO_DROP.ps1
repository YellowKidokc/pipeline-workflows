param(
    [Parameter(Position = 0)]
    [string]$Source
)

$ErrorActionPreference = "Stop"
$stationRoot = $PSScriptRoot
$dropRoot = Join-Path $stationRoot "Workspace\DROP"

if (-not $Source) {
    $Source = Read-Host "Enter a file or folder path"
}

$resolvedSource = (Resolve-Path -LiteralPath $Source).Path
New-Item -ItemType Directory -Path $dropRoot -Force | Out-Null

$sourceItem = Get-Item -LiteralPath $resolvedSource
$destination = Join-Path $dropRoot $sourceItem.Name
if (Test-Path -LiteralPath $destination) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $destination = Join-Path $dropRoot ("{0}_{1}" -f $stamp, $sourceItem.Name)
}

Copy-Item -LiteralPath $resolvedSource -Destination $destination -Recurse
Write-Host "Copied without changing the source: $destination"
