import os

# Your Account Sid and Auth Token from twilio.com/user/account
ACCOUNT_SID = "AC32a3c49700934481addd5ce1659f04d2"
AUTH_TOKEN  = "93cea5d8882178bfdec8abae2c18cf67"

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


