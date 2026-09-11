from flask import (
Blueprint,
render_template,
redirect,
url_for,
current_app
)

from flask_login import login_required, current_user

from app import db
from app.forms import ProfileForm
from app.models import User

profile = Blueprint("profile", __name__, url_prefix="/profile")

@profile.route("/", methods=["GET", "POST"])
@login_required
def profile_page():

 form = ProfileForm(obj=current_user)

 if form.validate_on_submit():

    existing_user = User.query.filter(
            User.email == form.email.data,
            User.id != current_user.id
        ).first()

    if existing_user:
        form.email.errors.append(
            "Email is already registered."
        )

        return render_template(
            "profile/profile.html",
            form=form
        )

    current_user.name = form.name.data
    current_user.email = form.email.data
    current_user.profile_image = form.profile_image.data

    db.session.commit()

    current_app.logger.info(
        "Profile updated by user: %s",
        current_user.email
    )

    return redirect(
        url_for("profile.profile_page")
    )

 return render_template(
"profile/profile.html",
form=form)

@profile.route("/<int:user_id>")
def public_profile(user_id):

    user = User.query.get_or_404(user_id)

    return render_template(
        "profile/public_profile.html",
        user=user)