.PHONY: help install dev test clean migrate upgrade downgrade

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Run development server"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean cache and build files"
	@echo "  make migrate    - Create new migration"
	@echo "  make upgrade    - Apply migrations"
	@echo "  make downgrade  - Rollback last migration"

install:
	pip install -r requirements.txt

dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true
	rm -rf htmlcov 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true

migrate:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1
