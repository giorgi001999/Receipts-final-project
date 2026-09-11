from app import create_app
from app import db
from app.models import User
from werkzeug.security import generate_password_hash


def test_login():
    app = create_app()

    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(
            name="Test User",
            email="test@example.com",
            password_hash=generate_password_hash("password123")
        )

        db.session.add(user)
        db.session.commit()

        client = app.test_client()

        response = client.post(
            "/auth/login",
            data={
                "email": "test@example.com",
                "password": "password123"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Hello, Test User!" in response.data