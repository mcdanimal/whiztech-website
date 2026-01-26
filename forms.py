from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

class ServiceRequestForm(FlaskForm):
    customer_lname = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    customer_fname = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    customer_email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Invalid format for email address")
    ])

    service_type = SelectField('Service', choices=[
        ('repair', 'Hardware Repair'),
        ('software', 'Software Installation'),
        ('consultation', 'Consultation'),
        ('other', 'Other')
    ])

    details = TextAreaField('Details', validators=[
        DataRequired(),
        Length(min=25, max=2500)
    ])