<#
.SYNOPSIS
    Automated Video Analysis Tool
.DESCRIPTION
    Analyzes video files and generates comprehensive reports
    Uses ffmpeg/ffprobe for extraction and analysis
.PARAMETER VideoPath
    Path to the video file to analyze
.PARAMETER OutputDir
    Output directory for analysis results (default: same as video)
.PARAMETER ExtractFrames
    Extract keyframes for visual analysis
.PARAMETER ExtractAudio
    Extract audio for transcription
.PARAMETER GenerateThumbnails
    Generate thumbnail previews
.PARAMETER Detailed
    Generate detailed analysis report
.EXAMPLE
    .\Analyze-Video.ps1 -VideoPath "C:\video.mp4" -ExtractFrames -ExtractAudio
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$VideoPath,
    
    [string]$OutputDir,
    
    [switch]$ExtractFrames,
    [switch]$ExtractAudio,
    [switch]$GenerateThumbnails,
    [switch]$Detailed,
    [switch]$All
)

# Set defaults
if ($All) {
    $ExtractFrames = $true
    $ExtractAudio = $true
    $GenerateThumbnails = $true
    $Detailed = $true
}

if (-not $OutputDir) {
    $OutputDir = Join-Path (Split-Path $VideoPath) "analysis_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
}

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

Write-Host "=== Video Analysis Tool ===" -ForegroundColor Cyan
Write-Host "Video: $VideoPath"
Write-Host "Output: $OutputDir"
Write-Host ""

# Check if video exists
if (-not (Test-Path $VideoPath)) {
    Write-Error "Video file not found: $VideoPath"
    exit 1
}

# Get video metadata
Write-Host "1. Extracting metadata..." -ForegroundColor Yellow
$metadata = ffprobe -v quiet -print_format json -show_format -show_streams $VideoPath | ConvertFrom-Json

# Save raw metadata
$metadata | ConvertTo-Json -Depth 10 | Out-File "$OutputDir\metadata.json"

# Parse metadata
$videoStream = $metadata.streams | Where-Object { $_.codec_type -eq "video" } | Select-Object -First 1
$audioStream = $metadata.streams | Where-Object { $_.codec_type -eq "audio" } | Select-Object -First 1
$format = $metadata.format

# Create summary
$summary = [PSCustomObject]@{
    FileName = Split-Path $VideoPath -Leaf
    FilePath = $VideoPath
    AnalysisDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Duration = [math]::Round([double]$format.duration, 2)
    DurationFormatted = [math]::Floor([double]$format.duration / 60).ToString() + ":" + ([math]::Round([double]$format.duration % 60)).ToString().PadLeft(2, '0')
    FileSizeMB = [math]::Round([long]$format.size / 1MB, 2)
    TotalBitrate = [math]::Round([long]$format.bit_rate / 1000, 0)
    VideoCodec = $videoStream.codec_name
    VideoProfile = $videoStream.profile
    VideoResolution = "$($videoStream.width)x$($videoStream.height)"
    VideoFPS = $videoStream.r_frame_rate
    VideoBitrate = if ($videoStream.bit_rate) { [math]::Round([long]$videoStream.bit_rate / 1000, 0) } else { "N/A" }
    AudioCodec = $audioStream.codec_name
    AudioSampleRate = $audioStream.sample_rate
    AudioChannels = $audioStream.channels
    AudioBitrate = if ($audioStream.bit_rate) { [math]::Round([long]$audioStream.bit_rate / 1000, 0) } else { "N/A" }
    CreationTime = $format.tags.creation_time
}

# Save summary
$summary | ConvertTo-Json | Out-File "$OutputDir\summary.json"

# Display summary
Write-Host "`n=== Video Summary ===" -ForegroundColor Green
Write-Host "File: $($summary.FileName)"
Write-Host "Duration: $($summary.DurationFormatted) ($($summary.Duration)s)"
Write-Host "Size: $($summary.FileSizeMB) MB"
Write-Host "Video: $($summary.VideoCodec) ($($summary.VideoProfile)) @ $($summary.VideoResolution)"
Write-Host "FPS: $($summary.VideoFPS)"
Write-Host "Audio: $($summary.AudioCodec) $($summary.AudioChannels)ch @ $($summary.AudioSampleRate)Hz"
Write-Host "Bitrate: $($summary.TotalBitrate) kbps total"

# Extract keyframes
if ($ExtractFrames) {
    Write-Host "`n2. Extracting keyframes..." -ForegroundColor Yellow
    $framesDir = Join-Path $OutputDir "keyframes"
    New-Item -ItemType Directory -Path $framesDir -Force | Out-Null
    
    # Extract 1 frame per second
    ffmpeg -v quiet -i $VideoPath -vf "fps=1" -q:v 2 "$framesDir\frame_%04d.jpg" 2>&1 | Out-Null
    
    $frameCount = (Get-ChildItem "$framesDir\*.jpg").Count
    Write-Host "   Extracted $frameCount keyframes to $framesDir"
}

# Extract audio
if ($ExtractAudio) {
    Write-Host "`n3. Extracting audio..." -ForegroundColor Yellow
    $audioPath = Join-Path $OutputDir "audio.wav"
    
    ffmpeg -v quiet -i $VideoPath -vn -acodec pcm_s16le -ar 16000 -ac 1 $audioPath 2>&1 | Out-Null
    
    if (Test-Path $audioPath) {
        $audioSize = [math]::Round((Get-Item $audioPath).Length / 1KB, 2)
        Write-Host "   Audio extracted: $audioPath ($audioSize KB)"
    }
}

# Generate thumbnails
if ($GenerateThumbnails) {
    Write-Host "`n4. Generating thumbnails..." -ForegroundColor Yellow
    $thumbsDir = Join-Path $OutputDir "thumbnails"
    New-Item -ItemType Directory -Path $thumbsDir -Force | Out-Null
    
    # Generate thumbnails at specific intervals
    $duration = [double]$format.duration
    $intervals = @(0, 0.25, 0.5, 0.75, 1.0)
    
    foreach ($pct in $intervals) {
        $time = $duration * $pct
        $thumbPath = Join-Path $thumbsDir "thumb_$([math]::Round($pct * 100))pct.jpg"
        ffmpeg -v quiet -i $VideoPath -ss $time -vframes 1 -q:v 2 $thumbPath 2>&1 | Out-Null
    }
    
    $thumbCount = (Get-ChildItem "$thumbsDir\*.jpg").Count
    Write-Host "   Generated $thumbCount thumbnails"
}

# Detailed analysis
if ($Detailed) {
    Write-Host "`n5. Performing detailed analysis..." -ForegroundColor Yellow
    
    # Analyze video quality metrics
    $analysis = [PSCustomObject]@{
        QualityScore = 0
        Issues = @()
        Recommendations = @()
    }
    
    # Check resolution
    if ($videoStream.width -ge 1920) {
        $analysis.QualityScore += 25
    } elseif ($videoStream.width -ge 1280) {
        $analysis.QualityScore += 15
    } else {
        $analysis.Issues += "Low resolution: $($summary.VideoResolution)"
        $analysis.Recommendations += "Consider recording at 1080p or higher"
    }
    
    # Check FPS
    $fps = [double]$videoStream.r_frame_rate.Split('/')[0] / [double]$videoStream.r_frame_rate.Split('/')[1]
    if ($fps -ge 30) {
        $analysis.QualityScore += 25
    } elseif ($fps -ge 24) {
        $analysis.QualityScore += 15
    } else {
        $analysis.Issues += "Low frame rate: $fps FPS"
        $analysis.Recommendations += "Consider recording at 30 FPS or higher"
    }
    
    # Check bitrate
    $videoBitrate = if ($videoStream.bit_rate) { [long]$videoStream.bit_rate } else { 0 }
    if ($videoBitrate -gt 5000000) {
        $analysis.QualityScore += 25
    } elseif ($videoBitrate -gt 2000000) {
        $analysis.QualityScore += 15
    } else {
        $analysis.Issues += "Low video bitrate: $([math]::Round($videoBitrate/1000)) kbps"
        $analysis.Recommendations += "Increase bitrate for better quality"
    }
    
    # Check audio
    if ($audioStream) {
        $analysis.QualityScore += 25
    } else {
        $analysis.Issues += "No audio track found"
        $analysis.Recommendations += "Add audio track if needed"
    }
    
    # Save detailed analysis
    $analysis | ConvertTo-Json -Depth 5 | Out-File "$OutputDir\detailed_analysis.json"
    
    Write-Host "   Quality Score: $($analysis.QualityScore)/100"
    if ($analysis.Issues.Count -gt 0) {
        Write-Host "   Issues:" -ForegroundColor Red
        $analysis.Issues | ForEach-Object { Write-Host "     - $_" }
    }
    if ($analysis.Recommendations.Count -gt 0) {
        Write-Host "   Recommendations:" -ForegroundColor Yellow
        $analysis.Recommendations | ForEach-Object { Write-Host "     - $_" }
    }
}

# Generate HTML report
Write-Host "`n6. Generating report..." -ForegroundColor Yellow
$htmlReport = @"
<!DOCTYPE html>
<html>
<head>
    <title>Video Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; }
        .metric { margin: 10px 0; }
        .label { font-weight: bold; }
        .good { color: green; }
        .warning { color: orange; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Video Analysis Report</h1>
    <p>Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")</p>
    
    <div class="summary">
        <h2>Summary</h2>
        <div class="metric"><span class="label">File:</span> $($summary.FileName)</div>
        <div class="metric"><span class="label">Duration:</span> $($summary.DurationFormatted)</div>
        <div class="metric"><span class="label">Size:</span> $($summary.FileSizeMB) MB</div>
        <div class="metric"><span class="label">Video:</span> $($summary.VideoCodec) @ $($summary.VideoResolution)</div>
        <div class="metric"><span class="label">FPS:</span> $($summary.VideoFPS)</div>
        <div class="metric"><span class="label">Audio:</span> $($summary.AudioCodec) $($summary.AudioChannels)ch</div>
        <div class="metric"><span class="label">Bitrate:</span> $($summary.TotalBitrate) kbps</div>
    </div>
    
    <h2>Files Generated</h2>
    <ul>
        <li>metadata.json - Raw metadata</li>
        <li>summary.json - Parsed summary</li>
        $(if ($ExtractFrames) { "<li>keyframes/ - Extracted frames</li>" })
        $(if ($ExtractAudio) { "<li>audio.wav - Extracted audio</li>" })
        $(if ($GenerateThumbnails) { "<li>thumbnails/ - Preview thumbnails</li>" })
        $(if ($Detailed) { "<li>detailed_analysis.json - Quality analysis</li>" })
    </ul>
</body>
</html>
"@

$htmlReport | Out-File "$OutputDir\report.html"

Write-Host "`n=== Analysis Complete ===" -ForegroundColor Cyan
Write-Host "Results saved to: $OutputDir"
Write-Host "Open report.html in a browser to view the full report"