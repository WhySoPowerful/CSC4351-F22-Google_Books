from flask import Blueprint, flash, request, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Users
import hashlib

auth = Blueprint("auth", __name__)

def getHashed(text):  # function to get hashed email/password as it is reapeatedly used
    salt = "ITSASECRET"  # salt for password security
    hashed = text + salt  # salt for password security, a random string will be added to password and hashed together below
    hashed = hashlib.md5(hashed.encode())  # encrypting with md5 hash, best for generating passwords for db
    hashed = hashed.hexdigest()  # converting to string
    return hashed  # gives hashed text back

@auth.route("/")
def landing():
    return render_template("landing.html")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        check_user = Users.query.filter(Users.username == username).first()
        if check_user:
            flash("User already exists")
            return render_template("login.html")

        new_user = Users(username, getHashed(password))
        new_user.insert()
        flash("Account created successfully")

        return render_template("login.html")
    

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter(Users.username == username).first()
        if user:
            if getHashed(password) == user.password:
                login_user(user)
                return redirect(url_for("main.index"))
            else:
                flash("Invalid password")
                return render_template("login.html")
        else:
            flash("User not found")
            return render_template("login.html")
                

@auth.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("auth.landing"))
