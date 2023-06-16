# Flask imports
from flask_wtf import FlaskForm

from wtforms.fields import IntegerField, StringField, DateField, SubmitField
from wtforms.validators import DataRequired


class DeleteBookForm(FlaskForm):
    submit = SubmitField('Borrar')


class DeleteAuthorForm(FlaskForm):
    submit = SubmitField('Borrar')


class AuthorForm(FlaskForm):
    name = StringField('Nombre del autor', validators=[DataRequired()])
    submit = SubmitField('Guardar')


class BookForm(FlaskForm):
    title = StringField('Título del libro', validators=[DataRequired()])
    author_id = IntegerField('ID del autor', validators=[DataRequired()])
    submit = SubmitField('Guardar')
