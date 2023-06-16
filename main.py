# Flas import
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash

# local import
from app import create_app

from app.forms import BookForm

from flask_sqlalchemy import SQLAlchemy

app = create_app()

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()


@app.route('/')
def index():
    context = {}
    return render_template('index.html', **context)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    book_form = BookForm()
    context = {
        'book_form': book_form
    }

    if book_form.validate_on_submit():
        message = 'Se agrego el libro {}'.format(book_form.name.data)
        flash(message)

        new_user = User(username='JohnDoe', email='john@example.com')
        db.session.add(new_user)
        db.session.commit()

        users = User.query.all()

        print(users)

    return render_template('book_add.html', **context)
