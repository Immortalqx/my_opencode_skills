param()

$ErrorActionPreference = "Stop"

function Try-Path {
  param([string]$P)
  if ($P -and (Test-Path -LiteralPath $P)) {
    return (Resolve-Path -LiteralPath $P).Path
  }
  return $null
}

# 1. Explicit override.
$candidate = Try-Path $env:DRAWIO_EXE
if ($candidate) { Write-Output $candidate; exit 0 }

# 2. PATH (covers scoop, choco, winget installers and PATH entries).
$names = @("draw.io.exe","drawio.exe","draw.io","drawio")
$cmd = $null
foreach ($n in $names) {
  $cmd = Get-Command $n -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($cmd) { break }
}
if ($cmd) { Write-Output $cmd.Source; exit 0 }

# 3. Common Windows install locations.
$common = @(
  "D:\drawio\draw.io\draw.io.exe"
  "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe"
  "$env:LOCALAPPDATA\Programs\draw.io\drawio.exe"
  "$env:LOCALAPPDATA\Programs\drawio\draw.io.exe"
  "$env:APPDATA\draw.io\draw.io.exe"
  "$env:ProgramFiles\draw.io\draw.io.exe"
  "$env:ProgramFiles\drawio\drawio.exe"
  "${env:ProgramFiles(x86)}\draw.io\draw.io.exe"
  "${env:ProgramFiles(x86)}\drawio\drawio.exe"
)
foreach ($p in $common) {
  if ($p) {
    $candidate = Try-Path $p
    if ($candidate) { Write-Output $candidate; exit 0 }
  }
}

# 4. Winget install paths (best-effort scan).
$wingetRoot = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages"
if ($wingetRoot -and (Test-Path -LiteralPath $wingetRoot)) {
  $hits = Get-ChildItem -LiteralPath $wingetRoot -Recurse -Filter "draw.io.exe" -ErrorAction SilentlyContinue |
    Select-Object -First 3 -ExpandProperty FullName
  foreach ($h in $hits) {
    $candidate = Try-Path $h
    if ($candidate) { Write-Output $candidate; exit 0 }
  }
}

Write-Error "drawio CLI not found. Set DRAWIO_EXE or install drawio from https://www.drawio.com/ (Windows installer). For Scoop: scoop install drawio."
exit 1
