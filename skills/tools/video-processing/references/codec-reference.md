# Video Processing — Codec Reference

> Split from SKILL.md to keep the main skill under ~150 lines (progressive disclosure).

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
