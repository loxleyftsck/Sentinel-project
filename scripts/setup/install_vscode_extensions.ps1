# SENTINEL Project - VS Code Extensions Auto-Installer
# Run this script to install all recommended extensions

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  VS Code Extensions Auto-Installer  " -ForegroundColor Cyan
Write-Host "  SENTINEL Project Setup              " -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if VS Code is installed
try {
    $vscodeVersion = code --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "VS Code not found"
    }
    Write-Host "✅ VS Code detected" -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host "❌ VS Code is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Please install VS Code from: https://code.visualstudio.com/" -ForegroundColor Yellow
    exit 1
}

# List of extensions to install
$extensions = @(
    # Python Development (Required)
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.pylint",

    # Jupyter & Data Science (Required)
    "ms-toolsai.jupyter",
    "ms-toolsai.jupyter-keymap",
    "ms-toolsai.jupyter-renderers",
    "mechatroner.rainbow-csv",
    "randomfractalsinc.vscode-data-preview",

    # Docker & DevOps (Recommended)
    "ms-azuretools.vscode-docker",
    "ms-vscode-remote.remote-containers",

    # Git & Version Control (Recommended)
    "eamodio.gitlens",
    "mhutchie.git-graph",

    # Configuration Files (Recommended)
    "redhat.vscode-yaml",
    "tamasfe.even-better-toml",

    # Markdown (Recommended)
    "yzhang.markdown-all-in-one",
    "davidanson.vscode-markdownlint",

    # Code Quality (Recommended)
    "sonarsource.sonarlint-vscode",
    "streetsidesoftware.code-spell-checker",

    # Productivity (Optional)
    "gruntfuggly.todo-tree",
    "wayou.vscode-todo-highlight",
    "aaron-bond.better-comments",

    # Testing (Optional)
    "littlefoxteam.vscode-python-test-adapter",

    # AI & LLM (Optional)
    "continue.continue",

    # API Development (Optional)
    "humao.rest-client",
    "mikestead.dotenv"
)

$installed = 0
$skipped = 0
$failed = 0
$total = $extensions.Count

Write-Host "📦 Installing $total extensions..." -ForegroundColor Cyan
Write-Host ""

foreach ($extension in $extensions) {
    $progress = [math]::Round((($installed + $skipped + $failed) / $total) * 100)
    Write-Host "[$progress%] Installing: $extension" -ForegroundColor Gray

    try {
        # Check if already installed
        $check = code --list-extensions | Select-String -Pattern "^$extension$" -Quiet

        if ($check) {
            Write-Host "  ⏭️  Already installed" -ForegroundColor Yellow
            $skipped++
        }
        else {
            # Install extension
            $output = code --install-extension $extension --force 2>&1

            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✅ Installed successfully" -ForegroundColor Green
                $installed++
            }
            else {
                Write-Host "  ❌ Installation failed" -ForegroundColor Red
                $failed++
            }
        }
    }
    catch {
        Write-Host "  ❌ Error: $_" -ForegroundColor Red
        $failed++
    }

    Write-Host ""
}

# Summary
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  📊 Installation Summary             " -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Total Extensions: $total" -ForegroundColor White
Write-Host "✅ Newly Installed: $installed" -ForegroundColor Green
Write-Host "⏭️  Already Installed: $skipped" -ForegroundColor Yellow
Write-Host "❌ Failed: $failed" -ForegroundColor Red
Write-Host ""

if ($failed -eq 0) {
    Write-Host "🎉 All extensions installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
    Write-Host "   1. Reload VS Code window (Ctrl+Shift+P > Reload Window)" -ForegroundColor White
    Write-Host "   2. Select Python interpreter: ./venv/Scripts/python.exe" -ForegroundColor White
    Write-Host "   3. Start coding!" -ForegroundColor White
}
else {
    Write-Host "⚠️  Some extensions failed to install" -ForegroundColor Yellow
    Write-Host "   Please install them manually from VS Code Extensions panel" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
