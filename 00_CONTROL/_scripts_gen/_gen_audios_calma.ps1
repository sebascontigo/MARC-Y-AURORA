# Genera audios de CALMA (TTS provisional en español) para la app DESPIERTA
# NOTA: voz provisional del sistema. La voz definitiva será el clon de Marc (ElevenLabs, con su consentimiento).
$ErrorActionPreference = 'Continue'
$out = 'C:\SEVISIONARI\04 Proyectos\01 Grupo Bayona\Empresa Tecnología\CLIENTES\MARC Y AURORA\MARC\APP_DESPIERTA\audios'
New-Item -ItemType Directory -Force -Path $out | Out-Null
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.Volume = 100; $s.Rate = -2
$esVoice = ($s.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture -like 'es*' } | Select-Object -First 1)
if ($esVoice) { $s.SelectVoice($esVoice.VoiceInfo.Name); "VOZ: $($esVoice.VoiceInfo.Name)" } else { "AVISO: no hay voz española instalada, se usa la por defecto" }

$textos = @{
  'calma_marc.wav'  = "Respira conmigo. Estás a salvo. Lo que sientes es un programa de tu mente, no una verdad. Inspira lentamente... sostén... y suelta el aire despacio. Muy bien. Otra vez: inspira... sostén... y suelta. Tu cuerpo vuelve al presente. Tu mente vuelve a ti. Nada fuera de este momento tiene poder ahora. Repite: yo dirijo mi mente. Yo dirijo mi mente. Cuando estés listo, vuelve despacio. Estás aquí. Estás bien."
  'fuerte_marc.wav' = "Escúchame bien. Tú no eres tu estrés. Tú no eres tu miedo. Eres la conciencia que lo observa. Este momento no te define. Responde, no reacciones. Elige tu próximo paso con la mente fría. Tú mandas. Empieza ahora."
}

foreach ($k in $textos.Keys) {
  $wav = Join-Path $out $k
  $mp3 = Join-Path $out ($k -replace '\.wav$','.mp3')
  $s.SetOutputToWaveFile($wav)
  $s.Speak($textos[$k])
  $s.SetOutputToNull()
  & ffmpeg -y -v error -i $wav -ac 1 -b:a 96k $mp3
  if (Test-Path $mp3) { "OK $mp3" } else { "ERR $mp3" }
  Remove-Item $wav -Force -ErrorAction SilentlyContinue
}
$s.Dispose()
Get-ChildItem $out | Select-Object Name, Length | Format-Table -AutoSize | Out-String