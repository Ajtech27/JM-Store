from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField  
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError 
from market.model import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist! Please try a different username')

    def validate_email_address(self, email_address_to_check):
            email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
            if email_address:
                raise ValidationError('Email Address already exist! Please try a different email address')
    
    username = StringField('Username:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField('Email Address:', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
     username= StringField('Username', validators=[DataRequired()])
     password = PasswordField('Password', validators=[DataRequired()])
     submit = SubmitField('Login')

class PurchaseItemForm(FlaskForm):
     submit = SubmitField('Purchase Item!')

class SellItemForm(FlaskForm):
     submit = SubmitField('Sell Item!')