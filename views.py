from flask import Flask, flash, render_template, redirect, request, session

from models import Article, Comment, User

app = Flask(__name__)


@app.route('/')
def index():
    """Home page. """
    app.logger.info("Home page loaded.")
    articles = Article.query.order_by(Article.modified.desc()).all()
    return render_template('index.html', articles=articles)


# ARTICLE ROUTES
@app.route('/articles')
def articles():
    """
    Returns all articles.
    """
    articles = Article.query.order_by(Article.created).all()
    app.logger.info('\t Rendering all articles ...')
    return render_template('articles/list.html', articles=articles)


@app.route('/article/new')
def article_new():
    """Render form to create a new article."""
    app.logger.info('\t Rendering new article template ...')
    return render_template('articles/new.html')


@app.route('/articles', methods=['POST'])
def article_create():
    """
    Creates a new article and redirects user to it.
    """
    if not session.get('user_id'):
        flash('You must be logged in to create a new article.', 'info')
        return redirect('/login')
    else:
        article = Article(title=request.form.get('title'),
                          content=request.form.get('content'),
                          author_id=request.form.get('author_id'))
        article.save()
        app.logger.info(f'Article {article.id} created.')
        flash('Your article has been saved.', 'success')
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
    if session.get('user_id') != article_id:
        flash('You do not have permission to edit this article.', 'warning')
        return redirect(f'articles/{article_id}')

    article = Article.query.get(article_id)
    return render_template('articles/edit.html', article=article)


@app.route('/articles/<int:article_id>', methods=['POST'])
def article_update(article_id):
    """
    Updates the current article and redirects the user to it.
    """
    if not session.get('user_id'):
        flash('You must be logged in to update your article.', 'warning')
        return redirect('/login')
    else:
        article = Article.query.get(article_id)
        if not session.get('user_id') == article.author_id:
            flash('You do not have permission to edit this article.', 'danger')
            return redirect(f'/articles/{article_id}')

        new_title = request.form.get('title')
        new_content = request.form.get('content')

        if article.title != new_title:
            article.title = new_title
        if article.content != new_content:
            article.content = new_content

        article.save()

        flash('Article update success!', 'success')
        return redirect(f'/articles/{article_id}')


@app.route('/articles/<int:article_id>/delete')
def article_delete(article_id):
    article = Article.query.get(article_id)

    if session.get('user_id') == article.author_id:
        Article.query.delete(article_id)
        app.logger.info(f"Article {article_id} deleted.")

        flash('Your article was deleted successfully', 'success')

    return redirect('/')


# AUTH ROUTES
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
                    email=request.form.get('email'))
        user.create_password(password)
        user.save()
        app.logger.info('User signup successful!')
        flash('Sign-up success! You are now logged in.', 'success')
        session['user_id'] = user.id

        return redirect('/')
    else:
        app.logger.info("User signup failed!")
        flash("Passwords don't match!", 'warning')

        return render_template('signup.html')


@app.route('/login')
def login_form():
    """Render login form."""
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Log the user in!"""
    user = User.query.filter_by(email=request.form.get('email')).first_or_404()
    if user.is_valid_password(request.form.get('password')):
        session['user_id'] = user.id
        flash('Login success!', 'success')
        return redirect('/')
    else:
        flash('Invalid password. Try again.', 'danger')
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')


# USER ROUTES
@app.route('/user/<int:user_id>')
def user_profile(user_id):
    if not session.get('user_id'):
        flash('You must log in to view profiles.', 'info')
        return redirect('/login')
    else:
        user = User.query.get(user_id)
        return render_template('users/profile.html', user=user)


@app.route('/user/<int:user_id>/edit')
def user_edit_template(user_id):
    if session.get('user_id') == user_id:
        user = User.query.get(user_id)
        return render_template('users/edit.html', user=user)


@app.route('/user/<int:user_id>', methods=['POST'])
def user_edit(user_id):
    if session.get('user_id') == user_id:
        user = User.query.get(user_id)
        user.email = request.form.get('email')
        user.name = request.form.get('name')
        user.save()
        flash('Your profile has been updated.', 'success')
        return redirect(f'/user/{user_id}')
    else:
        flash('You do not have permission to edit this profile.', 'warning')
        return redirect('/')


@app.route('/user/<int:user_id>/change-password')
def user_change_pw_template(user_id):
    if session.get('user_id') == user_id:
        user = User.query.get(user_id)
        return render_template('users/change_password.html', user=user)


@app.route('/user/<int:user_id>/change-password', methods=['POST'])
def user_change_pw(user_id):
    if session.get('user_id') == user_id:
        user = User.query.get(user_id)
        old_pw = request.form.get('currentPassword')
        new_pw = request.form.get('newPassword')
        pw_conf = request.form.get('passwordConf')

        if new_pw == pw_conf:
            user.change_password(old_pw, new_pw)

        flash('Your password has been changed successfully.', 'success')
        return redirect(f'user/{user_id}')
    else:
        flash('Your password was not changed.', 'warning')
        return redirect('/')


# COMMENT ROUTES
@app.route('/articles/<int:article_id>/comments', methods=['POST'])
def comment_create(article_id):
    user_id = session.get('user_id')
    if user_id:
        article = Article.query.get(article_id)
        comment = Comment(user_id=user_id,
                          body=request.form.get('body'))
        comment.save()
        article.comments.append(comment)
        article.save()

        # Confirm that the *comment* has been properly updated.
        app.logger.info('Comment {comment.id} for article {comment.article} created.')
        return redirect(f'articles/{article_id}')

    flash('You must login to leave a comment.')
    return redirect(f'article/{article_id}')


@app.route('/health-check')
def health_check_form():
    return render_template('testing.html')


@app.route('/health-check', methods=['POST'])
def health_check():
    form = request.form.get('books')
    app.logger.info(form.split())

    return render_template('testing.html')