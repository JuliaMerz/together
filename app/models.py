from app import db
from datetime import datetime

class Event(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  what = db.Column(db.String(30))
  where = db.Column(db.String(50))
  length = db.Column(db.Integer)
  wait_time = db.Column(db.Integer)
  pre_delay = db.Column(db.Integer)
  required_people = db.Column(db.Integer)
  description = db.Column(db.Text)
  happened_count = db.Column(db.Integer)
  created = db.Column(db.DateTime, default=datetime.utcnow)
  users_subscribed = db.relationship('EventSubscription', backref='event', lazy='dynamic')

class User(db.Model):
  id = db.Column(db.String, primary_key=True)
  created = db.Column(db.DateTime, default=datetime.utcnow)
  updated = db.Column(db.DateTime, default=datetime.utcnow,
                      onupdate=datetime.utcnow)
  name = db.Column(db.String)
  profile_url = db.Column(db.String)
  access_token = db.Column(db.String)
  email = db.Column(db.String, unique=True)
  phone_number = db.Column(db.String, unique=True)
  event_subscriptions = db.relationship('EventSubscription', backref='user',lazy='dynamic')

class EventSubscription(db.Model):
  id = db.Column(db.String, primary_key=True)
  created = db.Column(db.DateTime, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

