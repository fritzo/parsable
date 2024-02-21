.Phony: FORCE install lint test

install:
	pip install -r requirements-dev.txt
	pip install .

lint:
	flake8

test: lint FORCE
	pytest --doctest-modules .

FORCE:
	
