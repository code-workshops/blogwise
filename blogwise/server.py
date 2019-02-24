import os

from blogwise import app_factory
from flask_debugtoolbar import DebugToolbarExtension

settings = os.getenv('FLASK_SETTINGS', 'blogwise.settings.dev')
app = app_factory(settings)

if __name__ == '__main__':
    if app.debug:
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        DebugToolbarExtension(app)
    app.run()
