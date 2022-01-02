from flask import Blueprint, session, redirect, url_for, g, render_template

from model.db.alter_database import Retrieve, Insert

admin = Blueprint('admin', __name__, static_folder="static", template_folder="templates")

ret = Retrieve()
ins = Insert()


@admin.before_request
def before_request():
    if 'email' in session:
        users = ret.retrieve_users_by_email(session['email'])
        g.user = users[0]


@admin.route('/')
def home():
    if 'email' not in session:
        redirect(url_for('login_and_register.user_login'))

    user = g.user

    user_id = user.user_id
    first_name = user.first_name
    surname = user.surname

    session['user_id'] = user_id
    session['first_name'] = first_name
    session['surname'] = surname

    subjects = ret.retrieve_subjects()
    users = ret.retrieve_users()

    return render_template('admin.html', users=users, subjects=subjects)
