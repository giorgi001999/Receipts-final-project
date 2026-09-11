from flask import Blueprint, render_template, redirect, url_for, current_app

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, logout_user, current_user

from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user:
            form.email.errors.append(
                "Email is already registered."
            )
            return render_template(
                "auth/register.html",
                form=form
            )

        password_hash = generate_password_hash(
            form.password.data
        )

        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        current_app.logger.info(
            "New user registered: %s",
            user.email
        )

        return redirect(url_for("main.home"))

    return render_template(
        "auth/register.html",
        form=form
    )


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password_hash,
            form.password.data
        ):
            login_user(user)

            current_app.logger.info(
                "User logged in: %s",
                user.email
            )

            return redirect(url_for("main.home"))

        current_app.logger.warning(
            "Failed login attempt: %s",
            form.email.data
        )

        form.email.errors.append(
            "Invalid email or password."
        )

    return render_template(
        "auth/login.html",
        form=form
    )


@auth.route("/logout")
def logout():

    if current_user.is_authenticated:
        current_app.logger.info(
            "User logged out: %s",
            current_user.email
        )

    logout_user()

    return redirect(url_for("main.home"))