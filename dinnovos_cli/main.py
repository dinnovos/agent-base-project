"""CLI for creating new Dinnovos agent projects."""

import os
import sys
from pathlib import Path
from cookiecutter.main import cookiecutter


def main():
    """Main entry point for the CLI."""
    # Get the path to the template directory
    # First try: parent directory (development mode)
    cli_dir = Path(__file__).parent.parent
    template_path = cli_dir / "cookiecutter-template"
    
    # Second try: installed package location
    if not template_path.exists():
        import dinnovos_cli
        package_dir = Path(dinnovos_cli.__file__).parent.parent
        template_path = package_dir / "cookiecutter-template"
    
    if not template_path.exists():
        print(f"Error: Template directory not found")
        print(f"Tried: {cli_dir / 'cookiecutter-template'}")
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
