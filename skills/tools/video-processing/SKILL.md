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

## Codec & Container Reference

### Video Codecs

| Codec | Quality | Speed | File Size | Use Case |
|-------|---------|-------|-----------|----------|
| H.264 (libx264) | Good | Fast | Medium | Universal compatibility |
| H.265/HEVC (libx265) | Excellent | Slow | Small | 4K, streaming bandwidth |
| VP9 (libvpx-vp9) | Excellent | Slow | Small | WebM, YouTube |
| AV1 (libsvtav1) | Best | Very Slow | Smallest | Next-gen streaming |
| ProRes (prores_ks) | Lossless | Fast | Large | Editing, mastering |
| DNxHD/DNxHR | Lossless | Fast | Large | Avid workflows |

### Audio Codecs

| Codec | Quality | Bitrate Range | Use Case |
|-------|---------|---------------|----------|
| AAC (libfdk_aac) | Good | 64-320 kbps | Streaming, general |
| Opus | Excellent | 32-512 kbps | Low-latency, WebRTC |
| MP3 (libmp3lame) | Good | 128-320 kbps | Legacy compatibility |
| FLAC | Lossless | Variable | Archival |
| PCM (pcm_s16le) | Lossless | Variable | Editing, broadcast |

### Containers

| Container | Video Codecs | Audio Codecs | Streaming |
|-----------|-------------|--------------|-----------|
| MP4 | H.264, H.265, AV1 | AAC, MP3 | HLS (via fMP4) |
| MKV | All | All | No |
| WebM | VP8, VP9, AV1 | Vorbis, Opus | DASH |
| MOV | H.264, ProRes | AAC, PCM | No |
| TS | H.264, H.265 | AAC, MP3 | HLS native |

---

## Common Workflows

### 1. Basic Transcoding

```bash
# H.264 MP4 (universal)
ffmpeg -i input.mov -c:v libx264 -crf 23 -preset medium \
  -c:a aac -b:a 128k -movflags +faststart output.mp4

# H.265 MP4 (50% smaller, same quality)
ffmpeg -i input.mov -c:v libx265 -crf 28 -preset medium \
  -tag:v hvc1 -c:a aac -b:a 128k output.mp4

# VP9 WebM (web-optimized)
ffmpeg -i input.mov -c:v libvpx-vp9 -crf 30 -b:v 2M \
  -c:a libopus -b:a 128k output.webm
```

### 2. Bitrate Control Modes

```bash
# CRF (Constant Rate Factor) — BEST for quality
# Lower = better quality, larger file. Typical: 18-28
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4

# 2-pass VBR — BEST for file size targeting
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -an -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 -c:a aac output.mp4

# CBR (Constant Bitrate) — for streaming with strict bandwidth
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -minrate 2M -maxrate 2M -bufsize 1M output.mp4
```

### 3. Resolution & Scaling

```bash
# Scale to 1080p (maintain aspect ratio)
ffmpeg -i input.mp4 -vf "scale=-2:1080" -c:v libx264 -crf 23 output.mp4

# Scale to 720p with pad (fill 16:9 frame)
ffmpeg -i input.mp4 -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" output.mp4

# Crop and scale
ffmpeg -i input.mp4 -vf "crop=1920:1080:0:0,scale=-2:720" output.mp4

# Letterbox for cinematic
ffmpeg -i input.mp4 -vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" output.mp4
```

### 4. Frame Rate

```bash
# Convert to 30fps (drop frames)
ffmpeg -i input.mp4 -r 30 -c:v libx264 -crf 23 output.mp4

# Convert to 24fps (film look)
ffmpeg -i input.mp4 -vf "fps=24" -c:v libx264 -crf 23 output.mp4

# Interpolate to 60fps (motion smoothing)
ffmpeg -i input.mp4 -vf "minterpolate=fps=60:mi_mode=mci" -c:v libx264 -crf 23 output.mp4
```

### 5. Trimming & Concatenation

```bash
# Trim (fast, no re-encode)
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:30 -c copy output.mp4

# Trim (accurate, re-encode)
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:30 -c:v libx264 -crf 23 -c:a aac output.mp4

# Concat (same codec)
echo "file 'part1.mp4'" > list.txt
echo "file 'part2.mp4'" >> list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Concat (different codecs — re-encode)
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -crf 23 -c:a aac output.mp4
```

### 6. Thumbnail & Poster Extraction

```bash
# Single thumbnail at 10 seconds
ffmpeg -i input.mp4 -ss 00:00:10 -vframes 1 -q:v 2 thumbnail.jpg

# Poster frame (middle of video)
ffmpeg -i input.mp4 -vf "select=eq(n\,0)" -vframes 1 poster.jpg

# Grid of thumbnails (4x4)
ffmpeg -i input.mp4 -vf "fps=1/10,scale=320:-1,tile=4x4" thumbnails.png

# Thumbnail every 30 seconds
ffmpeg -i input.mp4 -vf "fps=1/30" -q:v 2 thumb_%04d.jpg
```

### 7. Subtitles

```bash
# Burn subtitles into video
ffmpeg -i input.mp4 -vf "subtitles=subs.srt:force_style='FontSize=24'" output.mp4

# Extract subtitles
ffmpeg -i input.mp4 -map 0:s:0 output.srt

# Soft subtitle (MKV only)
ffmpeg -i input.mp4 -i subs.srt -c copy -c:s srt output.mkv
```

### 8. Watermark

```bash
# Image watermark (top-right, 10px margin)
ffmpeg -i input.mp4 -i logo.png -filter_complex \
  "overlay=W-w-10:10" output.mp4

# Text watermark
ffmpeg -i input.mp4 -vf \
  "drawtext=text='SAMPLE':fontsize=24:fontcolor=white:x=W-tw-10:y=10" output.mp4
```

### 9. Adaptive Streaming

```bash
# HLS (HTTP Live Streaming) — multi-bitrate
ffmpeg -i input.mp4 \
  -map 0:v -map 0:a -map 0:v -map 0:a -map 0:v -map 0:a \
  -c:v libx264 -crf 23 -c:a aac -b:a 128k \
  -b:v:0 5M -maxrate:v:0 5M -bufsize:v:0 10M \
  -b:v:1 3M -maxrate:v:1 3M -bufsize:v:1 6M \
  -b:v:2 1M -maxrate:v:2 1M -bufsize:v:2 2M \
  -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" \
  -master_pl_name master.m3u8 \
  -f hls -hls_time 6 -hls_list_size 0 \
  -hls_segment_filename "stream_%v/segment_%03d.ts" \
  output_%v.m3u8

# DASH (MPEG-DASH)
ffmpeg -i input.mp4 \
  -c:v libx264 -crf 23 -c:a aac -b:a 128k \
  -b:v 3M -bufsize:v 6M \
  -bf 2 -g 60 -keyint_min 60 \
  -use_timeline 1 -use_template 1 \
  -seg_duration 6 -init_seg_name 'init-$RepresentationID$.m4s' \
  -media_seg_name 'chunk-$RepresentationID$-$Number%05d$.m4s' \
  -f dash output.mpd
```

### 10. Hardware Acceleration

```bash
# NVIDIA NVENC
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p4 -cq 23 -c:a aac output.mp4

# Intel QSV
ffmpeg -i input.mp4 -c:v h264_qsv -preset medium -c:a aac output.mp4

# AMD AMF
ffmpeg -i input.mp4 -c:v h264_amf -quality balanced -c:a aac output.mp4

# VAAPI (Linux)
ffmpeg -vaapi_device /dev/dri/renderD128 -i input.mp4 \
  -vf 'format=nv12,hwupload' -c:v h264_vaapi -c:a aac output.mp4
```

---

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

## Video Analysis Commands

```bash
# Probe video info
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Quick summary
ffprobe -v quiet -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_name,width,height,r_frame_rate,bit_rate \
  -of compact input.mp4

# Quality metrics (SSIM)
ffmpeg -i input.mp4 -i reference.mp4 -lavfi ssim -f null -

# Quality metrics (PSNR)
ffmpeg -i input.mp4 -i reference.mp4 -lavfi psnr -f null -

# Detect interlacing
ffmpeg -i input.mp4 -vf idet -frames:v 1000 -f rawvideo -an -

# Audio loudness (EBU R128)
ffmpeg -i input.mp4 -af loudnorm=print_format=json -f null -

# Frame count
ffprobe -v quiet -count_frames -select_streams v:0 \
  -show_entries stream=nb_read_frames -of csv=p=0 input.mp4
```

---

## Batch Processing Patterns

### Rename & Transcode (bash)

```bash
for f in *.mov; do
  ffmpeg -i "$f" -c:v libx264 -crf 23 -c:a aac -b:a 128k \
    -movflags +faststart "${f%.mov}.mp4"
done
```

### Batch Thumbnails (PowerShell)

```powershell
Get-ChildItem *.mp4 | ForEach-Object {
    $thumb = $_.BaseName + "_thumb.jpg"
    ffmpeg -i $_.FullName -ss 00:00:05 -vframes 1 -q:v 2 $thumb
}
```

### Parallel Transcode (GNU parallel)

```bash
ls *.mov | parallel -j 4 'ffmpeg -i {} -c:v libx264 -crf 23 -c:a aac {.}.mp4'
```

---

## Quality Presets

| Preset | CRF | Preset | Audio | Use Case |
|--------|-----|--------|-------|----------|
| **Web (Fast)** | 23 | fast | 128k AAC | General web delivery |
| **Web (Quality)** | 18 | medium | 192k AAC | Portfolio, showcase |
| **Archive** | 15 | slow | lossless FLAC | Mastering, archival |
| **Streaming (720p)** | 26 | medium | 96k AAC | Bandwidth-constrained |
| **Streaming (1080p)** | 23 | medium | 128k AAC | Standard streaming |
| **Streaming (4K)** | 20 | slow | 192k AAC | High-end streaming |
| **Mobile** | 28 | fast | 64k AAC | Mobile data savings |
| **Thumbnail** | N/A | N/A | N/A | `-ss TIME -vframes 1 -q:v 2` |

---

## Integration Patterns

### FFmpeg in Python

```python
import subprocess, json

def probe(video_path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", video_path
    ]
    return json.loads(subprocess.check_output(cmd))

def transcode(input_path: str, output_path: str, crf: int = 23) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-c:v", "libx264", "-crf", str(crf), "-preset", "medium",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", output_path
    ]
    subprocess.run(cmd, check=True)
```

### FFmpeg in CI/CD (GitHub Actions)

```yaml
- name: Transcode videos
  run: |
    sudo apt-get install -y ffmpeg
    for f in videos/*.mov; do
      ffmpeg -i "$f" -c:v libx264 -crf 23 -c:a aac -movflags +faststart \
        "output/$(basename ${f%.mov}.mp4)"
    done
```

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

## 11. Advanced Filter Graphs

### Overlay Compositing

```bash
# PiP (Picture-in-Picture) — small on bottom-right
ffmpeg -i main.mp4 -i pip.mp4 -filter_complex \
  "[1:v]scale=320:-1[pip];[0:v][pip]overlay=W-w-10:H-h-10" output.mp4

# Side-by-side comparison
ffmpeg -i left.mp4 -i right.mp4 -filter_complex \
  "[0:v]scale=960:-1[l];[1:v]scale=960:-1[r];[l][r]hstack" output.mp4

# Top-bottom split
ffmpeg -i top.mp4 -i bottom.mp4 -filter_complex \
  "[0:v]scale=-1:540[t];[1:v]scale=-1:540[b];[t][b]vstack" output.mp4

# 2x2 grid
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 -filter_complex \
  "[0:v]scale=960:540[a];[1:v]scale=960:540[b];[2:v]scale=960:540[c];[3:v]scale=960:540[d];\
   [a][b]hstack[top];[c][d]hstack[bot];[top][bot]vstack" output.mp4

# Wipe transition (50% overlap at 2s)
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
  "[1:v]setpts=PTS-STARTPTS+2/TB[bg];\
   [0:v][bg]overlay=x='min(1,W-t*W/2)':shortest=1" output.mp4
```

### Complex Filter Chains

```bash
# Trim + Scale + Watermark + Burn-sub (pipeline)
ffmpeg -i input.mk4 -ss 30 -to 90 -filter_complex \
  "[0:v]scale=1280:-1,drawtext=text='DRAFT':fontsize=36:fontcolor=red@0.5:x=10:y=10[v];\
   [0:a]atrim=start=30:end=90,asetpts=PTS-STARTPTS[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 23 -c:a aac output.mp4

# Multi-overlay watermark grid (4 corners)
ffmpeg -i input.mp4 -i logo.png -filter_complex \
  "[1:v]scale=80:-1[lw];\
   [lw][0:v]overlay=10:10[t1];\
   [lw][t1]overlay=W-w-10:10[t2];\
   [lw][t2]overlay=10:H-h-10[t3];\
   [lw][t3]overlay=W-w-10:H-h-10" output.mp4

# Animate text (scrolling credits)
ffmpeg -i input.mp4 -filter_complex \
  "drawtext=text='CREDITS\n\n\nDirector\nProducer\nEditor':\
   fontsize=24:fontcolor=white:x=(w-tw)/2:y=h-t*50" output.mp4
```

---

## 12. Color Space & HDR

### Color Matrix Conversion

```bash
# BT.709 → BT.601 (SD)
ffmpeg -i input.mp4 -vf "colorspace=all=bt709:iall=bt601-6-625" output.mp4

# Force BT.709 (HD standard)
ffmpeg -i input.mp4 -vf "scale=in_color_matrix=bt709:out_color_matrix=bt709" output.mp4

# Set color primaries, transfer, matrix
ffmpeg -i input.mp4 -color_primaries bt709 -color_trc bt709 -colorspace bt709 output.mp4
```

### HDR → SDR Tonemapping

```bash
# Hable tonemap (most reliable)
ffmpeg -i hdr_input.mp4 -vf \
  "zscale=t=linear:npl=100,format=gbrpf32le,\
   zscale=t=bt709:tonemap=hable:desat=0,\
   zscale=p=bt709:t=bt709:m=bt709" \
  -c:v libx264 -crf 23 -c:a copy output_sdr.mp4

# Reinhard tonemap (brighter)
ffmpeg -i hdr_input.mp4 -vf \
  "zscale=t=linear:npl=80,format=gbrpf32le,\
   zscale=t=bt709:tonemap=reinhard:desat=0,\
   zscale=p=bt709:t=bt709:m=bt709" \
  -c:v libx264 -crf 23 output.mp4

# Mobius tonemap (film-like)
ffmpeg -i hdr_input.mp4 -vf \
  "zscale=t=linear:npl=100,format=gbrpf32le,\
   zscale=t=bt709:tonemap=mobius:desat=0,\
   zscale=p=bt709:t=bt709:m=bt709" \
  -c:v libx264 -crf 23 output.mp4
```

### HDR → HDR Passthrough

```bash
# Keep HDR10 metadata
ffmpeg -i hdr_input.mp4 -c:v libx265 -crf 22 \
  -tag:v hvc1 -color_primaries bt2020 \
  -color_trc smpte2084 -colorspace bt2020nc \
  output_hdr.mp4
```

### Color Grading via LUT

```bash
# Apply 3D LUT (cinematic look)
ffmpeg -i input.mp4 -vf "lut3d='cinema.cube'" -c:v libx264 -crf 23 output.mp4

# LUT + scale pipeline
ffmpeg -i input.mp4 -vf "lut3d='warm.cube',scale=1920:1080" output.mp4
```

### Gamma & Brightness

```bash
# Adjust gamma
ffmpeg -i input.mp4 -vf "eq=gamma=1.5" output.mp4

# Brightness + Contrast + Saturation
ffmpeg -i input.mp4 -vf "eq=brightness=0.06:contrast=1.2:saturation=1.3" output.mp4

# Night effect (reduce brightness, boost blue)
ffmpeg -i input.mp4 -vf "eq=brightness=-0.1:colorbalance=bs=0.3:bm=0.2" output.mp4
```

---

## 13. Audio Processing

### Normalization (EBU R128)

```bash
# Analyze loudness (two-pass)
ffmpeg -i input.mp4 -af loudnorm=print_format=json -f null -

# Apply normalization (use JSON output from above)
ffmpeg -i input.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11:\
measured_I=-20:measured_TP=-2:measured_LRA=7:measured_thresh=-30\
:linear=true output.mp4

# Simple one-pass normalization
ffmpeg -i input.mp4 -af loudnorm=I=-16:TP=-1.5 output.mp4
```

### Audio EQ & Effects

```bash
# 10-band EQ (boost bass, cut treble)
ffmpeg -i input.mp4 -af "equalizer=f=60:t=h:w=100:g=6,equalizer=f=10000:t=h:w=5000:g=-4" output.mp4

# Bass boost
ffmpeg -i input.mp4 -af "bass=g=6:f=100" output.mp4

# Treble cut
ffmpeg -i input.mp4 -af "treble=g=-6:f=8000" output.mp4

# Highpass filter (remove low rumble)
ffmpeg -i input.mp4 -af "highpass=f=80" output.mp4

# Lowpass filter (remove hiss)
ffmpeg -i input.mp4 -af "lowpass=f=12000" output.mp4

# Compressor (dynamic range)
ffmpeg -i input.mp4 -af "acompressor=threshold=-20dB:ratio=4:attack=5:release=50" output.mp4

# Noise gate
ffmpeg -i input.mp4 -af "agate=threshold=0.01:ratio=2" output.mp4

# Echo / Reverb
ffmpeg -i input.mp4 -aecho=0.8:0.88:60:0.4 output.mp4
```

### Remix & Channel Layout

```bash
# Stereo → Mono (mix)
ffmpeg -i input.mp4 -ac 1 output.mp4

# Stereo → 5.1 surround
ffmpeg -i input.mp4 -ac 6 output.mp4

# Downmix 5.1 → Stereo
ffmpeg -i input.mp4 -ac 2 -af "pan=stereo|FL=0.5*FC+0.707*FL+0.707*BL|FR=0.5*FC+0.707*FR+0.707*BR" output.mp4

# Extract single channel (left only)
ffmpeg -i input.mp4 -af "pan=mono|c0=FL" output.mp4

# Audio delay (sync fix)
ffmpeg -i input.mp4 -af "adelay=500|500" output.mp4  # delay 500ms
ffmpeg -i input.mp4 -af "adelay=-300|-300" output.mp4  # advance 300ms

# Tempo change (1.5x speed, no pitch shift)
ffmpeg -i input.mp4 -af "atempo=1.5" output.mp4

# Pitch shift (semitones)
ffmpeg -i input.mp4 -af "rubberband=pitch=1.5" output.mp4
```

### Audio Extraction & Replacement

```bash
# Extract audio only
ffmpeg -i input.mp4 -vn -c:a copy audio.aac

# Replace audio track
ffmpeg -i video.mp4 -i new_audio.aac -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 output.mp4

# Mute video (keep stream)
ffmpeg -i input.mp4 -c:v copy -an output_muted.mp4

# Add audio to silent video
ffmpeg -i silent.mp4 -i music.mp3 -c:v copy -c:a aac -shortest output.mp4

# Multiple audio tracks (MKV)
ffmpeg -i video.mp4 -i english.aac -i french.aac \
  -map 0:v -map 1:a -map 2:a \
  -c:v copy -c:a copy \
  -metadata:s:a:0 language=eng -metadata:s:a:1 language=fra \
  output.mkv
```

---

## 14. Video Stabilization

```bash
# vidstab — two-pass stabilization

# Pass 1: Analyze
ffmpeg -i input.mp4 -vf vidstabdetect=stepsize=6:shakiness=5:accuracy=15 \
  -f null -

# Pass 2: Apply (using transforms.trf from pass 1)
ffmpeg -i input.mp4 -vf "vidstabtransform=input=transforms.trf:zoom=1:smoothing=30,\
  unsharp=5:5:0.8:3:3:0.4" -c:v libx264 -crf 23 output_stabilized.mp4

# Quick one-pass (less accurate)
ffmpeg -i input.mp4 -vf "vidstabtransform=smoothing=30:optzoom=0,\
  unsharp=5:5:0.8:3:3:0.4" output.mp4
```

### Deblock & Denoise

```bash
# Deblock (remove compression artifacts)
ffmpeg -i input.mp4 -vf "deblock=filter=weak:block=4" output.mp4

# Spatial denoise
ffmpeg -i input.mp4 -vf "hqdn3d=4:3:6:4.5" output.mp4

# Temporal denoise
ffmpeg -i input.mp4 -vf "tmix=frames=8:weights='1 1 1 1 1 1 1 1'" output.mp4

# NLMeans (high quality denoise, slow)
ffmpeg -i input.mp4 -vf "nlmeans=s=3:p=7:r=3" output.mp4

# Deflicker (time-lapse)
ffmpeg -i input.mp4 -vf "deflicker=mode=pm:size=10" output.mp4
```

### Deinterlace

```bash
# Yadif (best quality)
ffmpeg -i input.mp4 -vf "yadif=0:-1:0" -c:v libx264 -crf 23 output.mp4

# Bwdif (newer, slightly faster)
ffmpeg -i input.mp4 -vf "bwdif=mode=send_frame" -c:v libx264 -crf 23 output.mp4

# Simple field doubling (fast, lower quality)
ffmpeg -i input.mp4 -vf "fieldorder=tff" output.mp4
```

---

## 15. GIF & Animated Image Creation

```bash
# High-quality GIF (two-pass with palette)
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];\
  [s0]palettegen=max_colors=256:stats_mode=diff[p];\
  [s1][p]paletteuse=dither=sierra2_4a" output.gif

# Quick GIF (single pass, lower quality)
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1" -loop 0 output.gif

# GIF from specific segment
ffmpeg -i input.mp4 -ss 5 -t 3 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];\
  [s0]palettegen[p];[s1][p]paletteuse" output.gif

# Optimized GIF (with gifsicle)
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];\
  [s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif && \
  gifsicle -O3 --lossy=80 output.gif -o output_optimized.gif

# WebP animation (better than GIF)
ffmpeg -i input.mp4 -vcodec libwebp -lossless 0 -compression_level 4 \
  -loop 0 -an -vsync 0 output.webp
```

---

## 16. Privacy & Redaction

### Face Blur

```bash
# Blur face region (manual coordinates)
ffmpeg -i input.mp4 -vf "delogo=x=100:y=50:w=200:h=200" output.mp4

# Blur with adjustable strength
ffmpeg -i input.mp4 -filter_complex \
  "[0:v]boxblur=20:20[bg];\
   [0:v]crop=200:200:100:50,boxblur=25:25[fg];\
   [bg][fg]overlay=100:50" output.mp4
```

### Region Masking

```bash
# Black out region (redaction)
ffmpeg -i input.mp4 -vf "drawbox=x=100:y=50:w=200:h=200:color=black:t=fill" output.mp4

# Pixelate region
ffmpeg -i input.mp4 -filter_complex \
  "[0:v]scale=iw/10:ih/10,scale=iw*10:ih*10:flags=neighbor[pix];\
   [0:v][pix]overlay=0:0:enable='between(t,2,8)'" output.mp4

# Redact with timestamp range
ffmpeg -i input.mp4 -vf \
  "drawbox=x=100:y=50:w=200:h=200:color=black:t=fill:enable='between(t,5,15)'" output.mp4
```

### Audio Redaction

```bash
# Silence a time range
ffmpeg -i input.mp4 -af "volume=enable='between(t,5,15)':volume=0" output.mp4

# Beep over sensitive audio
ffmpeg -i input.mp4 -f lavfi -i "sine=frequency=1000:duration=10" \
  -filter_complex "[1:a]adelay=5000|5000[beep];[0:a][beep]amix=inputs=2:duration=first" \
  -map 0:v -map "[a]" output.mp4
```

---

## 17. Time-Lapse & Slow Motion

### Time-Lapse from Image Sequence

```bash
# Image sequence → video (24fps)
ffmpeg -r 24 -i frame_%04d.jpg -c:v libx264 -crf 20 -pix_fmt yuv420p timelapse.mp4

# Image sequence → video with EXIF timestamps
ffmpeg -r 24 -pattern_type glob -i '*.jpg' -c:v libx264 -crf 20 timelapse.mp4

# Time-lapse from video (10x speed)
ffmpeg -i input.mp4 -vf "setpts=0.1*PTS" -r 24 output_timelapse.mp4

# Stabilized time-lapse (deflicker)
ffmpeg -i input.mp4 -vf "deflicker=mode=pm:size=10,setpts=0.1*PTS" output.mp4
```

### Slow Motion

```bash
# 4x slow (with frame interpolation)
ffmpeg -i input.mp4 -vf "minterpolate=fps=120:mi_mode=mci:mc_mode=aobmc:vsbmc=1" \
  -r 120 -c:v libx264 -crf 18 output_slow.mp4

# 2x slow (simple frame duplication)
ffmpeg -i input.mp4 -vf "setpts=2*PTS" -r 60 output_slow.mp4

# Variable speed (slow start, normal end)
ffmpeg -i input.mp4 -vf "setpts='if(lt(T,5),4*PTS,PTS)'" output.mp4
```

---

## 18. Video Comparison & Analysis

### Visual Comparison

```bash
# Side-by-side with labels
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
  "[0:v]scale=640:-1,drawtext=text='Original':x=10:y=10:fontsize=24:fontcolor=white[l];\
   [1:v]scale=640:-1,drawtext=text='Encoded':x=10:y=10:fontsize=24:fontcolor=white[r];\
   [l][r]hstack" output.mp4

# Difference (visual diff)
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
  "[0:v][1:v]libplacebo=compare=1:show=diff" output_diff.mp4

# PSNR map (per-pixel quality heatmap)
ffmpeg -i a.mp4 -i b.mp4 -lavfi psnr=stats_file=psnr.log -f null -

# SSIM per-frame
ffmpeg -i a.mp4 -i b.mp4 -lavfi "ssim=stats_file=ssim.log" -f null -

# VMAF (Netflix quality metric, best perceptual)
ffmpeg -i a.mp4 -i b.mp4 -lavfi \
  "libvmaf=model=version=vmaf_v0.6.1" -f null -
```

### Bitrate Distribution Analysis

```bash
# Per-frame bitrate analysis
ffmpeg -i input.mp4 -vf "signalstats" -f null - 2>&1 | grep "Parsed_signalstats"

# Scene change detection (for adaptive ABR)
ffmpeg -i input.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep "showinfo"

# GOP analysis
ffprobe -v quiet -select_streams v:0 -show_entries frame=pict_type,key_frame \
  -of csv=p=0 input.mp4 | sort | uniq -c
```

---

## 19. Video Repair & Recovery

```bash
# Fix corrupt container (re-mux)
ffmpeg -i corrupt.mp4 -c copy -movflags +faststart fixed.mp4

# Recover truncated file (estimate duration)
ffmpeg -i corrupt.mp4 -t 00:59:00 -c copy recovered.mp4

# Extract raw H.264 stream
ffmpeg -i input.mp4 -an -c:v copy stream.h264

# Fix VFR (variable frame rate) → CFR
ffmpeg -i vfr_input.mp4 -vsync cfr -r 30 -c:v libx264 -crf 23 cfr_output.mp4

# Fix audio/video sync
ffmpeg -i input.mp4 -async 1 -c:v copy output.mp4

# Repair broken MP4 moov atom
ffmpeg -i broken.mp4 -c copy -movflags +faststart repaired.mp4
```

---

## 20. Professional Workflows

### ProRes Mastering

```bash
# ProRes 422 HQ (broadcast standard)
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 -c:a pcm_s24le output.mov

# ProRes 4444 (with alpha channel)
ffmpeg -i input.mov -c:v prores_ks -profile:v 4 -pix_fmt yuva444p output_4444.mov

# ProRes from DNxHR
ffmpeg -i input.mxf -c:v prores_ks -profile:v 3 output.mov
```

### Broadcast Delivery

```bash
# SMPTE bars + tone (30s test pattern)
ffmpeg -f lavfi -i "smptebars=duration=30:size=1920x1080:rate=29.97" \
  -f lavfi -i "sine=frequency=1000:duration=30" \
  -c:v libx264 -crf 18 -c:a pcm_s16le test_pattern.mov

# EBU R128 loudness-compliant delivery
ffmpeg -i input.mp4 -af loudnorm=I=-23:TP=-2:LRA=7 \
  -c:v libx264 -crf 18 broadcast.mp4

# Closed captions (CEA-608/708)
ffmpeg -i input.mp4 -c:s mov_text -metadata:s:s:0 language=eng output.mp4
```

### Archive & Preservation

```bash
# FFV1 lossless archival (per Library of Congress recommendation)
ffmpeg -i input.mp4 -c:v ffv1 -level 3 -coder 1 -context 1 \
  -g 1 -slicecrc 1 -slices 24 -c:a flac archive.mkv

# MKV with all metadata preserved
ffmpeg -i input.mp4 -c copy -map_metadata 0 \
  -metadata title="Archive Master" \
  -metadata date="2026-01-01" archive.mkv

# Extract all streams
ffmpeg -i input.mkv -map 0 -c copy output_%02d.%s
```

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
