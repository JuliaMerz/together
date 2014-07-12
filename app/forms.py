from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, IntegerField, BooleanField

class ProfileForm(Form):
  email = TextField('email')
  phone_number = IntegerField('phone_number')

class EventForm(Form):
  what = TextField('what')
  where = TextField('where')
  length = IntegerField('length')
  wait_time = IntegerField('wait_time')
  pre_delay = IntegerField('pre_delay')
  required_people = IntegerField('required_people')
  description = TextAreaField('description')
  public = BooleanField('public')
