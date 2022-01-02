from flask import Blueprint, session, redirect, url_for, g, render_template, flash, request

from model.db.alter_database import Retrieve, Insert

admin = Blueprint('admin', __name__, static_folder="static", template_folder="templates")

ret = Retrieve()
ins = Insert()


@admin.before_request
def before_request():
    if 'email' in session:
        users = ret.retrieve_users_by_email(session['email'])
        g.user = users[0]


@admin.route('/subjects', methods=['GET', 'POST'])
def admin_subjects():
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

    if request.method == 'POST':
        query = request.form.get('search-query')

        # User can reset search by sending an empty query
        if len(query) == 0:
            return render_template('subjects.html', subjects=subjects)

        try:
            results = ret.search_subjects(query)

            if len(results) == 0:
                flash("No search results found")  # Deliveres a message to the user if no matching values was found
                return render_template('subjects.html', subjects=subjects)

            subjects = results
        except TypeError as e:
            flash(str(e))
        except ValueError as e:
            flash(str(e))

    return render_template('subjects.html', subjects=subjects)


@admin.route('/users')
def users():
    if 'email' not in session:
        redirect(url_for('login_and_register.user_login'))

    user = g.user

    user_id = user.user_id
    first_name = user.first_name
    surname = user.surname

    session['user_id'] = user_id
    session['first_name'] = first_name
    session['surname'] = surname

    users = ret.retrieve_users()

    return render_template('users.html', users=users)
