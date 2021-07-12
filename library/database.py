from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

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