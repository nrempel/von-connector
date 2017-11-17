#! /bin/bash
set -e

if [ -z "$IP" ]; then
    von_generate_transactions
else
    von_generate_transactions -i "$IP"
fi

cp /home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis /usr/local

cd bcregistry

pipenv --three
pipenv run python main.py
# pipenv shell