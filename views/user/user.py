from urllib import request

from flask import Blueprint, session, g, render_template, redirect, url_for, request, flash

from model.db.alter_database import Retrieve, Insert, Delete, Modify

user = Blueprint('user', __name__, static_folder="static", template_folder="templates")

ret = Retrieve()
ins = Insert()
mod = Modify()
dlt = Delete()


@user.before_request
def before_request():
    if 'email' in session:
        users = ret.retrieve_users_by_email(session['email'])
        g.user = users[0]


@user.route('/subjects/', methods=["GET", "POST"])
def subjects():
    if 'email' not in session:
        return redirect(url_for('login_and_register.login'))

    user_id = g.user.user_id
    first_name = g.user.first_name
    surname = g.user.surname

    session['first_name'] = first_name
    session['surname'] = surname

    user_subjects = ret.retrieve_user_subjects(user_id)

    if request.method == 'POST':
        query = request.form.get('search-query')

        # User can reset search by sending an empty query
        if len(query) == 0:
            return render_template('user_subjects.html', subjects=user_subjects)

        try:
            results = ret.search_user_subjects(user_id, query)

            if len(results) == 0:
                flash("No search results found")  # Deliveres a message to the user if no matching values was found
                return render_template('user_subjects.html', subjects=user_subjects)

            user_subjects = results
        except TypeError as e:
            flash(str(e))
        except ValueError as e:
            flash(str(e))

    return render_template('user_subjects.html', subjects=user_subjects)


@user.route('/subjects/add/', methods=['GET', 'POST'])
def user_add_subject():
    if 'email' not in session:
        return redirect(url_for('login_and_register.login'))

    user_id = g.user.user_id

    subjects = ret.retrieve_subjects()
    grades = ret.retrieve_grades()

    if request.method == "POST":
        try:
            subject_id = int(request.form.get('subject-select'))
            grade_id = int(request.form.get('grade-select'))
            subject = next(filter(lambda subject: subject.subject_id == subject_id, subjects))

            if ins.insert_link(user_id=user_id, subject_id=subject_id, grade_id=grade_id):
                flash(f"Added {subject.subject_code} {subject.subject_name}")
                return redirect(url_for('user.user_add_subject'))
            else:

                flash(f"{subject.subject_code} {subject.subject_name} has already been added to your database.")
                return render_template('user_add_subject.html', subjects=subjects, grades=grades)
        except TypeError as e:
            flash(str(e))
            return render_template('user_add_subject.html', subjects=subjects, grades=grades)
        except ValueError as e:
            flash(str(e))
            return render_template('user_add_subject.html', subjects=subjects, grades=grades)

    return render_template('user_add_subject.html', subjects=subjects, grades=grades)


@user.route('/subjects/edit/<subject_id>/', methods=["GET", "POST"])
def user_edit_subject(subject_id=None):
    if 'email' not in session:
        return redirect(url_for('login_and_register.login'))

    subject_id = int(subject_id)
    subject = next(filter(lambda subject: subject.subject_id == subject_id, ret.retrieve_subjects()))
    grades = ret.retrieve_grades()

    if request.method == 'POST':
        grade_id = request.form.get('select-grade')
        grade_id = int(grade_id)  # Converts grade ID to an int
        user_id = g.user.user_id

        try:
            if mod.user_modify_subject(user_id, subject_id, grade_id):
                flash(f"Edited grade for {subject.subject_code} {subject.subject_name}")
                return redirect(url_for('user.subjects'))
            else:
                flash("Failed to edit subject")
                return redirect(url_for('user.user_edit_subject', subject_id=subject_id))
        except TypeError as e:
            flash(str(e))
            return redirect(url_for('user.user_edit_subject', subject_id=subject_id))
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('user.user_edit_subject', subject_id=subject_id))

    return render_template('user_edit_subject.html', subject=subject, grades=grades)


@user.route('/subjects/delete/<subject_id>/')
def user_delete_subject(subject_id=None):
    if 'email' not in session:
        return redirect(url_for('login_and_register.login'))

    subject_id = int(subject_id)
    user_id = g.user.user_id

    subject = next(filter(lambda subject: subject.subject_id == subject_id, ret.retrieve_subjects()))

    try:
        if dlt.user_delete_subject(user_id, subject_id):
            flash(f"{subject.subject_code} {subject.subject_name} was removed from your database.")
        else:
            flash(f"Could not remove {subject.subject_code} {subject.subject_name}.")
    except TypeError as e:
        flash(str(e))
    except ValueError as e:
        flash(str(e))

    return redirect(url_for('user.subjects'))


@user.route('/profile/')
def profile():
    if 'email' not in session:
        return redirect(url_for('login_and_register.login'))

    return render_template('profile.html')
