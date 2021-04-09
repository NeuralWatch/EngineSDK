.PHONY: clean format lint requirements create_environment

.EXPORT_ALL_VARIABLES:

#################################################################################
# GLOBALS
##################################################################################
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = app
PYTHON_INTERPRETER = python3
SRC = enginesdk/
TEST = enginesdk/tests/

#################################################################################
# COMMANDS
##################################################################################
		
## Delete all compiled Python files
clean:	
		find . -not -path "./.venv/*" -type f -name "*.py[co]" -exec rm -rf {} \;	
		find . -not -path "./.venv/*" -type d -name "__pycache__" -exec rm -rf {} \;	
		find . -not -path "./.venv/*" -type d -name "*.egg-info" -exec rm -rf {} \;	
		find . -not -path "./.venv/*" -type d -name "dist" -exec rm -rf {} \;	
		rm -rf htmlcov .coverage .hypothesis
		
## Format code using black
format:	
		$(PYTHON_INTERPRETER) -m poetry run black $(SRC)
		$(PYTHON_INTERPRETER) -m poetry run isort $(SRC) --profile black
		$(PYTHON_INTERPRETER) -m poetry run black $(TEST)
		$(PYTHON_INTERPRETER) -m poetry run isort $(TEST) --profile black

## Lint using flake8
lint:	
		$(PYTHON_INTERPRETER) -m poetry run pylint --fail-under=6 $(SRC) --exit-zero	
		$(PYTHON_INTERPRETER) -m poetry run flake8 $(SRC) --count --exit-zero --per-file-ignores="__init__.py:F401" --max-complexity=10 --max-line-length=127 --statistics	
		
## Run tests
test:
		$(PYTHON_INTERPRETER) -m poetry run pytest $(TEST) -s --cov=$(SRC) --cov-report html:./htmlcov --cov-fail-under 60 --log-cli-level DEBUG
		$(PYTHON_INTERPRETER) -m poetry run coverage-badge -fo coverage.svg

## Set up the environment using poetry
create_environment:	
		$(PYTHON_INTERPRETER) -m pip install -U poetry	
		$(PYTHON_INTERPRETER) -m poetry install

## Build wheel package
build:	
		$(PYTHON_INTERPRETER) -m poetry build

## Deploy on CloudRun
deploy:
	gcloud builds submit . --config=cloudbuild.yaml --substitutions=BRANCH_NAME=local,_REGION=$(REGION),_ENGINE_SLUG=$(ENGINE_SLUG),_MODEL=$(MODEL)