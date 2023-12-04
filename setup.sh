#!/bin/sh

set -e


# Colors

DEFAULT_COLOR="\e[0m"

BLUE="\033[34m"

YELLOW="\033[33m"


# Check arguments

if [[ -z $1 ]]; then
    echo -e "\n--------------------------------------\n";
    echo -e "${YELLOW}Please enter the <secret_key> argument${DEFAULT_COLOR}";
    echo -e "\n--------------------------------------\n";
    exit 1;
else
    secret_key=$1
fi

if [[ $1 == "<secret_key>" ]]; then 
    echo -e "\n--------------------------------------\n";
    echo -e "${YELLOW}Please enter the <secret_key> argument${DEFAULT_COLOR}";
    echo -e "\n--------------------------------------\n";
    exit 1;
fi


# Setup logs

mkdir -p src/logs

touch src/logs/general.log 2> out.txt


# Setup venv

poetry install --no-root


# Setup env

mkdir -p env

echo """
# POSTGRES
POSTGRES_DB=e-learning
POSTGRES_USER=e-learning
POSTGRES_PASSWORD=12345678
""" > env/.db.env

echo """
# APP
SECRET_KEY={secret_key}
DEBUG=1
LOGGING_LEVEL=DEBUG

# DB
DB_NAME=e-learning
DB_USER=e-learning
DB_PASSWORD=12345678
DB_HOST=db
DB_POST=5432

# ADMIN
DEFAULT_ADMIN_NAME=adm1
DEFAULT_ADMIN_EMAIL=adm1@adm1.com
DEFAULT_ADMIN_PASSWORD=adm1
""" > env/.e-learning.env

sed -i "s/{secret_key}/${secret_key}/g" env/.e-learning.env

rm -rf out.txt

