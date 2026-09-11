from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    TextAreaField,
    SelectField
)

class RegistrationForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")
from wtforms import IntegerField, TextAreaField
class RecipeForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired()]
    )

    short_description = StringField(
        "Short Description",
        validators=[DataRequired()]
    )

    full_recipe = TextAreaField(
        "Recipe",
        validators=[DataRequired()]
    )

    category = SelectField(
    "Category",
    choices=[
    ("Breakfast", "Breakfast"),
    ("Lunch", "Lunch"),
    ("Dinner", "Dinner"),
    ("Dessert", "Dessert"),
    ("Vegan", "Vegan"),
    ("Vegetarian", "Vegetarian"),
    ("Other", "Other")
    ],
    validators=[DataRequired()]
    )

    prep_time = IntegerField(
        "Preparation Time (minutes)",
        validators=[DataRequired()]
    )

    servings = IntegerField(
        "Servings",
        validators=[DataRequired()]
    )

    submit = SubmitField("Add Recipe")
class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
class ProfileForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    profile_image = StringField(
        "Profile Image URL"
    )

    submit = SubmitField("Save Changes")