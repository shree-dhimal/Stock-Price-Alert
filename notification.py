from app import *
import yfinance as yf
from flask_sqlalchemy import SQLAlchemy



def get_tickerprice(symbol):
    stock = yf.Ticker(symbol)
    latest_price = stock.history(period='1d')['Close'][0]
    price = round(latest_price, 2)
    return price 


def send_notification(notification_type,symbol,email,phone_number,price,threshold):
    if notification_type== 'email':
        sender = 'noreplynofacemaskalert@gmail.com'
        sender_pass = 'kzgocnslulvajdxb'
        reciever = email
        subject = 'Stock Threshold Reached'
        body = f'The price of the stock "{symbol}" has reached the threshold of {threshold} and price is {price}.'
        msg = f'Subject: {subject}\n\n{body}'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, sender_pass)
        server.sendmail(sender, reciever, msg)
        server.quit()
    elif notification_type=='sms':
        pass