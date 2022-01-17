from flask import Flask, session, redirect, url_for, flash

from model.db.database import init_db
from views.admin.admin import admin
from views.login_and_register.login_and_register import login_and_register
from views.user.user import user

app = Flask(__name__)

# Session setup
app.secret_key = 'trx0rua*TZU-tkm6ren'

# Registering blueprints
app.register_blueprint(login_and_register, url_prefix="/")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(user, url_prefix="/")


@app.route("/")
@app.route("/home/")
def home():
    return redirect(url_for('login_and_register.user_login'))


@app.route('/logout')
def logout():
    if 'email' in session:
        session.clear()
        flash('Logged out')

    return redirect(url_for('login_and_register.user_login'))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
