#!/bin/sh

flake8 *.py && \
pytest --doctest-modules -v
