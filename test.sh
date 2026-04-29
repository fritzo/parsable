#!/bin/sh

ruff check *.py && \
ruff format --check *.py && \
mypy parsable.py && \
pytest --doctest-modules -v
