from datetime import datetime

# Flas import
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash

# local import
from app import create_app

from app.forms import BookForm, AuthorForm, DeleteBookForm, DeleteAuthorForm

from flask_sqlalchemy import SQLAlchemy

app = create_app()

db = SQLAlchemy(app)


# region Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# endregion Models

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()


@app.route('/')
def index():
    books = Book.query.all()
    delete_form = DeleteBookForm()
    context = {
        'books': books,
        'delete_form': delete_form
    }

    return render_template('index.html', **context)

# region Book views
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    book_form = BookForm()
    book_form.author_id.choices = [(author.id, author.name) for author in Author.query.all()]
    context = {
        'book_form': book_form
    }

    if book_form.validate_on_submit():
        new_book = Book(title=book_form.title.data, author_id=book_form.author_id.data)
        db.session.add(new_book)
        db.session.commit()

        books = Book.query.all()

        print(books)

        message = 'Se agrego el libro {}'.format(book_form.title.data)
        flash(message)
        return redirect(url_for('index'))

    return render_template('book_add.html', **context)


@app.route('/update/<book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book_instance = Book.query.get(book_id)
    book_form = BookForm(obj=book_instance)
    book_form.author_id.choices = [(author.id, author.name) for author in Author.query.all()]
    context = {
        'book_form': book_form,
        'book': book_instance,
        'selected_author_id': book_instance.author_id
    }

    if book_form.validate_on_submit():
        book_form.populate_obj(book_instance)  # Actualiza los datos del registro con los datos del formulario
        db.session.commit()  # Guarda los cambios en la base de datos
        flash('Registro actualizado correctamente', 'success')
        return redirect(url_for('index'))
    return render_template('book_update.html', **context)


@app.route('/delete/<book_id>', methods=['POST'])
def delete_book(book_id):
    book_instance = Book.query.get(book_id)

    if not book_instance:
        flash('Libro no encontrado', 'error')
        return redirect(url_for('index'))
    
    db.session.delete(book_instance)
    db.session.commit()

    flash('Libro eliminado correctamente', 'success')
    return redirect(url_for('index'))


# endregion Book views

# region Authors views
@app.route('/author/list', methods=['GET'])
def list_author():
    authors = Author.query.all()
    delete_form = DeleteAuthorForm()
    context = {
        'authors': authors,
        'delete_form': delete_form
    }
    return render_template('author_list.html', **context)


@app.route('/author/add', methods=['GET', 'POST'])
def add_author():
    author_form = AuthorForm()
    context = {
        'author_form': author_form
    }

    if author_form.validate_on_submit():

        new_user = Author(name=author_form.name.data)
        db.session.add(new_user)
        db.session.commit()

        authors = Author.query.all()

        print(authors)

        message = 'Se agrego el Autor {}'.format(author_form.name.data)
        flash(message)
        return redirect(url_for('list_author'))

    return render_template('author_add.html', **context)


@app.route('/author/update/<author_id>', methods=['GET', 'POST'])
def update_author(author_id):
    author_instance = Author.query.get(author_id)
    author_form = AuthorForm(obj=author_instance)
    context = {
        'author_form': author_form,
        'author': author_instance,
    }

    if author_form.validate_on_submit():
        author_form.populate_obj(author_instance)  # Actualiza los datos del registro con los datos del formulario
        db.session.commit()  # Guarda los cambios en la base de datos
        flash('Registro actualizado correctamente', 'success')
        return redirect(url_for('list_author'))
    return render_template('author_add.html', **context)


@app.route('/author/delete/<author_id>', methods=['POST'])
def delete_author(author_id):
    author_instance = Author.query.get(author_id)
    if not author_instance:
        flash('Autor no encontrado', 'error')
        return redirect(url_for('author_list'))
    db.session.delete(author_instance)
    db.session.commit()
    flash('Autor eliminado correctamente', 'success')
    return redirect(url_for('list_author'))
# endregion Authors views
