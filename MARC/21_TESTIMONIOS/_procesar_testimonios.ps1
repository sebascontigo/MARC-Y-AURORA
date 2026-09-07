# Procesado de testimonios Despierta - versiones web + clips reel
# Genera MP4 comprimidos (720p) y clips 30s por testimonio
$ErrorActionPreference = 'Continue'
$testiDir = 'C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA TECNOLOGÍA\CLIENTES\MARC Y AURORA\MARC\21_TESTIMONIOS'
$outWeb = Join-Path $testiDir 'VERSIONES_WEB'
$outReels = Join-Path $testiDir 'CLIPS_REELS'
New-Item -ItemType Directory -Force -Path $outWeb | Out-Null
New-Item -ItemType Directory -Force -Path $outReels | Out-Null
$log = Join-Path $testiDir '_PROCESADO_LOG.txt'
"INICIO $(Get-Date -Format 'HH:mm:ss')" | Out-File $log

Get-ChildItem (Join-Path $testiDir 'VIDEOS') -Filter '*.mp4' | ForEach-Object {
  $v = $_.FullName
  $baseName = $_.BaseName.Trim() -replace '\s+','_'
  $web = Join-Path $outWeb ($baseName + '_web.mp4')
  if (-not (Test-Path $web)) {
    "[+] Web $baseName $(Get-Date -Format 'HH:mm:ss')" | Out-File $log -Append
    & ffmpeg -y -v error -i $v -vf "scale=720:-2" -c:v libx264 -preset medium -crf 27 -c:a aac -b:a 96k -movflags +faststart $web
    "[-] Web done $baseName $(Get-Date -Format 'HH:mm:ss')" | Out-File $log -Append
  }
  $reel = Join-Path $outReels ($baseName + '_reel30s.mp4')
  if (-not (Test-Path $reel)) {
    "[+] Reel $baseName $(Get-Date -Format 'HH:mm:ss')" | Out-File $log -Append
    & ffmpeg -y -v error -ss 5 -t 30 -i $v -vf "scale=720:-2" -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 128k -movflags +faststart $reel
    "[-] Reel done $baseName $(Get-Date -Format 'HH:mm:ss')" | Out-File $log -Append
  }
}
"FIN $(Get-Date -Format 'HH:mm:ss')" | Out-File $log -Append