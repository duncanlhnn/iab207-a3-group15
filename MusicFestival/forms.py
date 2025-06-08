from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    SelectField, DateField, TimeField, FloatField, IntegerField
)
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    title = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    date = DateField('Event Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    ticket_price = FloatField('Ticket Price (AUD)', validators=[DataRequired()])
    ticket_amount = IntegerField('Total Tickets Available', validators=[DataRequired()])
    status = SelectField('Event Status', choices=[
        ('open', 'Open'),
        ('inactive', 'Inactive'),
        ('soldout', 'Sold Out'),
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    artist_info = TextAreaField('Artist & Genre Information')
    image = FileField('Upload Event Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Create/Update Event')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Post Comment')

class BookingForm(FlaskForm):
    quantity = IntegerField('Number of Tickets', validators=[DataRequired()])
    submit = SubmitField('Confirm Booking')



