#!/bin/sh

ruff check parsable/__init__.py *.py && \
ruff format --check parsable/__init__.py *.py && \
mypy parsable && \
pytest --doctest-modules -v
