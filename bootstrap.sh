#!/bin/sh

export FLASK_APP=./backend/api
export FLASK_ENV=development

source $(pipenv --venv)/bin/activate

npm --prefix ./frontend install
npm --prefix ./frontend run build

flask run
