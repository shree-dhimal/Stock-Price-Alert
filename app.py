from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf
import time
import smtplib


app = Flask(__name__)
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
    #     return f"{self.Sn} -{self.symbol}-{self.price}- {self.email}-{self.phone} - {self.alert_time}"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        symbol = request.form['Symbol'].upper()
        price = request.form['Price']
        email = request.form['smsText']
        phone = request.form['emailText']
        dropdown1 = request.form['time']
        alert_type = request.form['alert']

        if dropdown1 == '_15':
            f_time = 15
        elif dropdown1 == '_20':
            f_time = 20
        elif dropdown1 == '_1':
            f_time = 60

        print(symbol)

        alert = Alert(symbol=symbol, price=price, email=email,
                      phone=phone, alert_time=f_time, alert_type=alert_type)
        db.session.add(alert)
        db.session.commit()

        def get_tickerprice(symbol):
            stock = yf.Ticker(symbol)
            latest_price = stock.history(period='1d')['Close'][0]
            price = round(latest_price, 2)
        return price

        def send_notification(notification_type, symbol, email, phone_number, price, threshold):
            if notification_type == 'email':
                sender = 'noreplynofacemaskalert@gmail.com'
                sender_pass = 'kzgocnslulvajdxb'
                reciever = email
                subject = 'Stock Threshold Reached'
                body = f'The price of the stock "{symbol}" has reached the threshold'
                msg = f'Subject: {subject}\n\n{body}'
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, sender_pass)
                server.sendmail(sender, reciever, msg)
                server.quit()
            elif notification_type == 'sms':
                pass

        return render_template('submit.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
