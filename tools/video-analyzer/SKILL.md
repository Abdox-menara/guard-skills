# Skill: video-analyzer

# Video Analyzer - Automated Video Analysis

## Overview
Automated video analysis tool that extracts metadata, keyframes, audio, and generates comprehensive reports. Also used for diagnosing desktop problems from user-recorded videos.

## Capabilities
- **Metadata Extraction**: Video codec, resolution, FPS, bitrate, duration
- **Keyframe Extraction**: Extract frames at regular intervals for visual analysis
- **Audio Extraction**: Separate audio track for transcription
- **Thumbnail Generation**: Create preview thumbnails at key moments
- **Quality Analysis**: Score video quality and identify issues
- **HTML Reports**: Generate visual reports with all findings
- **Problem Diagnosis**: Analyze user-recorded videos to identify desktop/app issues

## Usage

### Basic Analysis
```powershell
.\Analyze-Video.ps1 -VideoPath "C:\video.mp4"
```

### Full Analysis (All Options)
```powershell
.\Analyze-Video.ps1 -VideoPath "C:\video.mp4" -All
```

### Specific Options
```powershell
.\Analyze-Video.ps1 -VideoPath "C:\video.mp4" -ExtractFrames -ExtractAudio -Detailed
```

### Quick Launch (Batch)
```batch
analyze-video.bat "C:\video.mp4" -All
```

## Output Structure
```
analysis_YYYYMMDD_HHMMSS/
├── metadata.json          # Raw ffprobe metadata
├── summary.json           # Parsed video summary
├── detailed_analysis.json # Quality scores and issues
├── report.html            # Visual HTML report
├── keyframes/             # Extracted frames (if enabled)
├── thumbnails/            # Preview thumbnails (if enabled)
└── audio.wav              # Extracted audio (if enabled)
```

## Quality Scoring
- **Resolution**: 1080p+ = 25pts, 720p+ = 15pts
- **Frame Rate**: 30+ FPS = 25pts, 24+ FPS = 15pts
- **Bitrate**: 5+ Mbps = 25pts, 2+ Mbps = 15pts
- **Audio**: Present = 25pts

## Workflow: Diagnosing Desktop Problems from Video

### Step 1: Analyze Video
```powershell
.\Analyze-Video.ps1 -VideoPath "C:\Users\Abdox\Desktop\problem-video.mp4" -All
```

### Step 2: Review Keyframes
- Open `keyframes/` folder
- Look at frames showing the problem
- Identify error messages, frozen states, UI issues

### Step 3: Read OCR Text (if available)
- Use `ocr-advanced` skill to extract text from frames
- Identify error codes, status messages

### Step 4: Research Solution
- Use `diagnose` skill for systematic troubleshooting
- Use `pc-control` skill to apply fixes
- Use `websearch` for known issues

### Step 5: Document Fix
- Update AGENTS.md with solution
- Create runbook entry if recurring issue

## Lessons Learned from Session 2026-07-10

### Video Analysis Best Practices
1. **Extract keyframes at 1fps** for desktop recordings - captures UI state changes
2. **Review thumbnails first** - quick overview before diving into frames
3. **Check video metadata** - low bitrate = poor quality, affects OCR accuracy
4. **Audio extraction** helps with narration transcription

### Windows Search Troubleshooting (Lessons Learned)
1. **Windows 11 Insider Preview** has known Search index bugs
2. **Search index database** (`Windows.edb`) location: `C:\ProgramData\Microsoft\Search\Data\Applications\Windows\`
3. **Service management** often requires admin rights
4. **Complete fix requires PC restart** for corrupted index

### Effective Problem Diagnosis Workflow
1. **Record the problem** - user captures video of issue
2. **Analyze with video-analyzer** - extract frames and metadata
3. **Visual inspection** - look at keyframes for error messages
4. **Apply fixes** - use appropriate tools (services, registry, etc.)
5. **Test and verify** - confirm fix worked
6. **Document** - add to knowledge base

## Related Skills
| Skill | Use Case |
|-------|----------|
| `ocr-advanced` | Extract text from video frames |
| `diagnose` | Systematic root cause analysis |
| `pc-control` | Apply Windows fixes |
| `websearch` | Research known issues |
| `ghost-snapshot` | Real-time screen capture |

## Requirements
- FFmpeg/FFprobe installed and in PATH
- PowerShell 5.1+
- Admin rights (for some fixes)

## Location
`C:\opencodes\guard skills\tools\video-analyzer\`

## Trigger Phrases
- "analyze video"
- "video analysis"
- "extract video metadata"
- "video quality check"
- "extract frames from video"
- "diagnose from video"
- "fix problem in video"

## Publishing to GitHub
This skill can be published to help other AI assistants:
```bash
cd C:\opencodes\guard skills\tools\video-analyzer
git init
git add .
git commit -m "Add video analyzer skill with desktop problem diagnosis"
git remote add origin https://github.com/Abdox-menara/video-analyzer-skill.git
git push -u origin main
```

## Alternatives Considered
| Tool | Pros | Cons |
|------|------|------|
| **video-analyzer** (this) | Fast, local, no API | Limited OCR |
| `ocr-advanced` | Better text extraction | Slower |
| `ghost-snapshot` | Real-time capture | Not for recorded video |
| Python + OpenCV | Most flexible | Requires setup |
| Online services | Easy to use | Privacy concerns |

---
**Version**: 1.1.0
**Last Updated**: 2026-07-11
**Status**: PRODUCTION READY