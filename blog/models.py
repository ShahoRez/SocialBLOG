# models.py

from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from blog import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id == user_id)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    profile_image = db.Column(
        db.String(240), nullable=False,
        default="profile_image.png"
    )
    password_hash = db.Column(db.String(128))
    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class BlogPost(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
        )
    title = db.Column(db.String(160), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"BlogPost('{self.id}', '{self.title}', '{self.date}')"
