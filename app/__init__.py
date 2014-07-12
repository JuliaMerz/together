from flask import Flask
from twilio.rest import TwilioRestClient
from config import ACCOUNT_SID, AUTH_TOKEN

app = Flask(__name__)
client = twilio.TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

from app import views


