#!/usr/bin/env bash

LIGHT_CYAN=\033[1;36m
NO_COLOR=\033[0m

.PHONY: docs

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "install - install requirements packages"
	@echo "test - run tests quickly with the default Python"
	@echo "pytest - run tests with pytest"
	@echo "coverage - get code coverage report"
	@echo "lint - lint the code"
	@echo "checkstatictypes - check static types"
	@echo "format - format the code"
	@echo "docs - build the source code docs"

# Full clean
clean:
	@echo "${LIGHT_CYAN}Cleaning working directory...${NO_COLOR}"
	@rm -r ./env/

# Install requirements
install: requirements.txt
	@echo "${LIGHT_CYAN}Creating virtual environment...${NO_COLOR}"
	python3 -m venv env
	@echo "${LIGHT_CYAN}Activating created virtual environment...${NO_COLOR}"
	source env/bin/activate
	@echo "${LIGHT_CYAN}Installing requirements from requirements.txt...${NO_COLOR}"
	pip3 install -r requirements.txt

# Run tests
test:
	@echo "${LIGHT_CYAN}Running tests...${NO_COLOR}"
	python3 manage.py test --parallel

# Run tests with pytest
pytest: 
	@echo "${LIGHT_CYAN}Running tests with pytest...${NO_COLOR}"
	pytest --durations=1 -n 8

# Get code coverage report
coverage:
	@echo "${LIGHT_CYAN}Running tests and collecting coverage data...${NO_COLOR}"
	pytest --cov=. -n 8
	coverage combine
	@echo "${LIGHT_CYAN}Reporting code coverage data...${NO_COLOR}"
	coverage report
	@echo "${LIGHT_CYAN}Creating HTML report...${NO_COLOR}"
	coverage html
	@echo "${LIGHT_CYAN}Creating coverage badge...${NO_COLOR}"
	@rm ./coverage.svg
	coverage-badge -o coverage.svg

# Lint the project
lint: 
	@echo "${LIGHT_CYAN}Linting code...${NO_COLOR}"
	isort . --check-only
	black . --check
	flake8 .

# Check static typing
checkstatictypes:
	@echo "${LIGHT_CYAN}Checking static types...${NO_COLOR}"
	mypy

# Format code
format: 
	@echo "${LIGHT_CYAN}Formatting code...${NO_COLOR}"
	isort .
	black .

# Build docs
docs:
	@echo "${LIGHT_CYAN}Building docs...${NO_COLOR}"