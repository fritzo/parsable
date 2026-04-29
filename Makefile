.Phony: FORCE install lint format test

PY_FILES = parsable/__init__.py example.py test_example.py setup.py

install:
	pip install -r requirements-dev.txt
	pip install .

lint: FORCE
	ruff check $(PY_FILES)
	ruff format --check $(PY_FILES)
	mypy parsable

format: FORCE
	ruff format $(PY_FILES)
	ruff check --fix --unsafe-fixes $(PY_FILES)

test: lint FORCE
	pytest --doctest-modules .

FORCE:
