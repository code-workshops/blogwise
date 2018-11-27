import datetime as dt

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User {self.id} | {self.name}>"

    def save(self):
        """A method to make saving users simpler."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def create_password(self, password):
        self.password = generate_password_hash(password)

    def is_valid_password(self, password):
        return check_password_hash(self.password, password)

    def change_password(self, old, new):
        if self.is_valid_password(old):
            self.create_password(new)
            self.save()


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    # Timestamp Articles when they're created.
    created = db.Column(db.DateTime, default=dt.datetime.utcnow)
    # Track the last time it was updated (edited by the user)
    modified = db.Column(db.DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    author = db.relationship('User', backref='articles', lazy=True)

    def __repr__(self):
        return f"<Article {self.id} | {self.title[:10]} ... by {self.author.name}>"

    def save(self):
        """A method to make saving articles simpler."""
        db.session.add(self)
        db.session.commit()


def connect_to_db(app):
    """Helper function to configure the database with the flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogwise'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    # An application context is required to connect to the database!
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    # Create tables ...
    db.create_all()
    print('Connected to database.')
