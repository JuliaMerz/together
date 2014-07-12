from app import db

class Event(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  what = db.Column(db.String(30))
  where = db.Column(db.String(50))
  length = db.Column(db.Integer)
  wait_time = db.Column(db.Integer)
  pre_delay = db.Column(db.Integer)
  happened_count = db.Column(db.Integer)
  required_people = db.Column(db.Integer)
  description = db.Column(db.Text)

