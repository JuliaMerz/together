from facebook import get_user_from_cookie, GraphAPI
from flask import render_template

from app import app

@app.route('/')
@app.route('/index')
def index():
  """
  If logged in, return main.html. Otherwise return signin.html
  """
  if g.user:
    if g.first_time:
      g.first_time = False
      return redirect(url_for(profile))
  else:
    return render_template('signin.html', app_id=FB_APP_ID, name=FB_APP_NAME)

@app.route('/profile')
def profile():
  """
  Use this to let people change emails and phone numbers
  """

  return render_template("profile.html")

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
  if session.get('user'):
    g.user = session.get('user')
    return

  # Attempt to get the short term access token for the current user.
  result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                app_secret=FB_APP_SECRET)

  # If there is no result, we assume the user is not logged in.
  if result:
    # Check to see if this user is already in our database.
    user = User.query.filter(User.id == result['uid']).first()

    if not user:
      # Not an existing user so get info
      graph = GraphAPI(result['access_token'])
      profile = graph.get_object('me')

      # Create the user and insert it into the database
      user = User(id=str(profile['id']), name=profile['name'],
                  profile_url=profile['link'],
                  access_token=result['access_token'])
      db.session.add(user)
      g.first_time = True
    elif user.access_token != result['access_token']:
      # If an existing user, update the access token
      user.access_token = result['access_token']

    # Add the user to the current session
    session['user'] = dict(name=user.name, profile_url=user.profile_url,
                           id=user.id, access_token=user.access_token)

  # Commit changes to the database and set the user as a global g.user
  db.session.commit()
  g.user = session.get('user', None)

