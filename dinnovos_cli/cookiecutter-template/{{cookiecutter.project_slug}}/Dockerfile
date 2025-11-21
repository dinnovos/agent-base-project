FROM python:{{cookiecutter.python_version}}-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE {{cookiecutter.port}}

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "{{cookiecutter.port}}"]
