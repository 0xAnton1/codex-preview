[CmdletBinding()]
param(
    [ValidateSet('codex', 'claude', 'both')]
    [string]$Target = 'codex',
    [string]$ProjectDir = (Get-Location).Path,
    [string]$CodexDir = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }),
    [string]$RawBase = 'https://raw.githubusercontent.com/0xAnton1/codex-preview/main'
)

$ErrorActionPreference = 'Stop'

function Get-PreviewFile {
    param([string]$RelativePath, [string]$Destination)
    $parent = Split-Path -Parent $Destination
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    Invoke-WebRequest -UseBasicParsing -Uri "$RawBase/$RelativePath" -OutFile $Destination
}

function Install-CodexPreview {
    $destination = Join-Path $CodexDir 'skills\codex-preview'
    Get-PreviewFile 'SKILL.md' (Join-Path $destination 'SKILL.md')
    Get-PreviewFile 'agents/openai.yaml' (Join-Path $destination 'agents\openai.yaml')
    Get-PreviewFile 'references/patterns.md' (Join-Path $destination 'references\patterns.md')
    Get-PreviewFile 'references/renderer.md' (Join-Path $destination 'references\renderer.md')
    Get-PreviewFile 'scripts/demo.py' (Join-Path $destination 'scripts\demo.py')
    Get-PreviewFile 'scripts/preview.py' (Join-Path $destination 'scripts\preview.py')
    Write-Host "Installed Codex skill to $destination"
}

function Install-ClaudePreview {
    $commandPath = Join-Path $ProjectDir '.claude\commands\codex-preview.md'
    Get-PreviewFile '.claude/commands/codex-preview.md' $commandPath

    $claudePath = Join-Path $ProjectDir 'CLAUDE.md'
    if (Test-Path -LiteralPath $claudePath) {
        $referencePath = Join-Path $ProjectDir '.claude\codex-preview-reference.md'
        Get-PreviewFile 'CLAUDE.md' $referencePath
        Write-Host "Existing $claudePath preserved. Reference saved to $referencePath"
    } else {
        Get-PreviewFile 'CLAUDE.md' $claudePath
    }
    Write-Host "Installed Claude command to $commandPath"
}

switch ($Target) {
    'codex' { Install-CodexPreview }
    'claude' { Install-ClaudePreview }
    'both' {
        Install-CodexPreview
        Install-ClaudePreview
    }
}
