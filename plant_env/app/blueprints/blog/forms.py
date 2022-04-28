from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField, SelectField
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
    water_measurement = SelectField('Water Measurement', choices=[
                                 ('cpp', 'C++'), 
                                 ('py', 'Python'), 
                                 ('text', 'Plain Text')
                               ])
    frequency_int = IntegerField('Frequency', validators=[DataRequired()])
    frequency_measurement = SelectField('Frequency Measurement', validators=[DataRequired()], choices=[
                                 ('C++', 'C++'), 
                                 ('Python', 'Python'), 
                                 ('Plain Text', 'Plain Text')
                               ])
    submit = SubmitField('Create')


class PhotoForm(FlaskForm):
    body = StringField('Note')
    image = FileField('Image')
    submit = SubmitField('Create')