from datetime import datetime
import click

from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()

class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(36), nullable=False, unique=True)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(36), index=True, unique=True, nullable=False)
    user_password = db.Column(db.String(256), nullable=False)
    reg_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    group_id = db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))

    def generate_hash(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)

    def __repr__(self):
        return self.user_name

book_author = db.Table('book_author', 
    db.Column('books_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    
    def __repr__(self):
        return f'The book {self.name} on ID {self.id}'

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    books_author = db.relationship('Books', secondary=book_author, lazy='subquery',
        backref=db.backref('Author', lazy=True))

    def __repr__(self):
        return f'Author name {self.name} has ID {self.id}'

class Copy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_number = db.Column(db.Integer, unique=True, nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    book_id = db.Column('book_id', db.Integer, db.ForeignKey('books.id'))

class Passing_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_date = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    copy_id = db.Column('copy_id', db.Integer, db.ForeignKey('copy.id'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

