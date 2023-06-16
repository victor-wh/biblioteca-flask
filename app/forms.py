# Flask imports
from flask_wtf import FlaskForm

from wtforms.fields import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired()])
    color = StringField('Color portada', validators=[DataRequired()])
    release_date = DateField('Fecha de publicacion', validators=[DataRequired()])
    submit = SubmitField('Enviar')



