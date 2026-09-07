# PreToolUse security guard for VS Code agent hooks.
# Reads hook JSON from stdin; blocks (deny) catastrophic commands and
# requests confirmation (ask) for risky-but-possibly-legitimate ones.
# Fast path: pattern scan only, no I/O besides stdin/stdout.
$ErrorActionPreference = 'Stop'

function Emit([string]$json) { Write-Output $json; exit 0 }

$raw = [Console]::In.ReadToEnd()
if (-not $raw) { exit 0 }

try { $evt = $raw | ConvertFrom-Json } catch { exit 0 }
if ($evt.hook_event_name -ne 'PreToolUse') { exit 0 }

$tiText = ''
if ($evt.tool_input) {
    try { $tiText = $evt.tool_input | ConvertTo-Json -Depth 6 -Compress } catch { $tiText = [string]$evt.tool_input }
}

$deny = @(
    '(rm|rmdir|rd)\s+(-[a-z]*[rf][a-z]*\s+|\s*/s\s*)+[A-Za-z]:[\\/]*\s*($|[\\"]\s*$|/|\\)', # rm -rf C:\ / rd /s C:
    'Remove-Item[^"]*-(Recurse|Force)[^"]*\s+(")?[A-Za-z]:[\\/]("\s*|\s|[^a-zA-Z0-9_-])',  # Remove-Item -Recurse C:\
    '\bformat\s+[A-Za-z]:',
    '\bdiskpart\b',
    '\bmkfs(\.\w+)?\b',
    '\bbcdedit\b',
    '\bshutdown\s+(/[sr]|-(reboot|now))',
    '\bDROP\s+(DATABASE|SCHEMA|TABLESPACE)\b',
    '\bdel\s+/[a-z]*[sf][a-z]*\s+[A-Za-z]:[\\/]*\s*($|")',
    '\bdd\s+if=[^"]*\bof=/dev/',
    '>\s*/dev/sd[a-z]\b'
)

$ask = @(
    '\bgit\s+push\s+[^"]*--force(?!\s*-with-lease)',
    '\bDROP\s+TABLE\b',
    '\bTRUNCATE\s+TABLE\b',
    '\bdel\s+/s\b',
    'Remove-Item[^"]*-Recurse[^"]*\*'
)

foreach ($p in $deny) {
    if ($tiText -match $p) {
        Emit ('{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Bloqueado por politica de seguridad del workspace (patrón destructivo). Si es legitimo, ejecutalo manualmente fuera del agente."}}')
    }
}
foreach ($p in $ask) {
    if ($tiText -match $p) {
        Emit ('{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Operacion potencialmente destructiva: requiere confirmacion del usuario."}}')
    }
}
exit 0
