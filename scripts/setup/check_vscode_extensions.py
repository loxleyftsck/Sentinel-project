"""
Check currently installed VS Code extensions against recommended list
"""

import subprocess
import json
from pathlib import Path
from typing import Set, Dict, List

def get_installed_extensions() -> Set[str]:
    """Get list of currently installed VS Code extensions"""
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True,
            text=True,
            check=True
        )
        return set(result.stdout.strip().split('\n'))
    except subprocess.CalledProcessError:
        print("❌ Error: Could not get installed extensions")
        return set()
    except FileNotFoundError:
        print("❌ Error: VS Code not found in PATH")
        return set()

def get_recommended_extensions() -> List[str]:
    """Read recommended extensions from .vscode/extensions.json"""
    ext_file = Path('.vscode/extensions.json')

    if not ext_file.exists():
        print("❌ Error: .vscode/extensions.json not found")
        return []

    with open(ext_file, 'r', encoding='utf-8') as f:
        content = f.read()

        # Remove single-line comments (// ...)
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove comment part if exists
            if '//' in line:
                # Keep the part before //
                line = line.split('//')[0]
            cleaned_lines.append(line)

        cleaned_content = '\n'.join(cleaned_lines)

        data = json.loads(cleaned_content)
        return data.get('recommendations', [])

def categorize_extensions(recommended: List[str], installed: Set[str]) -> Dict[str, List[str]]:
    """Categorize extensions by installation status"""
    installed_lower = {ext.lower() for ext in installed}

    categories = {
        'installed': [],
        'missing': []
    }

    for ext in recommended:
        if ext.lower() in installed_lower:
            categories['installed'].append(ext)
        else:
            categories['missing'].append(ext)

    return categories

def main():
    print("=" * 70)
    print("🔍 VS Code Extensions Status Check")
    print("=" * 70)
    print()

    # Get extensions
    installed = get_installed_extensions()
    recommended = get_recommended_extensions()

    if not installed or not recommended:
        return

    # Categorize
    categories = categorize_extensions(recommended, installed)

    # Display results
    total = len(recommended)
    installed_count = len(categories['installed'])
    missing_count = len(categories['missing'])

    print(f"📊 Summary:")
    print(f"   Total Recommended: {total}")
    print(f"   ✅ Installed: {installed_count} ({installed_count/total*100:.1f}%)")
    print(f"   ❌ Missing: {missing_count} ({missing_count/total*100:.1f}%)")
    print()

    if categories['missing']:
        print("=" * 70)
        print("❌ Missing Extensions:")
        print("=" * 70)
        for ext in categories['missing']:
            print(f"   - {ext}")
        print()

        print("📋 Install Missing Extensions:")
        print("-" * 70)
        print("Option 1 (Auto): Run installer script")
        print("   powershell -File scripts/setup/install_vscode_extensions.ps1")
        print()
        print("Option 2 (Quick): Install critical only")
        print("   powershell -File scripts/setup/quick_install_extensions.ps1")
        print()
        print("Option 3 (Manual): Copy commands below:")
        print()
        for ext in categories['missing']:
            print(f"   code --install-extension {ext}")
        print()
    else:
        print("🎉 All recommended extensions are installed!")
        print()

    print("=" * 70)

if __name__ == "__main__":
    main()
