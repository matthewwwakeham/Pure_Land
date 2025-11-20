from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, SignupForm, ResetPasswordRequestForm, ResetPasswordForm
from .models import User, db
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("main/index.html")

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Logged in successfully!", "success")
            return redirect(url_for("main.index"))
        
        flash("Invalid email or password.", "danger")
        
    return render_template("auth/login.html", form=form)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash("Account created successfully!", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/signup.html", form=form)

@auth.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # generate token and send email
            flash("Check your email for reset instructions.", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request.html", form=form)

@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()
    # validate token, get user
    if form.validate_on_submit():
        # user.set_password(form.password.data)
        # db.session.commit()
        flash("Your password has been reset.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))