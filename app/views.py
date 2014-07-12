from facebook import get_user_from_cookie, GraphAPI
from flask import render_template, g, flash, session, url_for, redirect, request
from config import FB_APP_ID, FB_APP_NAME, FB_APP_SECRET
from forms import ProfileForm
from app import app, db
from app import models

@app.route('/')
@app.route('/index')
def index():
  """
  If logged in, return main.html. Otherwise return signin.html
  """
  if g.user:
    if g.first_time:
      g.first_time = False
      return redirect(url_for("profile"))
    return render_template("base.html", app_id=FB_APP_ID, name=FB_APP_NAME)
  else:
    return render_template('fbsignin.html', app_id=FB_APP_ID, name=FB_APP_NAME)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
  """
  Use this to let people change emails and phone numbers
  """
  if g.user is None:
    return redirect(url_for("index"))

  form = ProfileForm()
  user = g.user
  user = {"nickname":"Bob"}
  if form.validate_on_submit():
    g.user.email = form.email.data
    g.user.phone_number = form.phone_number.data
    db.session.add(g.user)
    db.session.commit()
    flash('Your changes have been saved')
  user['email_template'] = "Please enter your email address"
  user['phone_template'] = "Please enter your phone number"
  if g.user.email:
    user['email_template'] = g.user.email
  if g.user.phone_number:
    user['phone_template'] = g.user.phone_number
  return render_template("profile.html", app_id=FB_APP_ID, name=FB_APP_NAME, user = user, form=form)
@app.route('/logout')
def logout():
  """Log out the user from the application.

  Log out the user from the application by removing them from the
  session.  Note: this does not log the user out of Facebook - this is done
  by the JavaScript SDK.
  """
  session.pop('user', None)
  return redirect(url_for('index'))

@app.before_request
def get_current_user():
  """Set g.user to the currently logged in user.

  Called before each request, get_current_user sets the global g.user
  variable to the currently logged in user.  A currently logged in user is
  determined by seeing if it exists in Flask's session dictionary.

  If it is the first time the user is logging into this application it will
  create the user and insert it into the database.  If the user is not logged
  in, None will be set to g.user.
  """

  # Set the user in the session dictionary as a global g.user and bail out
  # of this function early.
  g.first_time = False
  g.user = None
  if session.get('user'):
    g.user = session.get('user')
    return


  # Attempt to get the short term access token for the current user.
  result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                app_secret=FB_APP_SECRET)

  # If there is no result, we assume the user is not logged in.
  if result:
    # Check to see if this user is already in our database.
    user = models.User.query.filter(models.User.id == result['uid']).first()

    if not user:
      # Not an existing user so get info
      graph = GraphAPI(result['access_token'])
      profile = graph.get_object('me')

      # Create the user and insert it into the database
      user = models.User(id=str(profile['id']), name=profile['name'],
                  profile_url=profile['link'],
                  access_token=result['access_token'])
      db.session.add(user)
      g.first_time = True
    elif user.access_token != result['access_token']:
      # If an existing user, update the access token
      user.access_token = result['access_token']

    # Add the user to the current session
    g.user = user
    session['user'] = dict(name=user.name, profile_url=user.profile_url,
                           id=user.id, access_token=user.access_token,
                           email=user.email, phone_number=user.phone_number)

  # Commit changes to the database and set the user as a global g.user
  db.session.commit()
  #g.user = session.get('user', None)
