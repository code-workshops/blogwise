from flask import Flask, render_template, redirect

from models import db, Article

app = Flask(__name__)


@app.route('/')
def index():
    """
    This is a view pattern. Note:
    
    * Route decorator
    * View function (this function)
    """
    
    # Try to replace your print() statements with logs instead anywhere that you're testing the live server.
    app.logger.info("Home page loaded.")
    return render_template('index.html')
