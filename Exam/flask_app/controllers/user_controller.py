from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.band import Band
@app.route("/")
def index():
    return render_template("index.html")

# REGISTRATION 
@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/")
    qt_hash = bcrypt.generate_password_hash(request.form["password"])
    query_data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : qt_hash
    }
    new_user_id = User.register_user(query_data)
    session['user_id'] = new_user_id
    return redirect("/dashboard")

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    if not User.validate_login(request.form):
        return redirect("/")
    logged_user = User.get_by_email(request.form)
    session['user_id'] = logged_user.id
    return redirect("/dashboard")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        flash("You need to login in order to continue!")
        return redirect("/")
    query_data = {
        "user_id" : session["user_id"]
    }
    user = User.get_by_id(query_data)
    all_bands = Band.get_all_bands()
    return render_template("dashboard.html", user = user, all_bands = all_bands)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
# -------------------------------------------