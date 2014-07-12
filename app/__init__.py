from flask import Flask
from twilio.rest import TwilioRestClient
from config import ACCOUNT_SID, AUTH_TOKEN
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

app.config.from_object('config')
db = SQLAlchemy(app)
from app import views, models, forms



