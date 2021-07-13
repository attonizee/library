from datetime import datetime
import click

from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(36), index=True, unique=True)
    user_password = db.Column(db.String(256))
    reg_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

    def generate_hash(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)

    def __repr__(self):
        return f'User {self.user_name} created {self.reg_date}'

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    lib = db.relationship('Book_author', backref='Books', lazy='dynamic')

    def __repr__(self):
        return f'The book {self.name} on ID {self.id}'

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    lib = db.relationship('Book_author', backref='Author', lazy='dynamic')

    def __repr__(self):
        return f'Author name {self.name} has ID {self.id}'

class Book_author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return f'The book {self.book_id} wroted by {self.author_id}'

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    click.echo('Initialized the database.')

