# Step 1: Get the server working. Install dependencies with pip!
from flask_debugtoolbar import DebugToolbarExtension

from views import app
from models import connect_to_db


if __name__ == '__main__':
	app.secret_key = 'secretzzzzzz'
	app.debug = True
	app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
	connect_to_db(app)

	DebugToolbarExtension(app)
	app.run()
