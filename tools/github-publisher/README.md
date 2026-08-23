# GitHub Publisher

Auto-publish folders and skills to GitHub with one command. Creates repos, initializes git, and pushes code automatically.

## Features

- Auto-create GitHub repos (public/private)
- Initialize git if needed
- Push code automatically
- Handle existing repos
- Open in browser after publish

## Quick Start

```powershell
# Publish a folder
.\Publish-GitHub.ps1 -Path "C:\my-skill" -RepoName "my-skill"

# Publish with description and open in browser
.\Publish-GitHub.ps1 -Path "C:\my-skill" -RepoName "my-skill" -Description "My skill" -AutoOpen

# Publish as private
.\Publish-GitHub.ps1 -Path "C:\my-skill" -Private
```

## Requirements

- [GitHub CLI](https://cli.github.com/) (`gh`)
- GitHub account authenticated (`gh auth login`)

### Install GitHub CLI
```powershell
winget install GitHub.cli
gh auth login
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `-Path` | Yes | - | Path to folder to publish |
| `-RepoName` | No | Folder name | GitHub repo name |
| `-Description` | No | "Published with GitHub Publisher" | Repo description |
| `-Private` | No | false | Make repo private |
| `-AutoOpen` | No | false | Open in browser after publish |

## Use Cases

1. **Publish Skills**: Share AI assistant skills
2. **Publish Projects**: Upload code to GitHub
3. **Update Repos**: Push changes to existing repos
4. **Backup**: Quick backup to GitHub

## License

MIT