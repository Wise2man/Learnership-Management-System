.PHONY: help install run migrate migrations test lint format demo check

help:            ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

install:         ## Install all packages
	pip install -r requirements.txt

run:             ## Start the development server
	python manage.py runserver

migrate:         ## Apply database migrations
	python manage.py migrate

migrations:      ## Create new migrations after changing a model
	python manage.py makemigrations

test:            ## Run all tests
	pytest

lint:            ## Check code style
	ruff check . && ruff format --check .

format:          ## Fix code style automatically
	ruff check . --fix && ruff format .

demo:            ## Fill the database with demo users and courses
	python manage.py create_demo_data

check:           ## Everything the CI checks (run before opening a Pull Request)
	ruff check . && ruff format --check . && python manage.py check && python manage.py makemigrations --check --dry-run && pytest
