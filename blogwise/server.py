import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from blogwise.views import articles, auth, index, users
from blogwise.models import connect_to_db
from blogwise.settings import dev

settings = os.getenv('BLOGWISE_SETTINGS', dev)

app = Flask(__name__)
app.register_blueprint(articles.article_bp)
app.register_blueprint(auth.auth_bp)
app.register_blueprint(index.home_bp)
app.register_blueprint(users.user_bp)

if __name__ == '__main__':
    app.secret_key = settings.SECRET_KEY
    app.debug = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)

    DebugToolbarExtension(app)
    app.run()
