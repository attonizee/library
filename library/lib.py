from flask import Blueprint, render_template, redirect, request, url_for, flash
from .database import Books, Author, db, book_author
from .forms import Add_Book


bp = Blueprint('lib', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('lib/index.html')

@bp.route('/books')
def books():
    books_list = Books.query.all()
    return render_template('lib/books.html', books=books_list)

   

@bp.route('/add_book', methods=('GET', 'POST'))
def add_book():
    form = Add_Book()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        new_book = Books(name=form.book_name.data)
        new_author = Author(name=form.author_name.data)
        author = Author.query.filter_by(name=new_author.name).first()
        book = Books.query.filter_by(name=new_book.name).first()
                 
        if author is not None:
           
            if book is not None:
                author.book_author.append(book)
                error = f'Book {book.name} connected to author {author.name}'
            else:
                db.session.add(new_book)
                author.books_author.append(new_book)
                error = f'Book {new_book.name} connected to author {author.name}'
            
            db.session.commit()
            
           
        elif book is not None:
            
            db.session.add(new_author)
            new_author.books_author.append(book)
            db.session.commit()
            error = f'Book {book.name} connected with author {new_author.name}'
            
        else:
            db.session.add(new_book)
            db.session.add(new_author)
            new_author.books_author.append(new_book)
            db.session.commit()
            error = f'Book {new_book.name} wroted by {new_author.name} added'
                            
        flash(error)
        
    return render_template('lib/addbook.html', form=form)
