from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request,
                   session)
from blogwise.models import User

user_bp = Blueprint('users', __name__, template_folder='templates/users')


@user_bp.route('/user/<int:user_id>')
def user_profile(user_id):
    if not session.get('user_id'):
        flash('You must log in to view profiles.', 'info')
        return redirect('/login')
    else:
        user = User.query.get(user_id)
        return render_template('users/profile.html', user=user)


@user_bp.route('/user/<int:user_id>/edit')
def user_edit_template(user_id):
    if session.get('user_id') == user_id:
        user = User.query.get(user_id)
        return render_template('users/edit.html', user=user)


@user_bp.route('/user/<int:user_id>', methods=['POST'])
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


@user_bp.route('/user/<int:user_id>/change-password')
def user_change_pw_template(user_id):
    if session.get('user_id') == user_id:
        user = User.query.get(user_id)
        return render_template('users/change_password.html', user=user)


@user_bp.route('/user/<int:user_id>/change-password', methods=['POST'])
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
