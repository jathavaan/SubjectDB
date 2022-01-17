from flask import Blueprint, session, redirect, url_for, g, render_template, flash, request

from model.db.alter_database import Retrieve, Insert, Modify, Delete

admin = Blueprint('admin', __name__, static_folder="static", template_folder="templates")

ret = Retrieve()
ins = Insert()
mod = Modify()
dlt = Delete()


@admin.before_request
def before_request():
    if 'email' in session:
        users = ret.retrieve_users_by_email(session['email'])
        g.user = users[0]


@admin.route('/subjects/', methods=['GET', 'POST'])
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


@admin.route('/subjects/add/', methods=["POST", "GET"])
def admin_add_subject():
    if 'email' not in session:
        redirect(url_for('login_and_register.user_login'))

    if request.method == 'POST':
        subject_code = request.form.get('add-subject-code').upper()
        subject_name = request.form.get('add-subject-name')
        credits = float(request.form.get('add-subject-credits'))

        try:
            if ins.insert_subject(subject_code, subject_name, credits):
                flash(f"Successfully added {subject_code} {subject_name} to database.")
            else:
                flash(f"Failed to add {subject_code} {subject_name}. The subject may have already been added.")
        except TypeError as e:
            flash(str(e))
            return redirect(url_for('admin.admin_subjects'))
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('admin.admin_subjects'))

        return redirect(url_for('admin.admin_subjects'))


@admin.route('/subjects/edit/<subject_id>/', methods=["POST", "GET"])
def admin_edit_subject(subject_id=None):
    if 'email' not in session:
        redirect(url_for('login_and_register.user_login'))

    if subject_id is None:
        return redirect(url_for('admin.subjects'))

    subject_id = int(subject_id)
    subject = next(filter(lambda sub: sub.subject_id == subject_id, ret.retrieve_subjects()))
    old_subject_code = subject.subject_code
    old_subject_name = subject.subject_name
    old_credits = None

    if subject.credits is None:
        old_credits = float(0)
    else:
        old_credits = subject.credits

    if request.method == 'POST':
        subject_code = request.form.get('subject_code').upper()
        subject_name = request.form.get('subject_name')
        credits = request.form.get('subject_credits')

        flash_credits = False  # Credits will always be updated. This variable decides whether the user gets a message
        # about the update

        if credits:
            credits = float(credits)  # Converting credits to float if the user user the credits input
            flash_credits = True
        else:
            if subject.credits is None:
                credits = float(0)
            else:
                credits = float(subject.credits)

        try:
            if len(subject_code) > 0 and len(subject_name) > 0:
                mod.admin_modify_subject(subject_id, subject_code=subject_code, subject_name=subject_name)
                flash(f"Changed {old_subject_code} {old_subject_name} to {subject_code} {subject_name}.")
            elif len(subject_code) > 0 and len(subject_name) == 0:
                mod.admin_modify_subject(subject_id, subject_code=subject_code)
                flash(
                    f"Changed {old_subject_code} {old_subject_name} to {subject_code} {old_subject_name}."
                )
            elif len(subject_code) == 0 and len(subject_name) > 0:
                mod.admin_modify_subject(subject_id, subject_name=subject_name)
                flash(f"Changed {old_subject_code} {old_subject_name} to {old_subject_code} {subject_name}.")

            if flash_credits:
                mod.admin_modify_subject(subject_id=subject_id, credits=credits)
                flash(f"Changed credits from {old_credits} to {credits}.")
            else:
                mod.admin_modify_subject(subject_id=subject_id, credits=credits)

                return redirect(url_for('admin.admin_subjects'))
        except TypeError as e:
            flash(str(e))
            return redirect(url_for('admin.admin_edit_subject', subject_id=subject.subject_id))
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('admin.admin_edit_subject', subject_id=subject.subject_id))

    return render_template('admin_edit_subject.html', subject=subject)


@admin.route('/subjects/delete/<subject_id>/')
def admin_delete_subject(subject_id=None):
    if 'email' not in session:
        redirect(url_for('login_and_register.user_login'))

    if subject_id is None:
        return redirect(url_for('admin.admin_subjects'))

    subject_id = int(subject_id)
    subject = next(filter(lambda sub: sub.subject_id == subject_id, ret.retrieve_subjects()))
    subject_code = subject.subject_code
    subject_name = subject.subject_name

    try:
        if dlt.delete_subject(subject_code):
            flash(f"{subject_code} {subject_name} has been deleted from the database")
        else:
            flash(f"Failed to delete {subject_code} {subject_name}")
    except TypeError as e:
        flash(str(e))
    except ValueError as e:
        flash(str(e))

    return redirect(url_for('admin.admin_subjects'))


@admin.route('/users/')
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
