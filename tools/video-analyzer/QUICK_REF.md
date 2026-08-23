# Video Analyzer - Quick Reference

## Location
`C:\opencodes\guard skills\tools\video-analyzer\`

## Quick Commands

### Analyze Video (All Options)
```powershell
powershell -ExecutionPolicy Bypass -File "C:\opencodes\guard skills\tools\video-analyzer\Analyze-Video.ps1" -VideoPath "VIDEO_PATH" -All
```

### Using Batch File
```batch
analyze-video.bat "VIDEO_PATH" -All
```

## Options
| Option | Description |
|--------|-------------|
| `-ExtractFrames` | Extract 1 frame per second |
| `-ExtractAudio` | Extract audio as WAV |
| `-GenerateThumbnails` | Create preview thumbnails |
| `-Detailed` | Quality analysis & scoring |
| `-All` | Enable all options |

## Output Location
Desktop: `analysis_YYYYMMDD_HHMMSS/`

## What It Does
1. ✅ Extracts video metadata (codec, resolution, FPS, bitrate)
2. ✅ Extracts keyframes for visual analysis
3. ✅ Extracts audio track for transcription
4. ✅ Generates thumbnail previews
5. ✅ Scores video quality (0-100)
6. ✅ Identifies issues and recommendations
7. ✅ Creates HTML report

## Requirements
- FFmpeg installed (already installed ✅)
- PowerShell 5.1+

## Example
```batch
analyze-video.bat "C:\Users\Abdox\Desktop\Recording 2026-07-10 234717.mp4" -All
```

## Results
Your video analysis is ready at:
`C:\Users\Abdox\Desktop\analysis_20260710_235308\`

Open `report.html` to view the full report.