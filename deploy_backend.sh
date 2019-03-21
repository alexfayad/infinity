#!/usr/bin/env bash
tar xvfz backend.tar.gz --strip-components=5 -C backend/ opt/atlassian/pipelines/agent/build > ~/BACKEND.LOG &&
source venv/bin/activate >> ~/BACKEND.LOG &&
source .envs_export &&
cd backend
pip install -r requirements.txt >> ~/BACKEND.LOG &&
python manage.py makemigrations --merge --no-input>> ~/BACKEND.LOG &&
python manage.py migrate >> ~/BACKEND.LOG &&
python manage.py collectstatic --no-input >> ~/BACKEND.LOG &&
systemctl --user restart infinity.service >> ~/BACKEND.LOG
systemctl --user restart celery.service >> ~/BACKEND.LOG
systemctl --user restart beat.service >> ~/BACKEND.LOG
