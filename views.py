from flask import Flask, flash, render_template, redirect, request, session

from models import Article, User

app = Flask(__name__)


# Step 1: Get 1 route working for sanity check. See server.py for more step 1

@app.route('/')
def index():
    """
    This is a view pattern. Note:
    
    * Route decorator
    * View function (this function)
    """
    app.logger.info("Home page loaded.")
    articles = Article.query.order_by(Article.created).all()
    return render_template('index.html', articles=articles)


# ARTICLE ROUTES
@app.route('/articles')
def articles():
    """
    Returns all articles.
    """
    articles = Article.query.order_by(Article.created).all()
    return render_template('articles/list.html', articles=articles)


@app.route('/article/new')
def article_new():
    """Render form to create a new article."""
    return render_template('articles/new.html')


@app.route('/articles', methods=['POST'])
def article_create():
    """
    Creates a new article and redirects user to it.
    """
    article = Article(title=request.form.get('title'),
                      content=request.form.get('content'),
                      author_id=request.form.get('author_id'))
    article.save()

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

    article.save()

    return redirect(f'/articles/{article_id}')


@app.route('/articles/<int:article_id>/delete')
def article_delete(article_id):
    article = Article.query.get(article_id)
    article.save()
    # db.session.delete(article)
    # db.session.commit()

    return redirect('/')


# USER ROUTES


@app.route('/signup')
def signup_form():
    """Render signup form."""
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup():
    """Register new users!"""
    # TODO: Allow javascript to verify a match on the form!
    pword_conf = request.form.get('passwordConf')
    password = request.form.get('password')

    if password == pword_conf:
        user = User(name=request.form.get('name'),
                    email=request.form.get('email'),
                    password=password)
        user.save()
        app.logger.info('User signup successful!')
        session['user_id'] = user.id

        return redirect('/')
    else:
        app.logger.info("User signp failed!")
        flash("Passwords don't match!")

        return render_template('signup.html')


@app.route('/login')
def login_form():
    """Render login form."""
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Log the user in!"""
    user = User.query.filter_by(email=request.form.get('email'),
                             password=request.form.get('password')).first_or_404()
    session['user_id'] = user.id

    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')