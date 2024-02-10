.Phony: FORCE test

lint:
	flake8

test: lint FORCE
	pytest --doctest-modules .

FORCE:
	