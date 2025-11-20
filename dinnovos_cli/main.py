"""CLI for creating new Dinnovos agent projects."""

import os
import sys
from pathlib import Path
from cookiecutter.main import cookiecutter


def main():
    """Main entry point for the CLI."""
    # Get the path to the template directory
    # The template is now bundled inside the dinnovos_cli package
    import dinnovos_cli
    
    # Primary location: inside the installed package
    package_dir = Path(dinnovos_cli.__file__).parent
    template_path = package_dir / "cookiecutter-template"
    
    # Fallback: development mode (parent directory)
    if not template_path.exists():
        cli_dir = Path(__file__).parent.parent
        template_path = cli_dir / "cookiecutter-template"
    
    if not template_path.exists():
        print(f"Error: Template directory not found")
        print(f"Expected location: {package_dir / 'cookiecutter-template'}")
        print(f"Fallback location: {cli_dir / 'cookiecutter-template'}")
        print(f"\nPackage directory: {package_dir}")
        print(f"Package contents:")
        if package_dir.exists():
            for item in package_dir.iterdir():
                print(f"  - {item.name}")
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
