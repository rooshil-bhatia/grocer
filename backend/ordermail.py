import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import models

def mail(user):
    sender_email = "leftwinger511@gmail.com"
    receiver_email = user.mail

    orders = models.Orders.get(user.mail)

    message = MIMEMultipart("alternative")
    message["Subject"] = "Order summary"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    part_html = generate_html(orders,receiver_email)

    part1 = MIMEText(part_html, "html")

    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP("0.0.0.0", 1025) as server:
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

from flask import render_template
import json
def generate_html(orders,mail):
    order_list = []
    for order in orders:
        o = {}
        o['items'] = []
        total = 0
        orderDict = json.loads(order.order)
        for i in orderDict:
            d = {}
            p = models.Product.query.filter_by(id=i).one_or_none()
            d['name'] = p.name
            d['rate'] = p.rate
            d['units'] = orderDict[i]
            d['price'] = p.rate*orderDict[i]
            o['items'].append(d)
            total+=d['price']
        o['total'] = total
        order_list.append(o)
    return render_template('orders_template.html', name=mail,olist=order_list)


