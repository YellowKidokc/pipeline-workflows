# GRAB_STORY_CHANNELS.ps1 - transcripts only (no video) for the analogy-bank channels.
# Safe to stop and re-run: the archive file skips anything already fetched.
$out = "D:\GitHub\pipeline-workflows\API\_data\youtube\subtitles"
$log = Join-Path $out "_GRAB_LOG.txt"
$channels = [ordered]@{
  "Mentour Pilot"        = "https://www.youtube.com/@MentourPilot/videos"
  "Plainly Difficult"    = "https://www.youtube.com/@PlainlyDifficult/videos"
  "Practical Engineering"= "https://www.youtube.com/@PracticalEngineeringChannel/videos"
  "Mustard"              = "https://www.youtube.com/@MustardChannel/videos"
  "LEMMiNO"              = "https://www.youtube.com/@LEMMiNO/videos"
  "Fall of Civilizations"= "https://www.youtube.com/@FallofCivilizations/videos"
  "The Moth"             = "https://www.youtube.com/@TheMoth/videos"
  "StoryCorps"           = "https://www.youtube.com/@StoryCorps/videos"
  "Veritasium"           = "https://www.youtube.com/@veritasium/videos"
  "Tom Scott"            = "https://www.youtube.com/@TomScottGo/videos"
  "Biographics"          = "https://www.youtube.com/@Biographics/videos"
  "MrBallen"             = "https://www.youtube.com/@MrBallen/videos"
}
New-Item -ItemType Directory -Force $out | Out-Null
foreach ($name in $channels.Keys) {
  $dir = Join-Path $out $name
  New-Item -ItemType Directory -Force $dir | Out-Null
  "[$(Get-Date -Format s)] START $name" | Add-Content $log
  yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "en.*,en" --convert-subs srt `
    --download-archive (Join-Path $dir "_archive.txt") --ignore-errors --no-overwrites `
    --sleep-requests 1 --sleep-interval 2 --max-sleep-interval 5 `
    -o (Join-Path $dir "%(upload_date)s %(title).120B [%(id)s].%(ext)s") $channels[$name] 2>&1 |
    Select-String -Pattern "ERROR|Writing video subtitles|already been recorded" | % { $_.Line } | Add-Content $log
  $n = (Get-ChildItem $dir -Filter *.srt -ErrorAction SilentlyContinue | Measure-Object).Count
  "[$(Get-Date -Format s)] DONE  $name  ($n transcripts)" | Add-Content $log
}
"[$(Get-Date -Format s)] ALL CHANNELS DONE" | Add-Content $log
