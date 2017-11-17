#! /bin/bash
set -e

if [ -z $IP ]; then
    von_generate_transactions
else
    von_generate_transactions -i $IP
fi


pipenv run python ./von-connector/main.py
pipenv shell