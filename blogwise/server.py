from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from blogwise.views import articles, auth, index, users
from blogwise.models import connect_to_db

app = Flask(__name__)
app.register_blueprint(articles)
app.register_blueprint(auth)
app.register_blueprint(index)
app.register_blueprint(users)

if __name__ == '__main__':
	app.secret_key = 'secretzzzzzz'
	app.debug = False
	app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
	connect_to_db(app)

	DebugToolbarExtension(app)
	app.run()
