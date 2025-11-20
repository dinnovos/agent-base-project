"""CLI for creating new Dinnovos agent projects."""

import os
import sys
from pathlib import Path
from cookiecutter.main import cookiecutter


def main():
    """Main entry point for the CLI."""
    # Get the path to the template directory
    # Multiple search paths for different installation scenarios
    search_paths = []
    
    # 1. Development mode: parent directory
    cli_dir = Path(__file__).parent.parent
    search_paths.append(cli_dir / "cookiecutter-template")
    
    # 2. Installed in site-packages
    import dinnovos_cli
    package_dir = Path(dinnovos_cli.__file__).parent.parent
    search_paths.append(package_dir / "cookiecutter-template")
    
    # 3. Check if template files are in the package itself
    search_paths.append(package_dir / "dinnovos_cli" / "cookiecutter-template")
    
    # 4. Check in parent of package_dir (for global installs)
    search_paths.append(package_dir.parent / "cookiecutter-template")
    
    template_path = None
    for path in search_paths:
        if path.exists():
            template_path = path
            break
    
    if not template_path:
        print(f"Error: Template directory not found")
        print(f"Searched in:")
        for path in search_paths:
            print(f"  - {path}")
        sys.exit(1)
    
    try:
        # Run cookiecutter with the template
        output_dir = cookiecutter(
            str(template_path),
            no_input=False,  # Allow user interaction
        )
        
        print("\n" + "="*60)
        print("✓ Project created successfully!")
        print(f"✓ Location: {output_dir}")
        print("="*60)
        print("\nNext steps:")
        print(f"  1. cd {Path(output_dir).name}")
        print("  2. python -m venv venv")
        print("  3. venv\\Scripts\\activate  # On Windows")
        print("  4. pip install -r requirements.txt")
        print("  5. python run.py")
        print("\nFor more information, see the README.md file in your project.")
        
    except Exception as e:
        print(f"Error: Failed to create project: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
