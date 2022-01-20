from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from app.models import users


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(message="Enter your username")])
    password = PasswordField('Password', validators=[
                             InputRequired(message="Enter your password")])
    submit = SubmitField('Login')

    def validate_username(self, field):
        if field.data not in [x.id for x in users]:
            raise ValidationError('Unknown username')


class RegisterForm(FlaskForm):
    first_name = StringField('First name',
                             validators=[InputRequired(message="Enter your first name"),
                                         Length(min=3, message="First name must be a least 3 characters long")])

    last_name = StringField('Last name',
                            validators=[InputRequired(message="Enter your last name"),
                                        Length(min=3, message="Last name must be a least 3 characters long")])

    birth = DateField('Birth date',
                      validators=[InputRequired(message="Enter a date like this dd/mm/yyyy")])

    username = StringField('Username',
                           validators=[InputRequired(message="Enter your username"),
                                       Length(min=3, message="Username must be a least 3 characters long")])

    password = PasswordField('Password',
                             validators=[InputRequired(message="Enter a password"),
                                         Length(min=3, message="Password must be a least 3 characters long")])

    password2 = PasswordField('Password confirmation',
                              validators=[InputRequired(),
                                          Length(min=3),
                                          EqualTo('password', message="Passwords does not match")])

    submit = SubmitField('Register')

    def validate_username(self, field):
        if field.data in [x.id for x in users]:
            raise ValidationError('Username already taken')


class TaskForm(FlaskForm):
    task = StringField('Task',
                       validators=[InputRequired(message="Enter a title"),
                                   Length(min=3, message="Task must be a least 3 characters long")])

    description = StringField('Description')

    due = DateField('Due',
                    validators=[InputRequired(message="Enter a date like this dd/mm/yyyy")])

    submit = SubmitField('Save')
