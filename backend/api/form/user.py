from wtforms import Form, StringField, PasswordField, validators, EmailField


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=5, max=20)])
    email = EmailField('Email Address', [validators.Email()])
    password = PasswordField('New Password', [validators.Length(min=8, max=20)])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=5, max=20)])
    password = PasswordField('Password', [validators.Length(min=8, max=20)])
