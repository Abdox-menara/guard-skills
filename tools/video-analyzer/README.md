# Video Analyzer Skill

A PowerShell-based video analysis tool for AI assistants. Extracts metadata, keyframes, audio, and generates quality reports. Also diagnoses desktop problems from user-recorded videos.

## Features

- **Metadata Extraction**: Video codec, resolution, FPS, bitrate, duration
- **Keyframe Extraction**: 1fps frames for visual analysis
- **Audio Extraction**: Separate audio track
- **Thumbnail Generation**: Preview thumbnails at key moments
- **Quality Scoring**: 0-100 score with recommendations
- **HTML Reports**: Visual reports with all findings
- **Problem Diagnosis**: Analyze user-recorded desktop issues

## Quick Start

```powershell
# Basic analysis
.\Analyze-Video.ps1 -VideoPath "C:\video.mp4"

# Full analysis with all options
.\Analyze-Video.ps1 -VideoPath "C:\video.mp4" -All

# Batch launcher
analyze-video.bat "C:\video.mp4" -All
```

## Requirements

- FFmpeg/FFprobe (in PATH)
- PowerShell 5.1+

## Output

```
analysis_YYYYMMDD_HHMMSS/
├── metadata.json
├── summary.json
├── detailed_analysis.json
├── report.html
├── keyframes/
├── thumbnails/
└── audio.wav
```

## Use Cases

1. **Video Quality Analysis**: Check codec, resolution, bitrate
2. **Desktop Problem Diagnosis**: Analyze user-recorded issues
3. **Content Extraction**: Get frames for OCR/analysis
4. **Batch Processing**: Analyze multiple videos

## Integration with AI Assistants

This skill is designed for chat AIs (ChatGPT, Claude, Gemini, etc.) to:

1. Receive video from user
2. Run video-analyzer to extract frames
3. Visually inspect frames for problems
4. Provide solutions based on findings

## License

MIT

## Contributing

Pull requests welcome! See SKILL.md for detailed documentation.