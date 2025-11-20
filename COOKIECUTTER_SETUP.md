# Cookiecutter Setup Guide

This document explains how to use and maintain the Cookiecutter template for creating new Dinnovos agent projects.

## For End Users

### Installation

Install the CLI tool:

```bash
pip install dinnovos-agent-cli
```

Or, if you're installing from the repository:

```bash
cd agent-base-project
pip install -e .
```

### Creating a New Project

Run the command to create a new project:

```bash
dinnovos-create-agent
```

The CLI will ask you for the following information:

- **project_name**: The human-readable name of your project (e.g., "My AI Agent")
- **project_slug**: The Python-friendly name (auto-generated, but you can customize it)
- **description**: A brief description of what your project does
- **port**: The port number for the development server (default: 8000)
- **author_name**: Your name
- **author_email**: Your email address
- **python_version**: The Python version to use (default: 3.11)

### Example

```bash
$ dinnovos-create-agent
project_name [My Agent Project]: My Chatbot
project_slug [my_chatbot]: 
description [An AI agent project...]: A conversational AI chatbot
port [8000]: 8001
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
python_version [3.11]: 
```

This will create a new directory called `my_chatbot/` with a complete project structure.

### Getting Started with Your New Project

```bash
cd my_chatbot
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
python run.py
```

Your API will be available at `http://localhost:8001`

---

## For Template Developers

### Project Structure

```
agent-base-project/
├── cookiecutter-template/          # Template directory
│   ├── README.md                   # Template documentation
│   └── {{cookiecutter.project_slug}}/
│       ├── src/                    # Main application code
│       ├── agents/                 # LangGraph agents
│       ├── tests/                  # Test suite
│       ├── alembic/                # Database migrations
│       ├── run.py                  # Development server
│       ├── requirements.txt        # Dependencies
│       ├── Dockerfile              # Docker configuration
│       ├── docker-compose.yml      # Docker Compose setup
│       └── ...
├── dinnovos_cli/                   # CLI package
│   ├── __init__.py
│   └── main.py                     # CLI entry point
├── setup.py                        # Package configuration
├── MANIFEST.in                     # Package manifest
└── COOKIECUTTER_SETUP.md          # This file
```

### Template Variables

The template uses Cookiecutter variables in the format `{{cookiecutter.variable_name}}`:

- `{{cookiecutter.project_name}}` - Project name
- `{{cookiecutter.project_slug}}` - Python-friendly project name
- `{{cookiecutter.description}}` - Project description
- `{{cookiecutter.port}}` - Server port
- `{{cookiecutter.author_name}}` - Author name
- `{{cookiecutter.author_email}}` - Author email
- `{{cookiecutter.python_version}}` - Python version

### Updating the Template

When you make changes to the main project, you should sync those changes to the template:

1. **Make changes to the main project** (in `src/`, `agents/`, etc.)

2. **Copy changes to the template**:
   ```bash
   python sync_template.py
   ```

3. **Replace hardcoded values with variables**:
   - In `src/main.py`: Replace `title="FastAPI Base Project"` with `title="{{cookiecutter.project_name}}"`
   - In `run.py`: Replace `port=8000` with `port={{cookiecutter.port}}`
   - In `Dockerfile`: Replace `FROM python:3.11` with `FROM python:{{cookiecutter.python_version}}`
   - And so on...

4. **Test the template locally**:
   ```bash
   cd cookiecutter-template
   cookiecutter .
   ```

5. **Update the version** in `setup.py`:
   ```python
   setup(
       name="dinnovos-agent-cli",
       version="1.0.1",  # Increment version
       ...
   )
   ```

6. **Commit and push**:
   ```bash
   git add .
   git commit -m "feat: update template with new features"
   git push
   ```

### Publishing to PyPI

To publish the CLI tool to PyPI:

1. **Build the package**:
   ```bash
   pip install build twine
   python -m build
   ```

2. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```

3. **Users can then install with**:
   ```bash
   pip install dinnovos-agent-cli
   ```

### Testing Locally

To test the CLI locally before publishing:

```bash
# Install in development mode
pip install -e .

# Test the command
dinnovos-create-agent

# Verify the generated project works
cd generated_project_name
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Adding New Template Variables

To add a new variable to the template:

1. **Update `cookiecutter.json`**:
   ```json
   {
     "project_name": "My Agent Project",
     "new_variable": "default_value"
   }
   ```

2. **Use the variable in template files**:
   ```
   {{cookiecutter.new_variable}}
   ```

3. **Test locally** to ensure it works correctly

### Troubleshooting

**Issue**: Template not found when running `dinnovos-create-agent`
- **Solution**: Ensure the `cookiecutter-template/` directory exists in the project root

**Issue**: Variables not being replaced in generated projects
- **Solution**: Ensure variables are in the format `{{cookiecutter.variable_name}}` (with double braces)

**Issue**: Generated project has import errors
- **Solution**: Verify that all necessary files are included in the template and that the structure matches the original project

---

## Additional Resources

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
