from flask import Blueprint, current_app, render_template, request
from blogwise.models import Article

home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/')
def index():
    """Home page. """
    current_app.logger.info("Home page loaded.")
    articles = Article.query.order_by(Article.modified.desc()).all()
    return render_template('index.html', articles=articles)


@home_bp.route('/sandbox')
def health_check_form():
    articles = Article.query.all()
    return render_template('sandbox.html', articles=articles)


@home_bp.route('/sandbox', methods=['POST'])
def health_check():
    form = request.form.get('books')
    current_app.logger.info(form.split())

    return render_template('sandbox.html')
