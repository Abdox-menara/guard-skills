# Video Processing — Workflows

> Split from SKILL.md to keep the main skill under ~150 lines (progressive disclosure).

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
