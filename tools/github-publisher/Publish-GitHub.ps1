<#
.SYNOPSIS
    GitHub Publisher - Auto-publish folders/repos to GitHub
.DESCRIPTION
    Automates creating GitHub repos and pushing code
.PARAMETER Path
    Path to folder/file to publish
.PARAMETER RepoName
    GitHub repo name (optional, uses folder name)
.PARAMETER Description
    Repo description
.PARAMETER Private
    Make repo private (default: public)
.PARAMETER AutoOpen
    Open repo in browser after publish
.EXAMPLE
    .\Publish-GitHub.ps1 -Path "C:\my-skill" -RepoName "my-skill" -Description "My awesome skill"
.EXAMPLE
    .\Publish-GitHub.ps1 -Path "C:\my-skill" -Private
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Path,
    
    [string]$RepoName,
    [string]$Description = "Published with GitHub Publisher",
    [switch]$Private,
    [switch]$AutoOpen,
    [switch]$Force
)

# Validate path
if (-not (Test-Path $Path)) {
    Write-Error "Path not found: $Path"
    exit 1
}

# Get folder name if not provided
if (-not $RepoName) {
    $RepoName = (Get-Item $Path).Name
}

Write-Host "=== GitHub Publisher ===" -ForegroundColor Cyan
Write-Host "Source: $Path"
Write-Host "Repo: $RepoName"
Write-Host "Visibility: $(if($Private){'Private'}else{'Public'})"
Write-Host ""

# Check gh CLI
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI (gh) not installed. Install: winget install GitHub.cli"
    exit 1
}

# Check if already a git repo
$isGitRepo = Test-Path (Join-Path $Path ".git")

if (-not $isGitRepo) {
    Write-Host "1. Initializing git repo..." -ForegroundColor Yellow
    
    # Use temp directory for clean push
    $tempDir = "$env:TEMP\github-publisher-$(Get-Date -Format 'yyyyMMddHHmmss')"
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    
    # Copy files
    Copy-Item "$Path\*" -Destination $tempDir -Recurse -Force
    
    # Init git
    Push-Location $tempDir
    git init
    git add .
    git commit -m "Initial commit"
    Pop-Location
    
    $sourcePath = $tempDir
} else {
    Write-Host "1. Using existing git repo..." -ForegroundColor Yellow
    $sourcePath = $Path
}

# Check if repo exists
Write-Host "2. Checking if repo exists..." -ForegroundColor Yellow
$repoExists = gh repo view "$env:GH_USER/$RepoName" 2>&1
if ($repoExists -like "*Not Found*" -or $LASTEXITCODE -ne 0) {
    # Create new repo
    Write-Host "   Creating new repo..." -ForegroundColor Yellow
    $visibility = if ($Private) { "--private" } else { "--public" }
    
    Push-Location $sourcePath
    gh repo create $RepoName $visibility --description $Description --source . --push
    Pop-Location
    
    Write-Host "   Repo created and pushed!" -ForegroundColor Green
} else {
    # Repo exists - push to it
    Write-Host "   Repo exists - pushing changes..." -ForegroundColor Yellow
    
    Push-Location $sourcePath
    git remote remove origin 2>$null
    git remote add origin "https://github.com/$env:GH_USER/$RepoName.git"
    git push -u origin main --force
    Pop-Location
    
    Write-Host "   Changes pushed!" -ForegroundColor Green
}

# Cleanup temp dir
if ($sourcePath -like "*github-publisher-*") {
    Remove-Item $sourcePath -Recurse -Force -ErrorAction SilentlyContinue
}

# Open in browser
if ($AutoOpen) {
    Write-Host "3. Opening in browser..." -ForegroundColor Yellow
    gh repo view "$env:GH_USER/$RepoName" --web
}

Write-Host "`n=== Published Successfully! ===" -ForegroundColor Green
Write-Host "URL: https://github.com/$env:GH_USER/$RepoName" -ForegroundColor Cyan