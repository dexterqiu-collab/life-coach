param(
    [ValidateSet("auto", "codex", "workbuddy", "codebuddy", "all")]
    [string]$Target = "auto",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$repositoryArchive = "https://github.com/dexterqiu-collab/life-coach/archive/refs/heads/main.zip"
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$repositoryRoot = Split-Path -Parent $scriptDirectory
$temporaryDirectory = $null

try {
    $sourceSkill = Join-Path $repositoryRoot "skills/career-coach"
    if (-not (Test-Path (Join-Path $sourceSkill "SKILL.md"))) {
        $temporaryDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ("career-coach-" + [guid]::NewGuid())
        New-Item -ItemType Directory -Path $temporaryDirectory | Out-Null
        $archivePath = Join-Path $temporaryDirectory "source.zip"
        Invoke-WebRequest -Uri $repositoryArchive -OutFile $archivePath
        Expand-Archive -Path $archivePath -DestinationPath $temporaryDirectory
        $repositoryRoot = Join-Path $temporaryDirectory "life-coach-main"
        $sourceSkill = Join-Path $repositoryRoot "skills/career-coach"
    }

    $targets = @()
    if ($Target -eq "auto") {
        if ($env:CODEX_HOME -or (Test-Path (Join-Path $HOME ".codex"))) { $targets += "codex" }
        if (Test-Path (Join-Path $HOME ".workbuddy")) { $targets += "workbuddy" }
        if (Test-Path (Join-Path $HOME ".codebuddy")) { $targets += "codebuddy" }
        if ($targets.Count -eq 0) {
            throw "Could not detect Codex, WorkBuddy, or CodeBuddy. Pass -Target explicitly."
        }
    } elseif ($Target -eq "all") {
        $targets = @("codex", "workbuddy", "codebuddy")
    } else {
        $targets = @($Target)
    }

    foreach ($currentTarget in $targets) {
        switch ($currentTarget) {
            "codex" {
                $codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
                $destinationRoot = Join-Path $codexRoot "skills"
            }
            "workbuddy" { $destinationRoot = Join-Path $HOME ".workbuddy/skills" }
            "codebuddy" { $destinationRoot = Join-Path $HOME ".codebuddy/skills" }
        }

        $destination = Join-Path $destinationRoot "career-coach"
        New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null

        if (Test-Path $destination) {
            if (-not $Force) {
                Write-Warning "Skipped existing installation: $destination (use -Force to update safely)"
                continue
            }
            $timestamp = Get-Date -Format "yyyyMMddHHmmss"
            $backup = "$destination.backup-$timestamp"
            Move-Item -Path $destination -Destination $backup
            Write-Output "Backed up existing installation to $backup"
        }

        Copy-Item -Path $sourceSkill -Destination $destination -Recurse
        $skillText = Get-Content -Path (Join-Path $destination "SKILL.md") -Raw
        if ($skillText -notmatch "(?m)^name: career-coach$") {
            throw "Verification failed for $destination"
        }
        foreach ($reference in @("decision-frameworks.md", "coaching-playbook.md", "templates.md")) {
            if (-not (Test-Path (Join-Path $destination "references/$reference"))) {
                throw "Missing reference after install: $reference"
            }
        }
        Write-Output "Installed and verified: $destination"
    }

    Write-Output "Start a new conversation or reload Skills, then invoke career-coach."
}
finally {
    if ($temporaryDirectory -and (Test-Path $temporaryDirectory)) {
        Remove-Item -Path $temporaryDirectory -Recurse -Force
    }
}
