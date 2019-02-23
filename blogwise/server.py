import os
# from flask import Flask
from blogwise import app_factory
from flask_debugtoolbar import DebugToolbarExtension

# from blogwise.views import articles, auth, index, users
# from blogwise.models import connect_to_db
# from blogwise.settings import dev

# app = Flask(__name__)
# app.register_blueprint(articles.article_bp)
# app.register_blueprint(auth.auth_bp)
# app.register_blueprint(index.home_bp)
# app.register_blueprint(users.user_bp)


if __name__ == '__main__':
    settings = os.getenv('FLASK_SETTINGS', 'blogwise.settings.dev')
    app = app_factory(settings)
    if app.debug:
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        DebugToolbarExtension(app)
    app.run()
