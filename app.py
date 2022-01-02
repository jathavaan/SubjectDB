from flask import Flask, render_template, session, redirect, url_for

from views.admin.admin import admin
from views.login_and_register.login_and_register import login_and_register

app = Flask(__name__)

# Session setup
app.secret_key = 'trx0rua*TZU-tkm6ren'

# Registering blueprints
app.register_blueprint(login_and_register, url_prefix="/")
app.register_blueprint(admin, url_prefix="/admin")

@app.route("/")
@app.route("/home/")
def home():
    if 'email' not in session:
        return redirect(url_for('login_and_register.user_login'))
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
