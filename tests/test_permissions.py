from app import create_app
from app import db
from app.models import User, Recipe
from werkzeug.security import generate_password_hash


def test_user_cannot_edit_other_users_recipe():
    app = create_app()

    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

        user1 = User(
            name="User One",
            email="user1@example.com",
            password_hash=generate_password_hash("password123")
        )

        user2 = User(
            name="User Two",
            email="user2@example.com",
            password_hash=generate_password_hash("password123")
        )

        db.session.add_all([user1, user2])
        db.session.commit()

        recipe = Recipe(
            title="User One Recipe",
            short_description="Test recipe",
            full_recipe="Test recipe instructions",
            category="Dinner",
            prep_time=30,
            servings=2,
            author_id=user1.id
        )

        db.session.add(recipe)
        db.session.commit()

        client = app.test_client()

        response = client.post(
            "/auth/login",
            data={
                "email": "user2@example.com",
                "password": "password123"
            },
            follow_redirects=True
        )

        assert response.status_code == 200

        response = client.get(
            f"/recipes/{recipe.id}/edit"
        )

        assert response.status_code == 403