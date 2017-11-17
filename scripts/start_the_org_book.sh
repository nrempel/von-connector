#! /bin/bash
set -e

if [ -z "$IP" ]; then
    von_generate_transactions
else
    von_generate_transactions -i "$IP"
fi

cd theorgbook

pipenv install
pipenv run python main.py
# pipenv shell