from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf
import time
import smtplib
import schedule
import atexit
import os
from twilio.rest import Client
import re


app = Flask(__name__)
# app.secret_key = "12345"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///stockalert.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Alert(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    alert_time = db.Column(db.Integer, nullable=False)
    alert_type = db.Column(db.String(50))

    # def __repr__(self) -> str:
    #     return f"{self.Id} -{self.symbol}-{self.price}- {self.email}-{self.phone} - {self.alert_time}"


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        symbol = request.form['Symbol'].upper()

        price = request.form['Price']

        email = request.form['emailText']

        phone = request.form['smsText']
        dropdown1 = request.form['time']
        alert_type = request.form['alert']

        # if re.match("^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$",email):
        #     if re.match("")
        if dropdown1 == '_15':
            f_time = 15
        elif dropdown1 == '_20':
            f_time = 20
        elif dropdown1 == '_1':
            f_time = 60

        # ticker = yf.Ticker(symbol)
        # # validating the given stock symbol
        # try:
        #     stock = ticker.info

        alert = Alert(symbol=symbol, price=price, email=email,
                          phone=phone, alert_time=f_time, alert_type=alert_type)
        db.session.add(alert)
        db.session.commit()

        return render_template('submit.html', alert=alert)
        # except :
        #     flash("Cannot get info of,"+ symbol)

    else:
        return render_template('index.html')


@app.route('/run', methods=['GET', 'POST'])
def run():
    run = True
    if request.method == 'POST':

        data = Alert.query.filter_by(Id=1).first()
        loop_time = data.alert_time
        if loop_time == 15:
            print("imhere")
            schedule.every(15).minutes.do(run_task)
        if loop_time == 20:
            schedule.every(20).minutes.do(run_task)
        if loop_time == 60:
            schedule.every(60).minutes.do(run_task)

        while run == True:
            schedule.run_pending()
            time.sleep(1)
        # if request.form.get('action2') == 'VALUE2':
        #     run = False

    else:
        return render_template('index.html')


def send_notification(notification_type, symbol, email_, phone_number, price, threshold):
    if notification_type == 'email':
        sender = 'noreplynofacemaskalert@gmail.com'
        sender_pass = 'kzgocnslulvajdxb'
        reciever = email_
        subject = 'Stock Threshold Reached'
        body = f'The price of the stock "{symbol}" has reached the threshold of "{threshold}" and the new Stock price is"{price}" '
        msg = f'Subject: {subject}\n\n{body}'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, sender_pass)
        server.sendmail(sender, reciever, msg)
        server.quit()
        print('Notification Sent')
    elif notification_type == 'sms':
        print("im in sms")
        # account_sid = os.environ['']
        # auth_token = os.environ['']

        # client = Client(account_sid, auth_token)

        # message = client.messages \
        #                 .create(
        #                     body="Stock Threshold Reached",
        #                     from_='+16813293340',
        #                     to='+9779843393667'
        #                 )
        # print(message.body)
        pass


def run_task():
    # print('imhere')
    data = Alert.query.filter_by(Id=1).first()
    # print(data)
    symbol = data.symbol
    price = data.price
    email = data.email
    phone = data.phone
    # alert_time = data.alert_time
    alert_type = data.alert_type

    stock = yf.Ticker(symbol)
    latest_price = stock.history(period='1d')['Close'][0]
    stock_price = round(latest_price, 2)
    # print(price)
    # print(email)
    # print(stock_price)
    if stock_price >= float(price):
        print('the price is greater')
        send_notification(alert_type, symbol, email, phone, stock_price, price)
    else:
        pass


def clear_data():
    db.session.query(Alert).delete()
    db.session.commit()


atexit.register(clear_data)


if __name__ == "__main__":
    db.create_all()

    app.run(debug=True)
