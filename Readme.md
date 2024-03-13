To install frontend part, 
cd to frontend 
Then npm install; npm run dev

----------------------------------------

To install the backend part,

cd to backend
python3 -m venv .venv to create virtual environment
. .venv/bin/activate
pip install -r requirements.txt - to install required packages
flask run --debug to run the app

----------------------------------------

redis-cli to start the redis server on default port

----------------------------------------

To run the celery workers

cd to backend 
celery -A app_instance.celery_app worker --loglevel INFO

-----------------------------------------

To run celery beat to run scheduled tasks

cd to backend
celery -A app_instance.celery_app beat --loglevel INFO