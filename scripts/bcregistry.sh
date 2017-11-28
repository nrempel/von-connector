#! /bin/bash
set -e

cd bcregistry

pipenv install
pipenv run python server.py
# pipenv shell