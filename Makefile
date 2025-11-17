.PHONY: help install run dev test clean docker-up docker-down migrate

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install black flake8 mypy pytest pytest-asyncio pytest-cov

run: ## Run the application
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev: ## Run in development mode with hot reload
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

test: ## Run tests
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	pytest-watch tests/ -v

lint: ## Run linters
	black app/ tests/ --check
	flake8 app/ tests/
	mypy app/

format: ## Format code
	black app/ tests/

clean: ## Clean cache and temporary files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .mypy_cache

docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-restart: ## Restart Docker containers
	docker-compose restart

docker-clean: ## Remove Docker containers and volumes
	docker-compose down -v

migrate: ## Run database migrations
	alembic upgrade head

migrate-create: ## Create a new migration
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

migrate-rollback: ## Rollback last migration
	alembic downgrade -1

db-reset: ## Reset database (WARNING: destroys all data)
	docker-compose down -v
	docker-compose up -d postgres
	sleep 5
	alembic upgrade head

celery-worker: ## Run Celery worker
	celery -A app.celery_app worker --loglevel=info

celery-beat: ## Run Celery beat scheduler
	celery -A app.celery_app beat --loglevel=info

shell: ## Open Python shell with app context
	python -i -c "from app.main import app; from app.core.database import engine"

api-docs: ## Open API documentation
	@echo "Opening API docs at http://localhost:8000/docs"
	open http://localhost:8000/docs || xdg-open http://localhost:8000/docs
