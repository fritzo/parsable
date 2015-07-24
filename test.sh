#!/bin/sh

pep8 *.py && \
pyflakes *.py && \
nosetests --with-doctest -v
