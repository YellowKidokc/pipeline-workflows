param(
    [Parameter(Position = 0)]
    [string]$VaultPath
)

$ErrorActionPreference = "Stop"

if (-not $VaultPath) {
    $VaultPath = Read-Host "Enter the Obsidian vault path"
}

$resolvedVault = (Resolve-Path -LiteralPath $VaultPath).Path
$obsidianRoot = Join-Path $resolvedVault ".obsidian"
if (-not (Test-Path -LiteralPath $obsidianRoot)) {
    throw "Not an Obsidian vault: $resolvedVault"
}

$bundleRoot = Join-Path $PSScriptRoot "ObsidianPlugins"
$pluginRoot = Join-Path $obsidianRoot "plugins"
New-Item -ItemType Directory -Path $pluginRoot -Force | Out-Null

foreach ($plugin in Get-ChildItem -LiteralPath $bundleRoot -Directory) {
    $destination = Join-Path $pluginRoot $plugin.Name
    if (Test-Path -LiteralPath $destination) {
        Write-Host "Already installed; leaving unchanged: $destination"
        continue
    }

    Copy-Item -LiteralPath $plugin.FullName -Destination $destination -Recurse
    Write-Host "Installed: $($plugin.Name)"
}

Write-Host "Enable the plugins in Obsidian Settings > Community plugins."
