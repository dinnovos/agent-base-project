# Dinnovos Agent Template

This is a Cookiecutter template for creating new AI agent projects based on LangGraph and FastAPI.

## How to Use This Template

This template is used by the `dinnovos-create-agent` CLI command. Users should not interact with this directory directly.

### For Template Developers

To test this template locally:

```bash
# Install cookiecutter
pip install cookiecutter

# Generate a new project from this template
cookiecutter .
```

### Template Variables

The template uses the following Cookiecutter variables:

- `project_name`: The human-readable name of the project (e.g., "My Agent Project")
- `project_slug`: The Python-friendly name (auto-generated from project_name)
- `description`: A brief description of the project
- `port`: The port number for the development server (default: 8000)
- `author_name`: The name of the project author
- `author_email`: The email of the project author
- `python_version`: The Python version to use (default: 3.11)

### Structure

The template generates a complete project structure with:

- FastAPI application setup
- SQLAlchemy ORM configuration
- JWT authentication
- LangGraph agent framework
- Docker and Docker Compose configuration
- Database migrations with Alembic
- Test suite with pytest
- Environment configuration

## Maintenance

When updating the template:

1. Make changes to files in the `{{cookiecutter.project_slug}}/` directory
2. Replace hardcoded values with `{{cookiecutter.variable_name}}`
3. Test locally with `cookiecutter .`
4. Commit and push changes
5. Update the CLI version in `setup.py`
