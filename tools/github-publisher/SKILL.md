# Skill: github-publisher

# GitHub Publisher - Auto-publish to GitHub

## Overview
Automate publishing folders and skills to GitHub. Creates repos, initializes git, and pushes code with one command.

## Capabilities
- **Auto-create GitHub repos** (public or private)
- **Initialize git** if not already a repo
- **Push code** to GitHub automatically
- **Handle existing repos** - update/push changes
- **Open in browser** after publish

## Quick Start

### Publish a folder
```powershell
.\Publish-GitHub.ps1 -Path "C:\my-skill" -RepoName "my-skill"
```

### Publish with description
```powershell
.\Publish-GitHub.ps1 -Path "C:\my-skill" -RepoName "my-skill" -Description "My awesome skill"
```

### Publish as private
```powershell
.\Publish-GitHub.ps1 -Path "C:\my-skill" -Private
```

### Publish and open in browser
```powershell
.\Publish-GitHub.ps1 -Path "C:\my-skill" -AutoOpen
```

### Batch launcher
```batch
publish-github.bat "C:\my-skill" -RepoName "my-skill" -AutoOpen
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-Path` | Yes | Path to folder to publish |
| `-RepoName` | No | GitHub repo name (uses folder name if not set) |
| `-Description` | No | Repo description |
| `-Private` | No | Make repo private (default: public) |
| `-AutoOpen` | No | Open repo in browser after publish |

## Workflow

1. **Check path** - Validate source folder exists
2. **Init git** - Initialize if not already a repo
3. **Check repo** - See if repo exists on GitHub
4. **Create/Push** - Create new repo or push to existing
5. **Cleanup** - Remove temp files
6. **Open** - Optionally open in browser

## Requirements
- GitHub CLI (`gh`) installed
- GitHub account authenticated (`gh auth login`)

## Install GitHub CLI
```powershell
winget install GitHub.cli
gh auth login
```

## Use Cases

### Publish a Skill
```powershell
.\Publish-GitHub.ps1 -Path "C:\opencodes\guard skills\tools\video-analyzer" -RepoName "video-analyzer-skill" -Description "Video analyzer for AI assistants"
```

### Publish a Project
```powershell
.\Publish-GitHub.ps1 -Path "C:\my-project" -RepoName "my-project" -Private -AutoOpen
```

### Update Existing Repo
```powershell
.\Publish-GitHub.ps1 -Path "C:\existing-repo" -RepoName "existing-repo"
```

## Lessons Learned

1. **Use temp directory** - Avoids git permission issues
2. **Check if repo exists** - Prevents duplicate creation errors
3. **Force push** - Updates existing repos cleanly
4. **Auto-open** - Quick verification after publish

## Related Skills
| Skill | Use Case |
|-------|----------|
| `video-analyzer` | Skill to publish |
| `commit-guard` | Validate commit messages |
| `readme-guard` | Ensure README quality |

## Location
`C:\opencodes\guard skills\tools\github-publisher\`

## Trigger Phrases
- "publish to github"
- "push to github"
- "create github repo"
- "upload to github"
- "git publish"

---
**Version**: 1.0.0
**Status**: PRODUCTION READY