from flask import Flask, render_template, redirect

app = Flask(__name__)


# Step 1: Get 1 route working for sanity check. See server.py for more step 1

@app.route('/')
def index():
    """
    This is a view pattern. Note:
    
    * Route decorator
    * View function (this function)
    """
    
    # Try to replace your print() statements with logs instead anywhere 
    # that you're testing the live server.
    app.logger.info("Home page loaded.")
    return render_template('index.html')
