# Genera REELS_FINALES 9:16 (1080x1920) con hook + CTA para los 4 testimonios
# Fuentes: versiones web 720p (mejor calidad que los clips 30s horizontales)
$ErrorActionPreference = 'Continue'
$testi = 'C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA TECNOLOGÍA\CLIENTES\MARC Y AURORA\MARC\21_TESTIMONIOS'
$out = Join-Path $testi 'REELS_FINALES'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$font = 'C\:/Windows/Fonts/arialbd.ttf'
$web = Join-Path $testi 'VERSIONES_WEB'

$reels = @(
  @{ src='GABI_TESTIMONIO_1_web.mp4';    out='REEL_1_GABI_9x16.mp4';    hook='NO ES MOTIVACIÓN. ES UN MÉTODO.';   hook2='GABI lo vivió en DESPIERTA' },
  @{ src='VICENT_TESTIMONIO_2_web.mp4';  out='REEL_2_VICENT_9x16.mp4';  hook='LO QUE DIRÍA A SU YO DE HACE UN AÑO'; hook2='VICENT · testimonio real' },
  @{ src='ELENA_TESTIMONIO_3_web.mp4';   out='REEL_3_ELENA_9x16.mp4';   hook='TU 95% SUBCONSCIENTE DECIDE POR TI';  hook2='ELENA lo desmontó en DESPIERTA' },
  @{ src='ANA_TESTIMONIO_4_web.mp4';     out='REEL_4_ANA_9x16.mp4';     hook='NUNCA FUE TU FUERZA DE VOLUNTAD';     hook2='ERA TU PROGRAMA. ANA lo cambió' }
)

$log = Join-Path $out '_GEN_LOG.txt'
"INICIO $(Get-Date -Format 'HH:mm:ss')" | Out-File $log -Encoding utf8

foreach ($r in $reels) {
  $in = Join-Path $web $r.src
  $o  = Join-Path $out $r.out
  if (-not (Test-Path $in)) { "FALTA $in" | Out-File $log -Append -Encoding utf8; continue }
  if (Test-Path $o) { "SKIP $($r.out) (ya existe)" | Out-File $log -Append -Encoding utf8; continue }
  $vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[bg];" +
        "[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2," +
        "drawtext=fontfile='$font':expansion=none:text='$($r.hook)':fontcolor=white:fontsize=58:borderw=5:bordercolor=0x000000AA:x=(w-text_w)/2:y=170:enable='between(t,0.3,5.5)'," +
        "drawtext=fontfile='$font':expansion=none:text='$($r.hook2)':fontcolor=white:fontsize=40:borderw=4:bordercolor=0x000000AA:x=(w-text_w)/2:y=280:enable='between(t,0.3,5.5)'," +
        "drawtext=fontfile='$font':expansion=none:text='Escríbeme DESPIERTA por WhatsApp':fontcolor=white:fontsize=44:borderw=4:bordercolor=0x000000AA:x=(w-text_w)/2:y=h-300:enable='between(t,24.5,30)'," +
        "drawtext=fontfile='$font':expansion=none:text='DESPIERTA · plazas septiembre':fontcolor=0xFFB347:fontsize=36:borderw=3:bordercolor=0x000000AA:x=(w-text_w)/2:y=h-170"
  "[GEN] $($r.out) $(Get-Date -Format 'HH:mm:ss')" | Out-File $log -Append -Encoding utf8
  & ffmpeg -y -v error -ss 0 -t 30 -i $in -filter_complex $vf -c:v libx264 -preset medium -crf 26 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart $o
  if ($LASTEXITCODE -eq 0) { "OK   $($r.out)" | Out-File $log -Append -Encoding utf8 } else { "ERR  $($r.out) exit=$LASTEXITCODE" | Out-File $log -Append -Encoding utf8 }
}
"FIN $(Get-Date -Format 'HH:mm:ss')" | Out-File $log -Append -Encoding utf8
Get-ChildItem $out -Filter '*.mp4' | Select-Object Name, Length | Format-Table -AutoSize | Out-String -Width 200