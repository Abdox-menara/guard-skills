# Video Processing — Quality Perf

> Split from SKILL.md to keep the main skill under ~150 lines (progressive disclosure).

## Anti-Patterns & Fixes

### P0 — Critical

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| Double encoding | Two lossy codecs applied | Use `-c:v copy` or single codec |
| Missing `-movflags +faststart` | MP4 for web without faststart | Add `-movflags +faststart` |
| CRF 0 (lossless) for delivery | `-crf 0` in production | Use CRF 18-28 for delivery |
| Wrong pixel format | `-pix_fmt yuv420p` missing | Add `-pix_fmt yuv420p` for compatibility |
| Interlaced output | No deinterlace on old sources | Add `-vf yadif` or `-vf bwdif` |

### P1 — High

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| Unbounded bitrate | `-b:v` without `-maxrate` | Add `-maxrate` and `-bufsize` |
| Wrong aspect ratio | Stretched/striked video | Use `-vf "scale=-2:HEIGHT"` |
| Audio sync drift | Long videos with VBR | Use `-af aresample=async=1` |
| Missing keyframes | `-g` not set for streaming | Set `-g` to half frame rate |
| Hardcoded subs in master | Subs in HLS master track | Extract to separate track |

### P2 — Medium

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| Inefficient preset | `-preset veryslow` in batch | Use `medium` for balance |
| No audio normalization | Uneven volume levels | Add `-af loudnorm` |
| Wrong color space | HDR→SDR without tonemap | Add `-vf zscale=t=linear:npl=100,tonemap=tonemap=hable` |
| Redundant streams | Duplicate video tracks | Use `-map 0:v:0` |
| Large thumbnails | Full resolution frame grab | Add `-vf scale=320:-1` |

---

## 21. Advanced Anti-Patterns

### P0 — Critical (continued)

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| HDR without tonemap | HDR input → SDR output, no tonemap | Add zscale+tonemap filter |
| Lossy re-encode for trim | `-ss` with codec re-encode | Use `-c copy` when possible |
| Missing deinterlace | Interlaced source, no yadif/bwdif | Add deinterlace filter |
| Wrong pixel format for web | `yuv444p` or `yuv422p` for delivery | Add `-pix_fmt yuv420p` |
| Unseekable MP4 | No `+faststart` for streaming | Add `-movflags +faststart` |

### P1 — High (continued)

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| No loudness normalization | Multiple videos, inconsistent levels | Apply `loudnorm` filter |
| Stretched text overlay | `drawtext` without font aspect | Set `fontsize` relative to resolution |
| Wrong keyframe interval | `-g 300` for 30fps streaming | Set `-g` to 2× frame rate |
| Missing audio in concat | Stream mapping skips audio | Add `-map 0:a` explicitly |
| Hardcoded CRF for all content | Same CRF for animation vs live-action | Adjust CRF by content type |

### P2 — Medium (continued)

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| Excessive B-frames | `-bf 4` for streaming | Use `-bf 2` max for compatibility |
| Wrong color matrix | BT.601 for HD content | Use `-colorspace bt709` for 720p+ |
| Over-compressed audio | 64k AAC for music content | Use 192k+ for music |
| No metadata preservation | Strip all metadata on transcode | Add `-map_metadata 0` |
| Inefficient GIF | No palette optimization | Use two-pass palette method |

---

## 22. Performance Optimization

```bash
# Limit CPU threads
ffmpeg -threads 4 -i input.mp4 -c:v libx264 output.mp4

# Ultrafast preset (live/realtime)
ffmpeg -i input.mp4 -c:v libx264 -preset ultrafast -crf 23 output.mp4

# Zero-copy (remux only)
ffmpeg -i input.mp4 -c copy -f mp4 output.mp4

# Hardware decode + software encode
ffmpeg -hwaccel auto -i input.mp4 -c:v libx264 -crf 23 output.mp4

# CUDA decode + NVENC encode (fastest)
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i input.mp4 -c:v h264_nvenc -preset p4 -cq 23 output.mp4

# Benchmark filter graph
ffmpeg -i input.mp4 -vf "null" -f null - 2>&1 | grep "speed="

# Profile encoding speed
ffmpeg -benchmark -i input.mp4 -c:v libx264 -crf 23 -f null - 2>&1 | grep "bench"
```

---

## 23. CI/CD & Automation Patterns

### GitHub Actions — Multi-Resolution Pipeline

```yaml
name: Video Transcode Pipeline
on: [push]
jobs:
  transcode:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        preset:
          - { name: "1080p", scale: "1920:1080", crf: "23", audio: "128k" }
          - { name: "720p", scale: "1280:720", crf: "26", audio: "96k" }
          - { name: "480p", scale: "854:480", crf: "28", audio: "64k" }
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y ffmpeg
      - run: |
          for f in videos/*.mov; do
            name=$(basename "${f%.mov}")
            ffmpeg -i "$f" -vf "scale=${{ matrix.preset.scale }}:force_original_aspect_ratio=decrease" \
              -c:v libx264 -crf ${{ matrix.preset.crf }} -preset medium \
              -c:a aac -b:a ${{ matrix.preset.audio }} \
              -movflags +faststart "output/${name}_${{ matrix.preset.name }}.mp4"
          done
      - uses: actions/upload-artifact@v4
        with:
          name: videos-${{ matrix.preset.name }}
          path: output/
```

### Python Batch Processor

```python
import subprocess, json, os
from pathlib import Path

def batch_transcode(input_dir: str, output_dir: str, crf: int = 23):
    os.makedirs(output_dir, exist_ok=True)
    for f in Path(input_dir).glob("*.mov"):
        out = Path(output_dir) / f"{f.stem}.mp4"
        cmd = [
            "ffmpeg", "-y", "-i", str(f),
            "-c:v", "libx264", "-crf", str(crf), "-preset", "medium",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            str(out)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FAIL: {f.name}\n{result.stderr}")
        else:
            size_mb = out.stat().st_size / (1024 * 1024)
            print(f"OK: {f.name} → {out.name} ({size_mb:.1f} MB)")

batch_transcode("./raw", "./output", crf=23)
```

### PowerShell Web Optimizer

```powershell
function Optimize-VideoForWeb {
    param(
        [string]$InputPath,
        [string]$OutputPath = ".",
        [int]$CRF = 23,
        [string]$AudioBitrate = "128k"
    )
    $name = [System.IO.Path]::GetFileNameWithoutExtension($InputPath)
    $out = Join-Path $OutputPath "$name.web.mp4"
    ffmpeg -i $InputPath `
        -c:v libx264 -crf $CRF -preset medium -pix_fmt yuv420p `
        -c:a aac -b:a $AudioBitrate `
        -movflags +faststart $out
    Write-Host "Done: $out ($([math]::Round((Get-Item $out).Length / 1MB, 1)) MB)"
}
```

---

**Version**: 2.1.0
**Status**: PRODUCTION READY
**Requires**: FFmpeg 6.0+, FFprobe
