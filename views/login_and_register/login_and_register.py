from datetime import datetime

from flask import Blueprint, session, render_template, request, flash, g, redirect, url_for
from jinja2 import Markup

from model.db.alter_database import Retrieve, Insert
from model.validation_classes import User

login_and_register = Blueprint('login_and_register', __name__, static_folder="static", template_folder="templates")

ret = Retrieve()
ins = Insert()


@login_and_register.route("/login/", methods=["GET", "POST"])
def user_login():
    if 'email' in session:
        session.pop('email', None)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get("password")

        try:
            users = ret.retrieve_users_by_email(email)
        except TypeError as e:
            flash(str(e))
            return render_template('login.html')
        except ValueError as e:
            flash(str(e))
            return render_template('login.html')
        if len(users) == 0:
            flash('Could not find a matching e-mail in our database.')
            return render_template('login.html')
        else:
            user = users[0]

            if user.email == email and user.password == password:
                session['email'] = email
                g.user = user

                flash("Logged in")
                return render_template('login.html')
            else:
                flash("Incorrect password")
                return render_template('login.html')
    else:
        return render_template('login.html')


@login_and_register.route("/register/", methods=["GET", "POST"])
def user_register():
    if 'email' in session:
        session.pop('email', None)

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        surname = request.form.get('surname')
        dob = request.form.get('dob')

        year, month, day = dob.split('-')
        dob = datetime(int(year), int(month), int(day)) # Converting dob-string to a datetime object

        email = request.form.get('email')
        password = request.form.get('password')

        try:
            if ins.insert_user(first_name, surname, dob, email, password):
                flash("Registered user!")
                return redirect(url_for('login_and_register.user_login'))
            else:
                # This does not work properly
                flash(Markup(
                    "There is already an account affiliated with this e-mail. "
                    "Click <a href=\"{{url_for('login_and_register.user_login')}}\">here</a> to log in, "
                    "or try another e-mail."
                ))
                return render_template('register.html')
        except TypeError as e:
            flash(str(e))
            return render_template('register.html')
        except ValueError as e:
            flash(str(e))
            return render_template('register.html')

    else:
        return render_template('register.html')
