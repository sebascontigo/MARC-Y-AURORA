# PostToolUse audit logger for VS Code agent hooks.
# Appends one compact line per tool invocation to agent-ops.log.
# Self-rotates when the log exceeds ~512 KB. Never blocks the agent:
# all errors are swallowed and it always exits 0.
try {
    $raw = [Console]::In.ReadToEnd()
    if ($raw) {
        $evt = $raw | ConvertFrom-Json
        if ($evt.hook_event_name -eq 'PostToolUse') {
            $ti = ''
            if ($evt.tool_input) {
                try { $ti = $evt.tool_input | ConvertTo-Json -Depth 2 -Compress } catch { $ti = [string]$evt.tool_input }
            }
            if ($ti.Length -gt 400) { $ti = $ti.Substring(0, 400) }
            $line = '{0}`t{1}`t{2}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $evt.tool_name, $ti
            $log = Join-Path $PSScriptRoot 'agent-ops.log'
            if ((Test-Path $log) -and ((Get-Item $log).Length -gt 512KB)) {
                $keep = Get-Content $log -Tail 500
                Set-Content -LiteralPath $log -Value $keep
            }
            Add-Content -LiteralPath $log -Value $line
        }
    }
} catch { }
exit 0
