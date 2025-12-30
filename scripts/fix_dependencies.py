"""
Fix protobuf dependency conflicts
Run this to fix the environment
"""
import subprocess
import sys

def fix_dependencies():
    """Fix protobuf and related dependencies"""
    print("=" * 60)
    print("🔧 Fixing Dependency Conflicts")
    print("=" * 60)

    fixes = [
        # Uninstall conflicting versions
        ("Uninstalling old protobuf", ["pip", "uninstall", "-y", "protobuf"]),

        # Install specific compatible version
        ("Installing protobuf 3.20.3", ["pip", "install", "protobuf==3.20.3"]),

        # Reinstall chromadb with correct deps
        ("Reinstalling chromadb", ["pip", "install", "--upgrade", "--force-reinstall", "chromadb"]),

        # Verify installation
        ("Verifying installation", ["pip", "show", "protobuf"]),
    ]

    for description, command in fixes:
        print(f"\n📦 {description}...")
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ {description} - SUCCESS")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ {description} - Warning: {e}")
            continue

    print("\n" + "=" * 60)
    print("✅ Dependency fixes complete!")
    print("=" * 60)
    print("\nTry running the server again:")
    print("  python -m sentinel.api.main")

if __name__ == "__main__":
    fix_dependencies()
