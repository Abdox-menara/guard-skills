# Video Processing — Analysis

> Split from SKILL.md to keep the main skill under ~150 lines (progressive disclosure).

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
