from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
  """
  If logged in, return main.html. Otherwise return signin.html
  """
  return render_template('base.html')

