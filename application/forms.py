from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    """
    Search Form for hero
    """
    search_string = StringField(
        'Search',
        [DataRequired()],
        message=('Enter a valid input.')
    )

    fields = [('title', 'title'), ('author', 'authors')]
    search_field = SelectField("", fields=fields)
    submit = SubmitField('submit')
