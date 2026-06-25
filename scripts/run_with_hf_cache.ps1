param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Command
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
$env:HF_HOME = "C:\Models\HuggingFace"

if ($Command.Count -eq 0) {
    Write-Host "HF_HOME set for this session: $env:HF_HOME"
    Write-Host "Project folder: $ProjectRoot"
    Write-Host "Pass a command after the script name to run it with this cache."
    Write-Host "Example: .\scripts\run_with_hf_cache.ps1 python run_experiment.py --analysis-only --output-dir results/gpt2"
    exit 0
}

& $Command[0] @($Command | Select-Object -Skip 1)
