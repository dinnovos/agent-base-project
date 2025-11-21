"""
Script para probar el template de cookiecutter localmente.

Este script:
1. Genera un proyecto de prueba usando cookiecutter
2. Instala las dependencias
3. Verifica que el proyecto se pueda ejecutar
4. Limpia los archivos temporales

Uso:
    python test_template.py
"""

import subprocess
import sys
import shutil
from pathlib import Path
import json


def run_command(cmd, cwd=None, check=True):
    """Ejecuta un comando y retorna el resultado."""
    print(f"\n→ Ejecutando: {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False
    )
    
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
    
    if check and result.returncode != 0:
        sys.exit(1)
    
    return result


def test_template():
    """Prueba el template de cookiecutter."""
    
    project_root = Path(__file__).parent
    temp_dir = project_root / "temp_test"
    template_dir = project_root / "cookiecutter-template"
    
    print("="*60)
    print("PRUEBA DEL TEMPLATE DE COOKIECUTTER")
    print("="*60)
    
    # 1. Limpiar directorio temporal si existe
    if temp_dir.exists():
        print(f"\n→ Limpiando directorio temporal: {temp_dir}")
        shutil.rmtree(temp_dir)
    
    temp_dir.mkdir()
    
    # 2. Configuración del proyecto
    config = {
        "project_name": "Test Agent Project",
        "project_slug": "test_agent_project",
        "description": "A test project for validating the template",
        "port": "8000",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "python_version": "3.11"
    }
    
    print(f"\n→ Configuración del proyecto:")
    print(json.dumps(config, indent=2))
    
    # 3. Generar proyecto con cookiecutter usando variables directas
    print(f"\n→ Generando proyecto desde template...")
    
    # Construir comando con todas las variables
    extra_context = " ".join([f'{key}="{value}"' for key, value in config.items()])
    cmd = f'cookiecutter "{template_dir}" --no-input --output-dir "{temp_dir}" {extra_context}'
    result = run_command(cmd)
    
    project_dir = temp_dir / config["project_slug"]
    
    if not project_dir.exists():
        print(f"✗ Error: El proyecto no se generó en {project_dir}")
        sys.exit(1)
    
    print(f"✓ Proyecto generado en: {project_dir}")
    
    # 4. Verificar estructura del proyecto
    print("\n→ Verificando estructura del proyecto...")
    required_files = [
        "requirements.txt",
        "run.py",
        ".env.example",
        "README.md",
        "Dockerfile",
        "docker-compose.yml",
        "langgraph.json",
        "pytest.ini",
        "alembic.ini",
    ]
    
    required_dirs = [
        "src",
        "agents",
        "tests",
        "alembic",
    ]
    
    all_ok = True
    for file in required_files:
        if (project_dir / file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - NO ENCONTRADO")
            all_ok = False
    
    for dir_name in required_dirs:
        if (project_dir / dir_name).is_dir():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - NO ENCONTRADO")
            all_ok = False
    
    if not all_ok:
        print("\n✗ La estructura del proyecto está incompleta")
        sys.exit(1)
    
    # 5. Verificar que las variables fueron reemplazadas
    print("\n→ Verificando reemplazo de variables...")
    
    # Verificar src/main.py
    main_py = project_dir / "src" / "main.py"
    if main_py.exists():
        content = main_py.read_text(encoding='utf-8')
        if config["project_name"] in content:
            print(f"  ✓ project_name reemplazado en src/main.py")
        else:
            print(f"  ✗ project_name NO reemplazado en src/main.py")
            all_ok = False
    
    # Verificar Dockerfile
    dockerfile = project_dir / "Dockerfile"
    if dockerfile.exists():
        content = dockerfile.read_text(encoding='utf-8')
        if f'python:{config["python_version"]}' in content:
            print(f"  ✓ python_version reemplazado en Dockerfile")
        else:
            print(f"  ✗ python_version NO reemplazado en Dockerfile")
            all_ok = False
    
    if not all_ok:
        print("\n✗ Algunas variables no fueron reemplazadas correctamente")
        sys.exit(1)
    
    # 6. Verificar sintaxis de Python
    print("\n→ Verificando sintaxis de archivos Python...")
    result = run_command(f'python -m py_compile src/main.py', cwd=project_dir, check=False)
    if result.returncode == 0:
        print("  ✓ src/main.py - Sintaxis correcta")
    else:
        print("  ✗ src/main.py - Error de sintaxis")
        all_ok = False
    
    # 7. Resumen
    print("\n" + "="*60)
    if all_ok:
        print("✓ TODAS LAS PRUEBAS PASARON")
        print("="*60)
        print(f"\nProyecto de prueba generado en: {project_dir}")
        print("\nPara probar manualmente:")
        print(f"  cd {project_dir}")
        print("  python -m venv venv")
        print("  .\\venv\\Scripts\\activate")
        print("  pip install -r requirements.txt")
        print("  python run.py")
        print("\nPara limpiar:")
        print(f"  rmdir /s /q {temp_dir}")
    else:
        print("✗ ALGUNAS PRUEBAS FALLARON")
        print("="*60)
        sys.exit(1)


if __name__ == "__main__":
    try:
        test_template()
    except KeyboardInterrupt:
        print("\n\n✗ Prueba cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
