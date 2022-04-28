from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title')
    body = StringField('Body')
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


class HealthForm(FlaskForm):
    title = StringField('Health Issue', validators=[DataRequired()])
    body = StringField('Note')
    image = FileField('Image')
    submit = SubmitField('Create')

class WaterForm(FlaskForm):
    water_quantity = IntegerField('Water Quantity', validators=[DataRequired()])
    water_measurement = SelectMultipleField('Water Measurement', choices=[
                                 'C++', 
                                 'Python', 
                                 'Plain Text',
                               ])
    frequency_int = IntegerField('Frequency', validators=[DataRequired()])
    frequency_measurement = SelectMultipleField('Frequency Measurement', validators=[DataRequired()], choices=[
                                 ('cpp', 'C++'), 
                                 ('py', 'Python'), 
                                 ('text', 'Plain Text')
                               ])
    submit = SubmitField('Create')


class PhotoForm(FlaskForm):
    body = StringField('Note')
    image = FileField('Image')
    submit = SubmitField('Create')