from flask.ext.wtf import Form
from wtforms import TextField

class ProfileForm(Form):
  email = TextField('email')
  phone_number = TextField('phone_number')
