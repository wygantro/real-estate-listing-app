# forms.py

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


# user registration
class RegistrationForm(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired()])
    occupation = SelectField(
        u'You are a?',
        choices=[('investor', 'Investor'), ('lender', 'Lender'), ('buyer', 'Buyer'), ('other', 'Other')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


# user login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


# user account info/update
class User_AccountForm(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    email_weekly = BooleanField('Email me weekly county listings')
    user_setting_option1 = BooleanField('Email me updates?')
    user_setting_option2 = BooleanField('Other user options?')
    submit = SubmitField('Save')


# user county access selection
class CountySelectionForm(FlaskForm):
    county_selection = BooleanField(validators=[DataRequired()])
    submit = SubmitField('Add/Remove')


# user payment selection
class PaymentSelectionForm(FlaskForm):
    payment_selection = SelectField(u'Select payment plan',
                                    choices=[('annual', 'Annual'), ('monthly', 'Monthly')], validators=[DataRequired()])
    payment_selection_submit = SubmitField('Select')


# user payments
class PaymentForm(FlaskForm):
    payment_info = StringField('Payment Info (type anything here)',
                               validators=[DataRequired()])
    payment_agreement = BooleanField(validators=[DataRequired()])
    submit_payment = SubmitField('Submit Payment')
