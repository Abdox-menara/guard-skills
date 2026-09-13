# Video Processing — Advanced Filters

> Split from SKILL.md to keep the main skill under ~150 lines (progressive disclosure).

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
