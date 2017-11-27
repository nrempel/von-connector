#! /bin/bash
set -e

if [ -z "$IP" ]; then
    von_generate_transactions
else
    von_generate_transactions -i "$IP"
fi

cd bcregistry

cat /home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis

pipenv install
pipenv run python main.py
# pipenv shell