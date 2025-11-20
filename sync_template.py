"""
Sync script to copy changes from the main project to the template.

This script copies key directories and files from the main project
to the cookiecutter template, preserving the template structure.

Usage:
    python sync_template.py
"""

import shutil
import os
from pathlib import Path


def sync_template():
    """Sync changes from main project to template."""
    
    # Define the base paths
    project_root = Path(__file__).parent
    template_base = project_root / "cookiecutter-template" / "{{cookiecutter.project_slug}}"
    
    # Folders to sync
    folders_to_sync = [
        ("src", template_base / "src"),
        ("agents", template_base / "agents"),
        ("tests", template_base / "tests"),
        ("alembic", template_base / "alembic"),
    ]
    
    # Files to sync (source, destination)
    files_to_sync = [
        ("requirements.txt", template_base / "requirements.txt"),
        (".env.example", template_base / ".env.example"),
        ("pytest.ini", template_base / "pytest.ini"),
        ("langgraph.json", template_base / "langgraph.json"),
        ("Dockerfile", template_base / "Dockerfile"),
        ("docker-compose.yml", template_base / "docker-compose.yml"),
        (".dockerignore", template_base / ".dockerignore"),
        ("alembic.ini", template_base / "alembic.ini"),
    ]
    
    print("Starting template sync...")
    print("=" * 60)
    
    # Sync folders
    for src_folder, dst_folder in folders_to_sync:
        src_path = project_root / src_folder
        
        if src_path.exists():
            print(f"Syncing folder: {src_folder}")
            
            # Remove destination if it exists
            if dst_folder.exists():
                shutil.rmtree(dst_folder)
            
            # Copy folder
            shutil.copytree(src_path, dst_folder)
            print(f"  ✓ {src_folder} synced successfully")
        else:
            print(f"  ✗ {src_folder} not found (skipped)")
    
    print()
    
    # Sync files
    for src_file, dst_file in files_to_sync:
        src_path = project_root / src_file
        
        if src_path.exists():
            print(f"Syncing file: {src_file}")
            shutil.copy2(src_path, dst_file)
            print(f"  ✓ {src_file} synced successfully")
        else:
            print(f"  ✗ {src_file} not found (skipped)")
    
    print()
    print("=" * 60)
    print("✓ Template sync completed!")
    print()
    print("Next steps:")
    print("  1. Review changes in cookiecutter-template/")
    print("  2. Replace hardcoded values with {{cookiecutter.variable_name}}")
    print("  3. Test the template: cd cookiecutter-template && cookiecutter .")
    print("  4. Commit changes: git add . && git commit -m 'chore: sync template'")


if __name__ == "__main__":
    sync_template()
