#!/usr/bin/env pwsh

# Defaults to 'build' and 'dist' but has options to disable them and enable other jobs

param (
    [Parameter(Mandatory=$false,HelpMessage="Clean files")][switch]$clean = $false,
    [Parameter(Mandatory=$false,HelpMessage="Update image files")][switch]$update_images = $false,
    [Parameter(Mandatory=$false,HelpMessage="Update web interfaces")][switch]$update_web_interfaces = $false,
    [Parameter(Mandatory=$false,HelpMessage="Build the program")][switch]$no_build = $false,
    [Parameter(Mandatory=$false,HelpMessage="Move built files to bin directory")][switch]$no_dist = $false,
    [Parameter(Mandatory=$false,HelpMessage="Create windows installer")][switch]$create_windows_installer = $false
)

# Make script stop when an error happens
$ErrorActionPreference = "Stop"

# Output state of parameter
Write-Host "build:                    $(-Not $no_build)"
Write-Host "dist:                     $(-Not $no_dist)"
Write-Host "clean:                    ${clean}"
Write-Host "update_images:            ${update_images}"
Write-Host "update_web_interfaces:    ${update_web_interfaces}"
Write-Host "create_windows_installer: ${create_windows_installer}"

$SRC_DIR = "DesktopClient"
$BIN_DIR = "bin"

if ($clean) {
    Remove-Item -Path $BIN_DIR -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "*.jar", "*.exe"
    Set-Location $SRC_DIR
    mvn clean
    Set-Location ..
}

if ($update_images) {
    Set-Location ImageResources
    python create_image_resources.py
    Set-Location ..
}

if ($update_web_interfaces) {
    Set-Location WebInterfaces
    python create_website_resources.py
    Set-Location ..
}

if (-Not $no_build) {
    Set-Location $SRC_DIR
    mvn install
    Set-Location ..
}

if (-Not $no_dist) {
    New-Item $BIN_DIR -ItemType Directory -ErrorAction SilentlyContinue
    Set-Location $SRC_DIR
    python format_exported_jar.py
    Set-Location ..
    $JAR_FILES=Join-Path -Path "." -ChildPath "*.jar"
    Copy-Item -Path $JAR_FILES -Destination $BIN_DIR -Recurse
}

if ($create_windows_installer) {
    Set-Location WindowsInstaller
    python build_windows_installer.py
    Set-Location ..
}
