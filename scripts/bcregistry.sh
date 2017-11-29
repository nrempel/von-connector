#! /bin/bash
set -e

cd bcregistry

cat /home/indy/.genesis

pipenv install
pipenv run python server.py
# pipenv shell