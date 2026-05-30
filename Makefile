.PHONY: up down logs migrate shell test check zip
up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f web

migrate:
	python manage.py migrate

shell:
	python manage.py shell

test:
	pytest

check:
	python manage.py check
