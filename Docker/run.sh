#!/bin/bash

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

cd deploy-tools
pyenv install 3.4.0

pyvenv-3.4 ~/.virtualenvs/deploy-tools
source ~/.virtualenvs/deploy-tools/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
