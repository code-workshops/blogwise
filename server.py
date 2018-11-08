# Step 1: Get the server working. Install dependencies with pip!
from flask_debugtoolbar import DebugToolbarExtension

from views import app

if __name__ == '__main__':
	app.secret_key = 'secretzzzzzz'
	app.debug = True

	DebugToolbarExtension(app)
	app.run()
