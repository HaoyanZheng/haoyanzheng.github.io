param(
  [string]$CsvPath = "assets/tcfEO/tache2.csv",
  [string]$OutDir  = "assets/tcfEO/",
  [string]$VoiceLike = "Microsoft",   # partial match; adjust to pick a specific voice
  [int]$Rate = 0,                     # -10..10 (0 is normal)
  [int]$Volume = 100,                 # 0..100
  [int]$Mp3Kbps = 96,                 # 64/96/128 etc.
  [switch]$KeepWav                    # keep intermediate wav files if set
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Ensure output dirs
$wavDir = Join-Path $OutDir "wav"
$mp3Dir = Join-Path $OutDir "mp3"
New-Item -ItemType Directory -Force -Path $wavDir | Out-Null
New-Item -ItemType Directory -Force -Path $mp3Dir | Out-Null

# Check dependencies
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  throw "ffmpeg not found in PATH. Install FFmpeg and ensure 'ffmpeg' works in PowerShell."
}

Add-Type -AssemblyName System.Speech

# Pick voice
$voices = (New-Object System.Speech.Synthesis.SpeechSynthesizer).GetInstalledVoices() |
  ForEach-Object { $_.VoiceInfo }

$voice = $voices | Where-Object { $_.Name -like "*$VoiceLike*" } | Select-Object -First 1
if (-not $voice) {
  Write-Host "Installed voices:" -ForegroundColor Yellow
  $voices | Select-Object Name, Culture | Format-Table | Out-String | Write-Host
  throw "No voice found matching '$VoiceLike'. Re-run with -VoiceLike to match one of the installed voice names."
}
Write-Host ("Using voice: {0} ({1})" -f $voice.Name, $voice.Culture)

# Read CSV (Import-Csv generally handles UTF-8 w/ BOM well; for no-BOM UTF-8, it's still ok in PS7+)
$rows = Import-Csv -Path $CsvPath

# Helpers
function Normalize-Id([string]$s) {
  if ([string]::IsNullOrWhiteSpace($s)) { return $null }
  # keep letters/numbers/_/-
  $id = ($s -replace '[^\w\-]+','').Trim('_','-')
  if ([string]::IsNullOrWhiteSpace($id)) { return $null }
  return $id.ToLower()
}

function Pad-Idx([string]$idx) {
  # allows 1, 01, 001 -> output without leading zeros by default? You asked t1a1 style,
  # but if you prefer fixed width, change "{0}" to "{0:D2}" or "{0:D3}"
  if ([string]::IsNullOrWhiteSpace($idx)) { return $null }
  $n = 0
  if ([int]::TryParse($idx, [ref]$n)) { return "$n" }
  return ($idx.Trim())
}

function Build-AutoId($r) {
  # Expected columns: tache (1/2/3), kind (q/a), idx (1..n)
  $tache = $r.tache
  $kind  = $r.kind
  $idx   = $r.idx

  if ([string]::IsNullOrWhiteSpace($tache) -or [string]::IsNullOrWhiteSpace($kind) -or [string]::IsNullOrWhiteSpace($idx)) {
    return $null
  }

  $t = 0
  if (-not [int]::TryParse([string]$tache, [ref]$t)) { return $null }
  if ($t -lt 1 -or $t -gt 9) { return $null }

  $k = ([string]$kind).Trim().ToLower()
  if ($k -ne "q" -and $k -ne "a") { return $null }

  $i = Pad-Idx([string]$idx)
  if ([string]::IsNullOrWhiteSpace($i)) { return $null }

  return ("t{0}{1}{2}" -f $t, $k, $i)
}

# Synthesize
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice($voice.Name)
$synth.Rate = $Rate
$synth.Volume = $Volume

$seen = @{}

foreach ($r in $rows) {
  # Determine text
  $text = $null
  if ($r.PSObject.Properties.Name -contains "text") { $text = [string]$r.text }
  if ([string]::IsNullOrWhiteSpace($text)) { continue }

  # Determine ID: prefer explicit r.id; else auto from tache/kind/idx
  $id = $null
  if ($r.PSObject.Properties.Name -contains "id") { $id = Normalize-Id([string]$r.id) }
  if (-not $id) {
    $auto = Build-AutoId $r
    $id = Normalize-Id $auto
  }
  if (-not $id) {
    Write-Host "Skipping row (no id and cannot auto-build): $($text.Substring(0, [Math]::Min(40, $text.Length)))" -ForegroundColor Yellow
    continue
  }

  # Ensure uniqueness
  if ($seen.ContainsKey($id)) {
    $seen[$id] += 1
    $id = "{0}_{1}" -f $id, $seen[$id]
  } else {
    $seen[$id] = 0
  }

  $wavPath = Join-Path $wavDir ("{0}.wav" -f $id)
  $mp3Path = Join-Path $mp3Dir ("{0}.mp3" -f $id)

  Write-Host "Generating $id..."

  # WAV
  $synth.SetOutputToWaveFile($wavPath)
  $synth.Speak($text)
  $synth.SetOutputToNull()

  # MP3 (mono, 44.1k, constant bitrate)
  & ffmpeg -y -hide_banner -loglevel error `
    -i $wavPath -ac 1 -ar 44100 -b:a ("{0}k" -f $Mp3Kbps) $mp3Path

  if (-not $KeepWav) {
    Remove-Item $wavPath -Force -ErrorAction SilentlyContinue
  }
}

Write-Host "Done. MP3s in: $mp3Dir" -ForegroundColor Green
