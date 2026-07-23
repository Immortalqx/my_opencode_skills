param(
  [Parameter(Mandatory=$true)][string]$DrawioPath,
  [string]$OutDir = "",
  [string]$DrawioExe = "",
  [double]$Scale = 1.5,
  [int]$TimeoutSeconds = 60,
  [switch]$EmbedPngDiagram
)

$ErrorActionPreference = "Stop"

function Resolve-DrawioExe {
  param([string]$Candidate)
  if ($Candidate -and (Test-Path -LiteralPath $Candidate)) {
    return (Resolve-Path -LiteralPath $Candidate).Path
  }
  if ($env:DRAWIO_EXE -and (Test-Path -LiteralPath $env:DRAWIO_EXE)) {
    return (Resolve-Path -LiteralPath $env:DRAWIO_EXE).Path
  }
  $names = @("draw.io.exe","drawio.exe","draw.io","drawio")
  $cmd = $null
  foreach ($n in $names) {
    $cmd = Get-Command $n -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($cmd) { break }
  }
  if ($cmd) { return $cmd.Source }
  $common = @(
    "D:\drawio\draw.io\draw.io.exe",
    "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe",
    "$env:LOCALAPPDATA\Programs\draw.io\drawio.exe",
    "$env:LOCALAPPDATA\Programs\drawio\draw.io.exe",
    "$env:APPDATA\draw.io\draw.io.exe",
    "$env:ProgramFiles\draw.io\draw.io.exe",
    "$env:ProgramFiles\drawio\drawio.exe",
    "${env:ProgramFiles(x86)}\draw.io\draw.io.exe",
    "${env:ProgramFiles(x86)}\drawio\drawio.exe"
  )
  foreach ($p in $common) {
    if ($p -and (Test-Path -LiteralPath $p)) { return (Resolve-Path -LiteralPath $p).Path }
  }
  throw "drawio executable not found. Set DRAWIO_EXE or pass -DrawioExe. Download: https://www.drawio.com/"
}

$drawio = Resolve-DrawioExe -Candidate $DrawioExe
$input = (Resolve-Path -LiteralPath $DrawioPath).Path
if (-not $OutDir) {
  $OutDir = Split-Path -Parent $input
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$base = [System.IO.Path]::GetFileNameWithoutExtension($input)
$png = Join-Path $OutDir "$base.png"

Write-Host "drawio : $drawio"
Write-Host "input  : $input"
Write-Host "output : $png"
Write-Host "scale  : $Scale"
Write-Host "timeout: ${TimeoutSeconds}s"

if ($EmbedPngDiagram) {
  $args = @("--export","--format","png","--embed-diagram","--output",$png,"--scale",$Scale,$input)
} else {
  $args = @("--export","--format","png","--output",$png,"--scale",$Scale,$input)
}

$proc = Start-Process -FilePath $drawio -ArgumentList $args -PassThru -NoNewWindow
if (-not $proc.WaitForExit($TimeoutSeconds * 1000)) {
  try { Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue } catch {}
  Start-Sleep -Seconds 1
  if (Test-Path -LiteralPath $png) {
    Remove-Item -LiteralPath $png -Force -ErrorAction SilentlyContinue
  }
  Write-Host "Error: drawio PNG export timed out after ${TimeoutSeconds}s. Aborted." -ForegroundColor Red
  exit 5
}

# Primary success signal: a non-empty PNG at the expected path.
if (-not (Test-Path -LiteralPath $png)) {
  $rc = $proc.ExitCode
  Write-Host "Error: PNG was not produced at $png (drawio exit code: $rc)"
  exit 1
}
$pngInfo = Get-Item -LiteralPath $png
if ($pngInfo.Length -le 0) {
  Remove-Item -LiteralPath $png -Force -ErrorAction SilentlyContinue
  Write-Host "Error: PNG at $png is empty."
  exit 1
}

# drawio's exit code is unreliable across versions / wrappers; treat non-zero as a
# warning only when the file looks sane. Clear non-zero + bad file = hard failure.
$rc = [int]$proc.ExitCode
if ($rc -ne 0 -and $rc -ne $null) {
  Write-Host "Warning: drawio exited with code $rc, but a non-empty PNG is present." -ForegroundColor Yellow
}

Get-Item -LiteralPath $png | Select-Object FullName, Length, LastWriteTime | Format-Table -AutoSize | Out-String | Write-Host
