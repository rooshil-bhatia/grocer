#this is a file where all my instances are being created 
from flask import Flask

from flask_cors import CORS

from db_instance import db

from flask_jwt_extended import JWTManager

from celery import Celery, Task

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app = Flask(__name__)

app.config.from_mapping(
    JWT_SECRET_KEY="8479240255dfda59422efb01e6a46f9f27324a5422985a5087c791a5c6d2284f",
    SQLALCHEMY_DATABASE_URI="sqlite:///project.db",
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True
    ),
)

from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379'})

celery_app = celery_init_app(app)

celery_app.conf.timezone = 'Asia/Kolkata'

from celery.schedules import crontab
import models,datetime

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(10.0, mailactivity.s(), name='order_summary')

    sender.add_periodic_task(
        crontab(hour=16, minute=53),
        sendhook.s(),
    )

    sender.add_periodic_task(
        crontab(0, 0, day_of_month='1'),
        mailactivity.s(),
    )




from json import dumps

from httplib2 import Http

WEBHOOK_URL = "https://chat.googleapis.com/v1/?key=dkgeytuipaenmqqWeMnbP"
def send_message(name):
    url = WEBHOOK_URL
    app_message = {
        'text': 'Hi ' + name + ' visit FreshFinds for the best offers in grocery shopping'}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(app_message),
    )

@celery_app.task
def sendhook():
    users = models.User.query.filter_by(role=2).all()
    t = datetime.datetime.now()
    for user in users:
        elapsed = t - user.last_visited
        if elapsed.total_seconds()>3600*24:
            send_message(user.mail)


import ordermail

@celery_app.task
def mailactivity():
    users = models.User.query.filter_by(role=2).all()
    for user in users:
        ordermail.mail(user)

jwt = JWTManager(app)

db.init_app(app)

CORS(app)

def get_csv():
    csv = ''
    csv+="Name,Price,Units Remaining,Expiry,Quantity\n"
    ps = models.Product.query.order_by(models.Product.added.desc()).all()
    for p in ps:
        csv+=p.name
        csv+=','
        csv+=str(p.rate)
        csv+=','
        csv+=str(p.units)
        csv+=','
        csv+=p.expiry
        csv+=','
        csv+=p.quantity
        csv+="\n"
    return csv

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@celery_app.task
def sendreport(mail):
    sender_email = "freshfinds@groceryapp.com"
    receiver_email = mail

    message = MIMEMultipart("alternative")
    message["Subject"] = "Products summary"
    message["From"] = sender_email
    message["To"] = receiver_email

    csv = MIMEText(get_csv())
    message.attach(csv)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP("0.0.0.0", 1025) as server:
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

