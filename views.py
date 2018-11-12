from flask import Flask, render_template, redirect, request

from models import User, Article

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
    articles = Article.query.all()
    return render_template('index.html', articles=articles)


# RESTful routes
@app.route('/articles')
def articles():
    """
    Returns all articles.
    """
    articles = Article.query.all()
    return render_template('articles/list.html', articles=articles)


@app.route('/articles', methods=['POST'])
def article_new():
    """
    Creates a new article and redirects user to it.
    """
    article = Article(title=request.form.get('title'), content=request.form.get('content'))
    db.session.add(article)
    db.session.commit(article)

    return redirect(f'/articles/{article.id}')


@app.route('/articles/<int:article_id>')
def article_detail(article_id):
    """
    Returns a specific article.

    The route variable `article_id` must be passed to the view function as an argument.
    Their names are arbitrary, but they must match.
    """
    article = Article.query.get(article_id)
    return render_template('articles/detail.html', article=article)


@app.route('/articles/<int:article_id>/edit')
def article_edit(article_id):
    """
    Renders the article's edit page.

    The full article content is returned so that the user can view the old and make updates to it.
    """
    article = Article.query.get(article_id)
    return render_template('articles/edit.html', article=article)


@app.route('/articles/<int:article_id>', methods=['POST'])
def article_update(article_id):
    """
    Updates the current article and redirects the user to it.
    """
    article = Article.query.get(article_id)
    new_title = request.form.get('title')
    new_content = request.form.get('content')

    if article.title != new_title:
        article.title = new_title
    if article.content != new_content:
        article.content = new_content

    db.session.add(article)
    db.session.commit()

    return redirect(f'/articles/{article_id}')


@app.route('/articles/<int:article_id>/delete')
def article_delete(article_id):
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()

    return redirect('/')
