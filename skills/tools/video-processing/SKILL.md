---
name: video-processing
version: 2.0.0
author: Abdox
description: |
  ULTRA-ADVANCED video processing - Video processing, transcoding, streaming, and optimization.
  Handles FFmpeg pipelines, format conversion, codec selection, quality tuning,
  adaptive streaming, and video analysis.

  CAPABILITIES:
  - Video transcoding (H.264, H.265/HEVC, VP9, AV1, ProRes)
  - Audio transcoding (AAC, Opus, MP3, FLAC, PCM)
  - Format conversion (MP4, MKV, WebM, MOV, AVI, TS)
  - Resolution scaling and aspect ratio handling
  - Frame rate conversion and interpolation
  - Bitrate control (CBR, VBR, CRF, 2-pass)
  - Thumbnail and poster frame extraction
  - Subtitle burn-in and extraction (SRT, ASS, VTT)
  - Video trimming and concatenation
  - Filter graphs (crop, scale, deinterlace, denoise, watermark)
  - Adaptive streaming (HLS, DASH, CMAF)
  - Video quality analysis (SSIM, VMAF, PSNR)
  - Container metadata manipulation
  - Hardware acceleration detection (NVENC, VAAPI, QSV, AMF)
  - Batch processing and automation scripts
  - Error detection and recovery

  TRIGGER PHRASES: "video processing, transcoding, ffmpeg, video streaming,
    video conversion, codec, bitrate, hls, dash, watermark video,
    extract frames, video thumbnail, video compression, video quality"

  ENVIRONMENT: Windows/Linux/macOS, FFmpeg 6.x+, Python 3.10+, bash/powershell
---

# Video Processing — ULTRA-ADVANCED v2.0

## Overview

Complete video processing toolkit covering transcoding, streaming, analysis, and optimization with FFmpeg as the core engine.

## Quick Reference

### Prerequisites
- **FFmpeg** 6.0+ (check: `ffmpeg -version`)
- **FFprobe** (bundled with FFmpeg)
- **Python 3.10+** (for scripting helpers)
- **MediaInfo** (optional, for deep metadata inspection)

### Mode Selection

| Mode | Trigger | Action |
|------|---------|--------|
| **Audit** | `video audit`, `check video pipeline` | Scan project for video processing issues |
| **Fix** | `fix video`, `optimize transcoding` | Generate corrected FFmpeg commands/scripts |
| **Report** | `video report`, `transcoding analysis` | Full analysis with quality scoring |
| **Convert** | `convert video`, `transcode` | Generate conversion commands |
| **Stream** | `setup streaming`, `create hls` | Generate adaptive streaming output |
| **Analyze** | `analyze video`, `video quality` | Probe and report video metrics |

---

## References (progressive disclosure)

- [Codec Reference](references/codec-reference.md)
- [Workflows](references/workflows.md)
- [Analysis](references/analysis.md)
- [Advanced Filters](references/advanced-filters.md)
- [Quality Perf](references/quality-perf.md)

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Error opening input` | Corrupt or unsupported file | Try `-err_detect ignore_err` |
| `Invalid encoder` | Codec not compiled | Check `ffmpeg -encoders` |
| `Too many packets buffered` | Large GOP or B-frames | Reduce `-max_muxing_queue_size` |
| `Timestamp discontinuity` | Concat mismatched streams | Re-encode with `-async 1` |
| `Output file is empty` | Wrong stream mapping | Check `-map` or remove it |
| `codec frame size` | Resolution mismatch in concat | Re-encode both inputs |

---

## Trigger Phrases

- video processing
- transcoding
- ffmpeg
- video streaming
- video conversion
- codec selection
- bitrate control
- hls / dash streaming
- watermark video
- extract frames / thumbnails
- video compression
- video quality analysis
- batch transcode
- adaptive streaming
- subtitle burn-in
- hardware acceleration

---

## See Also

- [audio-processing](../audio-processing/SKILL.md)
- [batch-processing](../batch-processing/SKILL.md)
- [image-processing](../image-processing/SKILL.md)
