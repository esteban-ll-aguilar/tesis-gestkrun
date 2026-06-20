.PHONY: up down logs shell-api shell-db migrate test lint build

up:
	docker compose -f docker/docker-compose.yml up -d

down:
	docker compose -f docker/docker-compose.yml down

logs:
	docker compose -f docker/docker-compose.yml logs -f

shell-api:
	docker compose -f docker/docker-compose.yml exec api bash

shell-db:
	docker compose -f docker/docker-compose.yml exec postgres psql -U gestkrun

migrate:
	docker compose -f docker/docker-compose.yml exec api alembic upgrade head

migrate-new:
	docker compose -f docker/docker-compose.yml exec api alembic revision --autogenerate -m "$(message)"

test:
	docker compose -f docker/docker-compose.yml exec api pytest

test-coverage:
	docker compose -f docker/docker-compose.yml exec api pytest --cov=app --cov-report=html --cov-report=term

lint:
	docker compose -f docker/docker-compose.yml exec api ruff check .
	docker compose -f docker/docker-compose.yml exec api ruff format --check .

build:
	docker compose -f docker/docker-compose.yml build

restart:
	docker compose -f docker/docker-compose.yml restart

ps:
	docker compose -f docker/docker-compose.yml ps

clean:
	docker compose -f docker/docker-compose.yml down -v
