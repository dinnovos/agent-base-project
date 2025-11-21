"""
Sync script to copy changes from the main project to the template.

This script copies key directories and files from the main project
to the cookiecutter template, preserving the template structure.
Then it replaces hardcoded values with Cookiecutter variables.

Usage:
    python sync_template.py
"""

import shutil
import os
from pathlib import Path
from typing import List, Tuple


def get_replacements() -> List[Tuple[str, str, str]]:
    """
    Define the specific replacements to make.
    
    Returns list of tuples: (file_relative_path, old_value, new_value)
    """
    return [
        # src/main.py replacements
        ("src/main.py", '"FastAPI Base Project"', '"{{cookiecutter.project_name}}"'),
        ("src/main.py", '"A modular FastAPI project with JWT authentication and SQLAlchemy"', 
         '"{{cookiecutter.description}}"'),
        
        # Dockerfile replacements
        ("Dockerfile", "FROM python:3.11-slim", "FROM python:{{cookiecutter.python_version}}-slim"),
        ("Dockerfile", "EXPOSE 8000", "EXPOSE {{cookiecutter.port}}"),
        ("Dockerfile", '"--port", "8000"', '"--port", "{{cookiecutter.port}}"'),
        
        # .env.example replacements
        (".env.example", "sqlite:///./app.db", "sqlite:///./{{cookiecutter.project_slug}}.db"),
    ]


def replace_hardcoded_values(template_base: Path) -> int:
    """
    Replace hardcoded values with Cookiecutter variables.
    
    Args:
        template_base: Path to the template base directory
        
    Returns:
        Total number of replacements made
    """
    replacements = get_replacements()
    total_replacements = 0
    
    print("\nReplacing hardcoded values with Cookiecutter variables...")
    print("=" * 60)
    
    for file_rel_path, old_value, new_value in replacements:
        file_path = template_base / file_rel_path
        
        if not file_path.exists():
            print(f"  ✗ {file_rel_path} not found (skipped)")
            continue
        
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count occurrences
            count = content.count(old_value)
            
            if count > 0:
                # Replace
                new_content = content.replace(old_value, new_value)
                
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  ✓ {file_rel_path}: {count} replacement(s)")
                total_replacements += count
            else:
                print(f"  ℹ {file_rel_path}: value not found (skipped)")
        
        except Exception as e:
            print(f"  ✗ {file_rel_path}: error - {e}")
    
    return total_replacements


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
    
    # Replace hardcoded values
    total_replacements = replace_hardcoded_values(template_base)
    
    print()
    print("=" * 60)
    print("✓ Template sync completed!")
    print(f"✓ Total replacements made: {total_replacements}")
    print()
    print("Next steps:")
    print("  1. Review changes in cookiecutter-template/")
    print("  2. Test the template: cd cookiecutter-template && cookiecutter .")
    print("  3. Verify the generated project has correct values")
    print("  4. Commit changes: git add . && git commit -m 'chore: sync template and replace hardcoded values'")


if __name__ == "__main__":
    sync_template()
