from datetime import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    recipes = db.relationship("Recipe", backref="author", lazy=True)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    short_description = db.Column(db.String(300), nullable=False)
    full_recipe = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )