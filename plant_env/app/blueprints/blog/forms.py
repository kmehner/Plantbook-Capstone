from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    image = FileField('Post Image')
    submit = SubmitField('Create')


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class PlantForm(FlaskForm):
    common_name = StringField('Common Name', validators=[DataRequired()])
    scientific_name = StringField('Scientific Name')
    content = StringField('Content')
    image = FileField('Plant Image')
    submit = SubmitField('Create')
