from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request,
                   session)
from blogwise.models import Article, Comment

article_bp = Blueprint('articles', __name__, template_folder='templates/articles')


@article_bp.route('/articles')
def articles():
    """
    Returns all articles.
    """
    articles = Article.query.order_by(Article.created).all()
    current_app.logger.info('\t Rendering all articles ...')
    return render_template('articles/list.html', articles=articles)


@article_bp.route('/article/new')
def article_new():
    """Render form to create a new article."""
    current_app.logger.info('\t Rendering new article template ...')
    return render_template('articles/new.html')


@article_bp.route('/articles', methods=['POST'])
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
        current_app.logger.info(f'Article {article.id} created.')
        flash('Your article has been saved.', 'success')
        return redirect(f'/articles/{article.id}')


@article_bp.route('/articles/<int:article_id>')
def article_detail(article_id):
    """
    Returns a specific article.

    The route variable `article_id` must be passed to the view function as an argument.
    Their names are arbitrary, but they must match.
    """
    article = Article.query.get(article_id)
    return render_template('articles/detail.html', article=article)


@article_bp.route('/articles/<int:article_id>/edit')
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


@article_bp.route('/articles/<int:article_id>', methods=['POST'])
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


@article_bp.route('/articles/<int:article_id>/delete')
def article_delete(article_id):
    article = Article.query.get(article_id)

    if session.get('user_id') == article.author_id:
        Article.query.delete(article_id)
        current_app.logger.info(f"Article {article_id} deleted.")

        flash('Your article was deleted successfully', 'success')

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
