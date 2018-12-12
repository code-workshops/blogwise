from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request,
                   session)
from blogwise.models import User

auth_bp = Blueprint('auth', __name__, template_folder='templates')


# AUTH ROUTES
@auth_bp.route('/signup')
def signup_form():
    """Render signup form."""
    return render_template('signup.html')


@auth_bp.route('/signup', methods=['POST'])
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
        current_app.logger.info('User signup successful!')
        flash('Sign-up success! You are now logged in.', 'success')
        session['user_id'] = user.id

        return redirect('/')
    else:
        current_app.logger.info("User signup failed!")
        flash("Passwords don't match!", 'warning')

        return render_template('signup.html')


@auth_bp.route('/login')
def login_form():
    """Render login form."""
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
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


@auth_bp.route('/logout')
def logout():
    session.clear()

    return redirect('/')
