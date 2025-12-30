# Quick VS Code Extension Installer
# Minimal version - just installs critical Python extensions

Write-Host "🚀 Installing Critical VS Code Extensions..." -ForegroundColor Cyan
Write-Host ""

$critical = @(
    "ms-python.python",           # Python
    "ms-python.vscode-pylance",   # IntelliSense
    "ms-python.black-formatter",  # Formatter
    "ms-toolsai.jupyter",         # Jupyter
    "ms-azuretools.vscode-docker", # Docker
    "eamodio.gitlens"             # Git
)

foreach ($ext in $critical) {
    Write-Host "Installing: $ext" -ForegroundColor Gray
    code --install-extension $ext --force
}

Write-Host ""
Write-Host "✅ Critical extensions installed!" -ForegroundColor Green
Write-Host "   Reload VS Code to activate." -ForegroundColor Yellow
